# Edge Cases & Corner Cases: Weekly Product Review Pulse (Groww)

This document outlines potential edge cases and corner cases across the system's pipeline, along with proposed handling strategies to ensure the Weekly Product Review Pulse remains robust and reliable.

---

## 1. Data Ingestion (Google Play Scraper)

| Edge Case | Impact | Handling Strategy |
| :--- | :--- | :--- |
| **Zero Reviews Fetched** | Pipeline fails or generates an empty report. | Gracefully halt the pipeline. Send an informational email stating "No new reviews found for the specified period" instead of a blank report. |
| **Play Store Rate Limits / IP Bans** | Scraper is blocked, resulting in missing data. | Implement exponential backoff and retries. If persistent, alert the administrator and gracefully fail the run. |
| **Massive Volume Spike** (e.g., viral bug) | Out-of-memory errors, extremely long processing times, or hitting LLM token/cost limits. | Implement **reservoir sampling** or limit ingestion to the top $N$ most relevant/helpful/lowest-rated reviews to keep token usage bounded. |
| **Non-English, Gibberish, or Emoji-only Reviews** | Embeddings create noisy clusters; LLM produces garbage summaries. | Apply a pre-filtering step (e.g., `langdetect`) to drop non-English reviews or reviews below a minimum word count. |
| **Play Store DOM/API Structure Changes** | Scraper breaks entirely. | Add strict schema validation on the scraped output. If the schema fails, abort the run and trigger an immediate developer alert. |

---

## 2. Reasoning & NLP Pipeline

| Edge Case | Impact | Handling Strategy |
| :--- | :--- | :--- |
| **Everything Clustered as "Noise" (-1)** | HDBSCAN fails to find dense clusters due to extreme diversity in reviews. | Fallback logic: If >X% of reviews are noise, group them into a generic "Miscellaneous Feedback" bucket and use a map-reduce LLM prompt to extract broad themes. |
| **LLM Hallucinates Quotes** | The generated quote sounds plausible but does not exist in the source reviews. | The **Quote Validator** must perform an exact substring match (or high-similarity fuzzy match). If it fails, either retry the LLM prompt once or drop the quote from the final report. |
| **PII Scrubber False Negatives** | Sensitive user data (like obscure ID formats) leaks to the LLM. | Layer multiple heuristics (Regex + NLP-based like Presidio). Prioritize over-redaction over under-redaction. |
| **LLM API Outages or 429 Rate Limits** | Pipeline halts mid-execution. | Implement robust retry mechanisms with exponential backoff (e.g., using `tenacity` in Python). Save intermediate clustering state so the run can resume without re-embedding. |
| **Context Window Exceeded** | A specific cluster has too many long reviews, exceeding the LLM's context window. | Truncate the reviews within the cluster or randomly sample reviews from the cluster until it fits within the context limit. |

---

## 3. Rendering & Delivery (MCP Client)

| Edge Case | Impact | Handling Strategy |
| :--- | :--- | :--- |
| **External MCP Server Down** | Cannot append to Docs or send Gmail. | Save the fully rendered Docs and Email payloads locally as JSON/Markdown. Retry delivery on the next scheduled cron tick without re-running the heavy NLP pipeline. |
| **Partial Failure (Docs appended, Email failed)** | Document is updated, but stakeholders are not notified. On retry, the Doc might be duplicated. | **Strict Idempotency Check:** Before appending, use the MCP tool to check if the `[Week XX]` anchor exists in the Doc. If it does, skip the append phase and only retry the Email phase. |
| **Google Doc Becomes Too Large** | Google Docs API fails to append due to file size limits. | Monitor Doc size/length. Propose a long-term strategy to rotate documents annually (e.g., `Weekly Pulse - Groww 2026`, `Weekly Pulse - Groww 2027`). |
| **Markdown to Google Docs Formatting Errors** | The MCP server fails to parse the structure correctly, corrupting the Doc layout. | Ensure the rendering engine produces strict, simplified payload structures (avoiding complex nested tables or unsupported HTML) that the MCP tool can safely convert. |

---

## 4. Orchestration & State Management

| Edge Case | Impact | Handling Strategy |
| :--- | :--- | :--- |
| **Overlapping Cron Executions** | Two instances of the pipeline run simultaneously, causing race conditions. | Use a file lock or database lock to ensure only one instance of the agent can run at a time. |
| **Timezone/Date Boundary Issues** | A backfill request straddles leap years or daylight saving boundaries, causing duplicate or missed days. | Standardize all internal date handling on UTC. Only convert to IST for the human-readable report headers. |
| **Local State Corruption** | The local SQLite/JSON tracking idempotency is corrupted or deleted. | Rely on the **Google Doc itself as the primary source of truth**. The agent should always query the Doc via MCP to verify if a week was already processed before relying solely on local state. |
