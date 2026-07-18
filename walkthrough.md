# Groww Play Store Reviews Agent

This project successfully automates the ingestion, clustering, and summarization of user reviews for the Groww Android app using a combination of local NLP models, the Groq LLM API, and Google Workspace integrations via the Model Context Protocol (MCP).

## Architecture & Data Flow

The agent runs as a seamless pipeline triggered weekly via GitHub Actions:

1. **Ingestion** ([src/scraper.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/scraper.py)): Fetches the latest week of reviews from the Google Play Store, automatically filtering out noise (reviews with < 10 words) and stripping out bloated metadata.
2. **PII Scrubbing** ([src/pii_scrubber.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/pii_scrubber.py)): Sanitizes the reviews by replacing emails, phone numbers, and profile images with `[REDACTED]` to protect user privacy.
3. **Embeddings & Clustering** ([src/embeddings.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/embeddings.py), [src/clustering.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/clustering.py)): 
   - Uses the lightweight local `all-MiniLM-L6-v2` model from `sentence-transformers` to generate 384-dimensional dense vectors.
   - Reduces dimensionality with **UMAP** and clusters the vectors with **HDBSCAN** to isolate distinct emerging themes and automatically discard scattered noise (`Cluster -1`).
4. **LLM Summarization** ([src/summarizer.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/summarizer.py)): Batches the clustered reviews and prompts the `llama-3.3-70b-versatile` model on Groq to generate theme names, actionable ideas, and extract exact verbatim quotes. It includes an **anti-hallucination post-processor** to ensure no quotes are fabricated.
5. **Output Rendering** ([src/renderer.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/renderer.py)): Formats the raw LLM JSON payload into a structured Markdown document and a clean HTML email teaser.
6. **Delivery via MCP** ([src/docs_delivery.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/docs_delivery.py), [src/email_delivery.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/email_delivery.py)): Uses a Google Workspace MCP server to automatically append the markdown report to a canonical Google Doc and send an HTML email teaser to stakeholders.
7. **Idempotency** ([src/state_manager.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/state_manager.py)): Maintains a local `.groww_state.json` file and actively checks the remote Google Doc to ensure a week's report is never appended or emailed twice.

## Deployment

- The entire orchestration logic is housed in the master orchestrator [src/main.py](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/src/main.py).
- Automation is securely configured in [.github/workflows/pulse_cron.yml](file:///Users/arpitdayal/Desktop/Nextleap/GrowwAgents/.github/workflows/pulse_cron.yml), scheduled to run every Monday at 08:00 AM IST.

> [!TIP]
> To run the script manually:
> ```bash
> pip install -r requirements.txt
> cp .env.example .env # Fill in your GROQ_API_KEY, TARGET_DOC_ID, etc.
> PYTHONPATH=. python src/main.py --product Groww
> ```

---

# Deep-Dive Architecture & Technical Approaches

This section provides a comprehensive technical breakdown of the approaches, algorithms, and architectural decisions used to build the Groww Pulse AI Agent.

## 1. The NLP Engine: Embeddings & Vector Spaces (`src/embeddings.py`)

### The Problem
Computers cannot understand raw text. To group similar reviews together, we need a mathematical way to measure "semantic similarity" (e.g., recognizing that *"The UI is broken"* and *"The screen freezes"* mean the same thing).

### The Approach: Dense Vector Embeddings
We utilize **Sentence Transformers** (specifically the `all-MiniLM-L6-v2` model) to convert every single review into a **Vector Embedding**. 
- **What is it?** An embedding is a high-dimensional mathematical coordinate. Our model takes a review and turns it into an array of 384 floating-point numbers (a 384-dimensional vector).
- **Why Local?** Instead of calling OpenAI's embedding API, we download the model weights to the local machine. This guarantees 100% data privacy and operates at lightning speed without network latency or API costs.
- **The Result:** Reviews that discuss similar topics (like "login issues") end up having vectors that are mathematically close to each other in 384-dimensional space.

*(Note: We do not use a persistent Vector Database like Pinecone or ChromaDB because our pipeline processes discrete, ephemeral 7-day batches in memory. The vectors are discarded after the weekly report is generated, keeping the architecture stateless and lightweight).*

---

## 2. The Clustering Engine: UMAP + HDBSCAN (`src/clustering.py`)

### The Problem
Once we have 157 vectors floating in 384-dimensional space, we need an algorithm to find the "clumps" or "themes" automatically. Standard algorithms like K-Means are terrible for NLP because they force you to guess the number of clusters (`K`) in advance, and they force every outlier into a cluster, polluting the data.

### The Approach: Dimensionality Reduction & Density Clustering
We use a two-step pipeline that represents the state-of-the-art in topic modeling:

#### Step A: UMAP (Uniform Manifold Approximation and Projection)
- 384 dimensions are too sparse for clustering algorithms to work efficiently (the "curse of dimensionality"). 
- UMAP acts as a mathematical compressor. It squashes the 384-dimensional vectors down into 5-dimensional vectors while preserving the local and global distances between the reviews.

#### Step B: HDBSCAN (Hierarchical Density-Based Spatial Clustering)
- HDBSCAN sweeps through the compressed 5D space looking for densely packed "galaxies" of points. 
- **Why it's brilliant:** It doesn't require us to guess how many themes exist. If there are 3 themes this week, it finds 3. If there are 12 themes, it finds 12. 
- **Noise Rejection:** If a review is completely random and doesn't fit a theme, HDBSCAN classifies it as "Noise" (Cluster -1) and discards it. This guarantees that our LLM only receives highly coherent, thematic data.

---

## 3. The LLM Strategy: Map-Reduce Summarization (`src/summarizer.py`)

### The Problem
If we simply dumped 157 raw reviews into ChatGPT and said "summarize this", the LLM would suffer from "Lost in the Middle" syndrome. It would focus on the first and last few reviews and completely hallucinate or ignore the rest.

### The Approach: Micro-Summarization via Groq
Because we have already grouped the reviews into highly specific clusters using HDBSCAN, we feed the LLM **one cluster at a time**.
- We use the **Groq API** (running the Llama-3 architecture). Groq uses specialized LPU hardware to generate tokens at over 800 words per second.
- We prompt the LLM to act as a Senior Product Manager. We pass it the exact 15 to 30 reviews in "Cluster A" and demand a Title, Actionable Recommendations, and 3 verbatim, exact quotes.
- By breaking the problem down, the LLM has perfect attention and zero hallucinations. It processes 10 distinct clusters in parallel/series and we simply append the outputs together.

---

## 4. The Model Context Protocol (MCP) Architecture (`src/mcp_server/`)

### The Problem
AI agents traditionally struggle to interact with the real world safely. Giving an AI a raw API key to Google Workspace is dangerous, and writing custom API wrappers for every new tool is exhausting. 

### The Approach: Custom Python MCP Server
We adopted the **Model Context Protocol (MCP)**, an open-source standard pioneered by Anthropic. MCP acts as a universal, secure bridge between AI applications and data sources.

- **How it works:** We built a fully isolated `mcp_server` that exposes specific "Tools" (like `docs_append_text` and `gmail_send_message`). 
- **The Transport Layer (`stdio`):** Instead of running a complex web server (HTTP/REST), the MCP server is spawned as a child process by `main.py`. The two programs communicate instantly and securely by writing JSON-RPC messages to standard input/output (`stdio`).
- **Isolation of Concerns:** The main ML pipeline has zero knowledge of Google's complex OAuth2 flows, token pickling, or Google Docs batch update syntax. It simply says over the MCP protocol: *"Call the `docs_append_text` tool with this payload."*
- **The Google Integration:** Inside the MCP Server (`google_workspace.py`), we use the official Google API Client to catch the JSON-RPC request, locate the user's `token.pickle`, and securely push the Markdown payload into the live Google Doc.

---

## 5. Security & Idempotency (`src/state_manager.py` & `src/pii_scrubber.py`)

1. **PII Scrubbing:** Before the reviews even reach the embedding model or the LLM, a strict Regex and Contextual scrubber strips out phone numbers, emails, and sensitive identifiers. 
2. **Idempotency (Safe Retries):** The `state_manager.py` uses the MCP server to *read* the target Google Doc before the pipeline starts. It searches for the anchor text (e.g., `[Week 2026-W29] Groww Pulse Report`). If it finds it, the system safely aborts. This ensures that if the cron job accidentally triggers twice, you will never get duplicate reports appended to your document.

---

## 6. Interactive Frontend & Data Integration (`frontend/`)

### The Problem
The output of the ML pipeline is inherently heavy text (Markdown). While this is perfect for Google Docs, stakeholders often need a high-level, scannable dashboard to see the macro-trends at a glance.

### The Approach: Data-Driven React Dashboard
We built a local React application (using Vite and Tailwind CSS) that acts as a visual layer on top of the backend's computations. Rather than the frontend establishing database connections or dealing with APIs, the ML pipeline (`main.py`) acts as a static site generator.

#### The Data Lifecycle (End-to-End Flow)
1. **Generation:** At the end of the Python backend's execution, `main.py` collects the raw data (scraped scores, user names) and the ML-processed data (HDBSCAN clusters, Groq LLM themes, extracted quotes). It mathematically calculates the UI-specific metrics (Net Sentiment, 5-Star Distribution).
2. **Storage:** Instead of pushing to a database, the Python script serializes this data into a structured JSON dictionary and writes it directly to the React application's public asset folder: `frontend/public/data.json`.
3. **Fetching:** When the user opens the React dashboard, the `App.jsx` component mounts. A React `useEffect` hook triggers an asynchronous `fetch('/data.json')` request to the local Vite development server to pull the static JSON artifact into memory.
4. **Insertion:** The parsed JSON object is stored in a React state variable (`const [data, setData] = useState(null)`). The UI is built using conditional rendering; once the state populates, the React components map over the data arrays and directly inject the properties into the JSX elements.

The dashboard UI components (tiles) are deeply integrated with this data payload:

#### Tile 1: Top KPI Row
- **What it shows:** Net Sentiment, Velocity Score, Clustered Mentions, and AI Confidence.
- **Approach:** During the data ingestion phase (`scraper.py`), the backend aggregates the raw 1-5 star scores. The backend calculates the `average_rating` and `net_sentiment` mathematically before pushing the JSON. The React frontend simply binds these pre-calculated values to the KPI cards, eliminating heavy client-side computation.

#### Tile 2: Critical Verbatims List
- **What it shows:** Highlighted, exact quotes from users complaining about critical bugs, complete with their actual user names (e.g., *Amit Kumar*).
- **Approach:** The Groq LLM extracts the raw quotes, but the LLM drops the user metadata. To solve this, a mapping function in `main.py` intercepts the LLM output, searches the original Play Store JSON payload for string matches, extracts the original author's `userName`, and marries the two pieces of data together before saving `data.json`.

#### Tile 3: Rating Distribution Card
- **What it shows:** A horizontal bar chart mapping the percentage of 1-star through 5-star reviews.
- **Approach:** The Python backend calculates the distribution percentages during scraping. The React component iterates over this payload `{[5, 4, 3, 2, 1]}` and dynamically injects the percentages into the `width` property of Tailwind CSS divs, creating an instantaneous, data-driven bar chart.

#### Tile 4: AI Detected Clusters
- **What it shows:** A table of the themes discovered by HDBSCAN, ranked by volume.
- **Approach:** The UI iterates over the `summaries` array from the LLM. It calculates the max cluster volume and renders an inline progress bar whose width is mathematically proportional to the cluster size, creating a visual heatmap of severity.

#### Tile 5: Google Docs Export Button
- **What it shows:** A top bar button to download the PDF.
- **Approach:** Since the MCP Server anchors the data into a single Google Doc, the React button simply points to `https://docs.google.com/document/d/<TARGET_DOC_ID>/export?format=pdf`. This seamlessly leverages the user's active Google Workspace session to download the PDF without writing custom PDF-generation code on the client.
