import asyncio
import sys
from mcp import Server, StdioServerTransport
from mcp.types import CallToolRequest, ListToolsRequest, JsonObject
from src.tools.example_tools import ExampleTools
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class MyMCPServer:
    def __init__(self):
        self.server = Server(settings.SERVER_NAME, settings.SERVER_VERSION)
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up MCP request handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[JsonObject]:
            """Return list of available tools"""
            tools = [
                {
                    "name": "get_weather",
                    "description": "Get weather information for a city",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name to get weather for"
                            }
                        },
                        "required": ["city"]
                    }
                },
                {
                    "name": "calculate_bmi",
                    "description": "Calculate BMI from weight and height",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "weight": {
                                "type": "number",
                                "description": "Weight in kilograms"
                            },
                            "height": {
                                "type": "number",
                                "description": "Height in centimeters"
                            }
                        },
                        "required": ["weight", "height"]
                    }
                },
                {
                    "name": "text_analyzer",
                    "description": "Analyze text and provide statistics",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to analyze"
                            }
                        },
                        "required": ["text"]
                    }
                }
            ]
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: JsonObject) -> list[JsonObject]:
            """Handle tool execution requests"""
            try:
                if name == "get_weather":
                    city = arguments.get("city", "")
                    result = await ExampleTools.get_weather(city)
                    return [{"type": "text", "text": result["content"][0]["text"]}]
                
                elif name == "calculate_bmi":
                    weight = arguments.get("weight", 0)
                    height = arguments.get("height", 0)
                    result = await ExampleTools.calculate_bmi(weight, height)
                    return [{"type": "text", "text": result["content"][0]["text"]}]
                
                elif name == "text_analyzer":
                    text = arguments.get("text", "")
                    result = await ExampleTools.text_analyzer(text)
                    return [{"type": "text", "text": result["content"][0]["text"]}]
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                error_msg = f"Tool execution failed: {str(e)}"
                logger.error(error_msg)
                return [{"type": "text", "text": error_msg}]
    
    async def run(self):
        """Run the MCP server"""
        try:
            # Use stdio transport for MCP protocol
            transport = StdioServerTransport()
            await self.server.run(transport)
            logger.info("MCP Server started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start MCP server: {e}")
            sys.exit(1)