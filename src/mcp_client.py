import asyncio
from typing import Any, Dict, List, Optional
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from src.logger import get_logger

logger = get_logger(__name__)

class GoogleWorkspaceMCPClient:
    """
    A client to interact with the provided external Google Workspace MCP Server.
    Uses stdio for communication by default, assuming the server is a local process
    or proxied process. This can be adapted for SSE if the provided server uses HTTP.
    """
    def __init__(self, server_command: str, server_args: List[str]):
        self.server_parameters = StdioServerParameters(
            command=server_command,
            args=server_args
        )
        self._session: Optional[ClientSession] = None
        self._exit_stack = None

    async def connect(self):
        """Establish connection to the MCP server and discover tools."""
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        
        logger.info(f"Connecting to MCP server using command: {self.server_parameters.command}")
        
        try:
            stdio_transport = await self._exit_stack.enter_async_context(
                stdio_client(self.server_parameters)
            )
            self._session = await self._exit_stack.enter_async_context(
                ClientSession(stdio_transport[0], stdio_transport[1])
            )
            
            await self._session.initialize()
            logger.info("Successfully connected and initialized MCP session.")
            
            # Verify tool discovery
            tools = await self._session.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            logger.info(f"Discovered tools: {', '.join(tool_names)}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MCP Server: {str(e)}")
            await self.close()
            raise

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Helper to call a specific tool on the MCP server."""
        if not self._session:
            raise RuntimeError("Not connected to MCP server.")
        
        logger.info(f"Calling MCP tool: {name}")
        result = await self._session.call_tool(name, arguments)
        return result

    async def close(self):
        """Close the connection to the MCP server."""
        if self._exit_stack:
            await self._exit_stack.aclose()
            self._exit_stack = None
            self._session = None
            logger.info("Closed MCP session.")
