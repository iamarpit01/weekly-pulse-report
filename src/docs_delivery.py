from src.mcp_client import GoogleWorkspaceMCPClient
from src.logger import get_logger

logger = get_logger(__name__)

async def deliver_to_google_docs(mcp_client: GoogleWorkspaceMCPClient, document_id: str, payload_md: str) -> str:
    """
    Appends the provided Markdown payload to the specified Google Doc.
    Returns the URL to the document (ideally a deep link to the appended section if supported by the MCP server).
    """
    logger.info(f"Appending weekly pulse report to Google Doc ID: {document_id}")
    
    try:
        # Note: We are using a generic tool name assumption here. The exact name will be based
        # on the provided Google Workspace MCP server schema (e.g. 'append_to_doc', 'docs_append_text').
        result = await mcp_client.call_tool("docs_append_text", {
            "document_id": document_id,
            "text": payload_md
        })
        
        if getattr(result, "isError", False):
            raise Exception(f"MCP Tool Error: {result.content}")
            
        logger.info("Successfully appended report to Google Doc.")
        
        # Generate the link to the document. 
        # If the MCP tool result returns a specific heading ID or deep link, we could parse it here.
        # For now, we return the base document link.
        doc_link = f"https://docs.google.com/document/d/{document_id}/edit"
        
        return doc_link
        
    except Exception as e:
        logger.error(f"Failed to deliver payload to Google Doc: {str(e)}")
        raise
