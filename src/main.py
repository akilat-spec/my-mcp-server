#!/usr/bin/env python3
"""
MCP Server - No External Dependencies
"""
import asyncio
import json
import sys
import traceback

class SimpleMCPServer:
    def __init__(self):
        self.tools = {
            "greet": {
                "description": "A friendly greeting tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Your name"}
                    },
                    "required": ["name"]
                }
            },
            "calculator": {
                "description": "Simple calculator with basic operations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "description": "add, subtract, multiply, divide"},
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["operation", "a", "b"]
                }
            }
        }

    async def handle_request(self, request):
        try:
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": "my-mcp-server",
                            "version": "1.0.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                tools_list = []
                for name, tool_info in self.tools.items():
                    tools_list.append({
                        "name": name,
                        "description": tool_info["description"],
                        "inputSchema": tool_info["inputSchema"]
                    })
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools_list}
                }
            
            elif method == "tools/call":
                name = request["params"]["name"]
                arguments = request["params"].get("arguments", {})
                
                if name == "greet":
                    result = f"Hello, {arguments.get('name', 'Friend')}! Welcome to MCP Server!"
                elif name == "calculator":
                    operation = arguments.get("operation", "add")
                    a = arguments.get("a", 0)
                    b = arguments.get("b", 0)
                    
                    if operation == "add":
                        result = f"{a} + {b} = {a + b}"
                    elif operation == "subtract":
                        result = f"{a} - {b} = {a - b}"
                    elif operation == "multiply":
                        result = f"{a} * {b} = {a * b}"
                    elif operation == "divide":
                        if b == 0:
                            result = "Error: Cannot divide by zero"
                        else:
                            result = f"{a} / {b} = {a / b}"
                    else:
                        result = f"Unknown operation: {operation}"
                else:
                    result = f"Unknown tool: {name}"
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": result}]
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    async def run(self):
        print("🚀 MCP Server running (stdio)...", file=sys.stderr)
        
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line or line.strip() == "":
                    continue
                    
                request = json.loads(line)
                response = await self.handle_request(request)
                
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                traceback.print_exc()

async def main():
    server = SimpleMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
    