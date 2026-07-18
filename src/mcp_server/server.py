import sys
from dotenv import load_dotenv
load_dotenv()

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.mcp_server.google_workspace import (
    docs_read_document,
    docs_append_text,
    gmail_create_draft,
    gmail_send_message
)

# Initialize MCP server
server = Server("google-workspace-mcp")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Register the Google Workspace tools with the MCP client."""
    return [
        types.Tool(
            name="docs_read_document",
            description="Reads the text content of a Google Doc",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"}
                },
                "required": ["document_id"]
            }
        ),
        types.Tool(
            name="docs_append_text",
            description="Appends text to the end of a Google Doc",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "text": {"type": "string"}
                },
                "required": ["document_id", "text"]
            }
        ),
        types.Tool(
            name="gmail_create_draft",
            description="Creates a draft email in Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "subject": {"type": "string"},
                    "html_body": {"type": "string"}
                },
                "required": ["to", "subject", "html_body"]
            }
        ),
        types.Tool(
            name="gmail_send_message",
            description="Sends an email via Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "subject": {"type": "string"},
                    "html_body": {"type": "string"}
                },
                "required": ["to", "subject", "html_body"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Route tool calls from the MCP client to the corresponding Python function."""
    if name == "docs_read_document":
        result = docs_read_document(arguments["document_id"])
    elif name == "docs_append_text":
        result = docs_append_text(arguments["document_id"], arguments["text"])
    elif name == "gmail_create_draft":
        result = gmail_create_draft(arguments["to"], arguments["subject"], arguments["html_body"])
    elif name == "gmail_send_message":
        result = gmail_send_message(arguments["to"], arguments["subject"], arguments["html_body"])
    else:
        raise ValueError(f"Unknown tool: {name}")
        
    return [types.TextContent(type="text", text=str(result))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
