# Phase-wise Implementation Plan: Weekly Product Review Pulse (Groww)

This document outlines the step-by-step, phase-wise implementation plan for building the automated weekly pulse system for Groww's Google Play Store reviews, as described in the architecture and problem statement documents.

---

## Phase 1: Foundation & Project Setup
**Goal:** Establish the project structure, basic orchestration, and verify the connection to the external MCP Server.

1. **Repository Setup:**
   - Initialize the project repository (e.g., Python or TypeScript based on preference).
   - Set up dependency management (e.g., `requirements.txt` / `poetry` or `package.json`).
2. **CLI & Orchestration Skeleton:**
   - Create the CLI entry point that accepts arguments like `product` (hardcoded/default to `Groww`) and `iso_week`.
   - Set up basic logging for future auditing.
3. **MCP Client Integration:**
   - Implement the MCP client layer to connect to the external, provided Google Workspace MCP server.
   - Verify tool discovery (e.g., `document_batch_update`, `gmail_send`) to ensure credentials and connection are functional.

---

## Phase 2: Data Ingestion & Data Safety
**Goal:** Successfully fetch Play Store reviews and ensure sensitive user data is scrubbed before processing.

1. **Google Play Scraper:**
   - Implement the scraper module to fetch reviews for Groww.
   - Add filtering logic to only keep reviews from the specified time window (e.g., last 8–12 weeks).
   - Implement data sampling/limiting to ensure token limits aren't exceeded on high-volume weeks.
2. **PII Scrubbing:**
   - Integrate a PII scrubbing library (e.g., `presidio-analyzer` or custom regex heuristics).
   - Ensure all incoming review texts have names, emails, and phone numbers replaced with placeholders (e.g., `[REDACTED]`).

---

## Phase 3: Reasoning & NLP Pipeline
**Goal:** Process the scrubbed reviews into meaningful clusters and extract themes, actionable ideas, and verified quotes using the Groq API.

1. **Embeddings:**
   - Integrate an open-source local embeddings model (e.g., `sentence-transformers` with `all-MiniLM-L6-v2`) to convert scrubbed text into dense vectors without relying on paid APIs.
2. **Clustering:**
   - Implement dimensionality reduction (UMAP).
   - Implement density-based clustering (HDBSCAN) to group similar reviews together.
3. **LLM Summarization:**
   - Create batched prompts for each cluster.
   - Use the Groq API (`llama-3.3-70b-versatile`) to generate theme names, actionable ideas, and extract representative quotes from the cluster.
   - **Rate Limiting Mitigation**: Implement token truncation and delay logic to respect Groq's strict limits (30 RPM, 12K TPM, 100K TPD).
4. **Quote Validation Post-Processor:**
   - Implement a validation step that checks if the exact quote returned by the LLM exists in the original review text. Discard or fix hallucinated quotes.

---

## Phase 4: Output Rendering
**Goal:** Transform the structured LLM output into formats suitable for Google Docs and Gmail.

1. **Doc Payload Generation:**
   - Render a structured string/Markdown payload containing the top themes, validated quotes, and action ideas.
   - Add a stable anchor (e.g., `[Week XX - YYYY] Groww Pulse`) for idempotency.
2. **Email Teaser Generation:**
   - Render a concise HTML/text email payload highlighting just the top themes.
   - Include a placeholder for the "Read full report" link (to be populated during delivery).

---

## Phase 5: Delivery & Idempotency (via MCP)
**Goal:** Safely deliver the rendered payloads to Google Workspace without duplicates.

1. **Idempotency State Management:**
   - Implement a local state store (e.g., SQLite or JSON file) to track successfully processed ISO weeks.
   - Use the MCP Docs tool to search for existing weekly anchors to avoid duplicate appends.
2. **Google Docs Delivery:**
   - Use the `append_to_doc` (or equivalent) MCP tool to append the week's report section to the canonical Google Doc.
   - Retrieve the heading ID / deep link of the newly appended section.
3. **Gmail Delivery:**
   - Update the email teaser payload with the deep link from the Docs delivery.
   - Use the `gmail_draft_create` or `gmail_send` MCP tool to distribute the email to stakeholders.

---

## Phase 6: Orchestration, Scheduling & Auditing
**Goal:** Automate the execution and ensure complete observability.

1. **Cron Scheduling:**
   - Configure a scheduled job (e.g., cron or GitHub Actions) to trigger the CLI entry point every Monday morning IST.
2. **Audit Logging:**
   - Finalize the audit module to record total reviews ingested, clusters generated, LLM costs/token usage, and delivery metadata (Doc links, Email Message IDs).
   - Save these logs locally or output them to a structured file.
3. **End-to-End Testing & Staging:**
   - Run end-to-end tests for a specific backfilled week.
   - Ensure the system defaults to "draft-only" mode for emails during staging before enabling direct sends.
