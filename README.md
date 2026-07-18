# Groww Pulse AI Agent 🚀

An autonomous AI pipeline that extracts raw user feedback from the Google Play Store, uses Machine Learning to identify hidden themes, and leverages LLMs to generate actionable product reports. It automatically delivers these reports directly into Google Workspace (Docs & Gmail) via a custom Model Context Protocol (MCP) server.

---

## 🧠 Technologies & Topics Covered

1. **Web Scraping:** `google-play-scraper`
2. **Data Sanitization:** PII Scrubbing (Regex & Contextual removal)
3. **Machine Learning & NLP:** 
   - **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
   - **Dimensionality Reduction:** `UMAP`
   - **Density-Based Clustering:** `HDBSCAN`
4. **Large Language Models (LLMs):** `Groq` API (Llama-3 architecture)
5. **System Architecture:** Model Context Protocol (MCP) standard for AI tool execution.
6. **Cloud Integrations:** Google Workspace APIs (Docs & Gmail) via User OAuth2.
7. **CI/CD Automation:** GitHub Actions (Cron Jobs).

---

## 🔄 The End-to-End Flow

The entire application is orchestrated by `src/main.py`, which coordinates 5 distinct phases:

### Phase 1: Data Ingestion (`src/scraper.py`)
The agent connects to the Google Play Store and downloads all reviews for the Groww app posted within the last 7 days (the ISO week).

### Phase 2: Data Sanitization (`src/pii_scrubber.py`)
Before any AI processes the data, the scrubber scans the raw reviews and masks Personally Identifiable Information (PII) such as phone numbers, emails, and account details to ensure user privacy.

### Phase 3: AI Analysis (`src/embeddings.py`, `src/clustering.py`, `src/summarizer.py`)
This is the core brain of the operation:
1. **Embedding:** The agent converts the text of every review into mathematical vectors (embeddings) using a local, open-source model (`all-MiniLM-L6-v2`). This allows the computer to understand the "semantic meaning" of the text.
2. **Clustering:** It uses UMAP to compress those vectors, and HDBSCAN to group similar reviews together into distinct "Clusters" (e.g., all reviews complaining about withdrawal bugs end up in Cluster A; all reviews praising the UI end up in Cluster B).
3. **Summarization:** The agent sends each cluster to the ultra-fast Groq LLM. The LLM acts as a Product Manager, analyzing the cluster and writing a formatted Markdown summary containing actionable recommendations and verbatim user quotes.

### Phase 4: Output Rendering
The agent stitches all the individual cluster summaries together into one massive, cohesive Markdown document, formatted beautifully with headers, blockquotes, and lists.

### Phase 5: Google Delivery (`src/docs_delivery.py`, `src/email_delivery.py`)
Instead of talking to Google directly, the agent spawns a **Custom MCP Server** as a background subprocess. 
1. The agent securely passes the Markdown payload to the MCP server.
2. The MCP Server authenticates via your saved OAuth `token.pickle`.
3. The MCP server calls the Google Docs API to append the report to your live document.
4. The MCP server calls the Gmail API to dispatch an HTML notification email to your stakeholders.

---

## 📁 Project Structure

### Core Application
- **`src/main.py`**: The master orchestrator script. Run this to execute the entire pipeline.
- **`src/state_manager.py`**: Ensures idempotency. It checks the Google Doc before running to ensure it doesn't accidentally publish the same week's report twice.
- **`src/logger.py`**: Custom logging configuration that ensures logs are written to `stderr` so they don't corrupt the MCP server's JSON-RPC communication on `stdout`.

### Pipeline Modules
- **`src/scraper.py`**: Connects to the Play Store.
- **`src/pii_scrubber.py`**: Cleans sensitive data.
- **`src/embeddings.py`**: Generates NLP embeddings.
- **`src/clustering.py`**: Groups data using UMAP/HDBSCAN.
- **`src/summarizer.py`**: Prompts the Groq LLM.

### Model Context Protocol (MCP) Server
- **`src/mcp_server/`**: A fully isolated directory containing the custom Python MCP Server.
  - **`server.py`**: Defines the JSON-RPC interface and the 4 available tools (`docs_read_document`, `docs_append_text`, `gmail_create_draft`, `gmail_send_message`).
  - **`auth.py`**: Handles Google OAuth2 login flows and manages `token.pickle` state.
  - **`google_workspace.py`**: Contains the actual raw API calls to Google Docs and Gmail.

### Delivery Modules
- **`src/mcp_client.py`**: An asynchronous client that `main.py` uses to talk to the MCP server via standard input/output.
- **`src/docs_delivery.py`**: Formats the MCP request for Google Docs.
- **`src/email_delivery.py`**: Constructs the HTML email template and formats the MCP request for Gmail.

### Configuration & Automation
- **`.env`**: Holds all environment variables (API keys, Document IDs, Emails).
- **`requirements.txt`**: Python dependencies.
- **`.github/workflows/pulse_cron.yml`**: The GitHub Actions workflow that automatically wakes up every Monday morning and runs `main.py`.
- **`credentials.json`**: The Google Cloud OAuth Client ID (downloaded by the user).
- **`token.pickle`**: The secure session token generated after the user logs in via the browser.
