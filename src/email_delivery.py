from typing import List
from src.mcp_client import GoogleWorkspaceMCPClient
from src.logger import get_logger

logger = get_logger(__name__)

async def deliver_email_teaser(
    mcp_client: GoogleWorkspaceMCPClient, 
    to_emails: List[str], 
    subject: str, 
    html_body: str,
    draft_only: bool = True
) -> str:
    """
    Uses the MCP client to send an email (or create a draft) containing the HTML teaser.
    Defaults to draft_only=True for safety during staging/testing.
    Returns the message ID or draft ID.
    """
    action_str = "Creating draft" if draft_only else "Sending email"
    logger.info(f"{action_str} teaser to {len(to_emails)} recipients...")
    
    try:
        # Note: We use generic tool names here. The exact name will depend on 
        # the provided Google Workspace MCP server schema.
        tool_name = "gmail_create_draft" if draft_only else "gmail_send_message"
        
        result = await mcp_client.call_tool(tool_name, {
            "to": to_emails,
            "subject": subject,
            "html_body": html_body
        })
        
        logger.info(f"Successfully executed {tool_name}.")
        return str(result)
        
    except Exception as e:
        logger.error(f"Failed to deliver email teaser: {str(e)}")
        raise
