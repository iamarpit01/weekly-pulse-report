import json
import os
from typing import List
from src.logger import get_logger
from src.mcp_client import GoogleWorkspaceMCPClient

logger = get_logger(__name__)

STATE_FILE = ".groww_state.json"

def get_processed_weeks() -> List[str]:
    """Reads the local state file to get a list of already processed ISO weeks."""
    if not os.path.exists(STATE_FILE):
        return []
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("processed_weeks", [])
    except Exception as e:
        logger.error(f"Failed to read state file: {str(e)}")
        return []

def mark_week_processed(iso_week: str) -> None:
    """Adds the ISO week to the local state file to prevent duplicate processing."""
    weeks = set(get_processed_weeks())
    weeks.add(iso_week)
    
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"processed_weeks": list(weeks)}, f, indent=2)
        logger.info(f"Marked week {iso_week} as processed in local state.")
    except Exception as e:
        logger.error(f"Failed to write state file: {str(e)}")

async def check_doc_for_anchor(mcp_client: GoogleWorkspaceMCPClient, doc_id: str, anchor_text: str) -> bool:
    """
    Uses the MCP client to read the target Google Doc and check if the anchor text exists.
    Returns True if the anchor is found (meaning the report for this week is already published).
    """
    logger.info(f"Checking Google Doc {doc_id} for anchor: '{anchor_text}'")
    try:
        # Note: We will dynamically fetch the document content. The exact tool name
        # will depend on the provided Google Workspace MCP server schema.
        # Typical names: "docs_get", "read_google_doc", "document_get"
        result = await mcp_client.call_tool("docs_read_document", {
            "document_id": doc_id
        })
        
        if getattr(result, "isError", False):
            logger.error(f"Failed to read doc. Assuming anchor not found. Error: {result.content}")
            return False
            
        content = ""
        for item in result.content:
            if item.type == "text":
                content += item.text
        if anchor_text in content:
            logger.info("Anchor found! This week has already been published to the Doc.")
            return True
            
        logger.info("Anchor not found in Doc. Safe to append.")
        return False
        
    except Exception as e:
        logger.error(f"Error checking doc for anchor: {str(e)}")
        # If we hit an error, we assume it's not safe to blindly append (to prevent duplicates)
        # or we could return False to force retry. Returning False for now.
        return False
