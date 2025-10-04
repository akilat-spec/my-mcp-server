#!/usr/bin/env python3
"""
MCP Server - Correct MCP Protocol Implementation
"""
import asyncio
import json
import sys
import traceback

class SimpleMCPServer:
    def __init__(self):
        self.initialized = False
        
    async def handle_initialize(self, request_id, params):
        """Handle initialization request"""
        self.initialized = True
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "my-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    
    async def handle_tools_list(self, request_id):
        """Handle tools/list request"""
        if not self.initialized:
            return self.create_error(request_id, -32002, "Server not initialized")
            
        tools = [
            {
                "name": "greet",
                "description": "A friendly greeting tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Your name"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "calculator",
                "description": "Simple calculator with basic operations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string", 
                            "description": "Operation: add, subtract, multiply, divide"
                        },
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number"
                        }
                    },
                    "required": ["operation", "a", "b"]
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }
    
    async def handle_tools_call(self, request_id, name, arguments):
        """Handle tools/call request"""
        if not self.initialized:
            return self.create_error(request_id, -32002, "Server not initialized")
            
        try:
            if name == "greet":
                user_name = arguments.get("name", "Friend")
                result = f"Hello, {user_name}! Welcome to MCP Server!"
                
            elif name == "calculator":
                operation = arguments.get("operation", "add")
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                
                if operation == "add":
                    result = f"{a} + {b} = {a + b}"
                elif operation == "subtract":
                    result = f"{a} - {b} = {a - b}"
                elif operation == "multiply":
                    result = f"{a} × {b} = {a * b}"
                elif operation == "divide":
                    if b == 0:
                        result = "Error: Cannot divide by zero"
                    else:
                        result = f"{a} ÷ {b} = {a / b}"
                else:
                    result = f"Unknown operation: {operation}"
            else:
                return self.create_error(request_id, -32601, f"Tool not found: {name}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            }
            
        except Exception as e:
            return self.create_error(request_id, -32603, f"Tool execution failed: {str(e)}")
    
    def create_error(self, request_id, code, message):
        """Create error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    async def handle_request(self, request):
        """Main request handler"""
        try:
            method = request.get("method")
            request_id = request.get("id")
            params = request.get("params", {})
            
            if method == "initialize":
                return await self.handle_initialize(request_id, params)
            elif method == "tools/list":
                return await self.handle_tools_list(request_id)
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                return await self.handle_tools_call(request_id, name, arguments)
            elif method == "notifications/cancelled":
                # Ignore cancellation notifications
                return None
            else:
                return self.create_error(request_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            return self.create_error(request.get("id"), -32603, f"Internal error: {str(e)}")
    
    async def run(self):
        """Main server loop"""
        print("🚀 MCP Server starting...", file=sys.stderr)
        
        while True:
            try:
                # Read from stdin
                line = sys.stdin.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON request
                request = json.loads(line)
                print(f"Received: {request}", file=sys.stderr)
                
                # Handle request
                response = await self.handle_request(request)
                
                # Send response if not None
                if response is not None:
                    response_json = json.dumps(response)
                    print(response_json, flush=True)
                    print(f"Sent: {response_json}", file=sys.stderr)
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}", file=sys.stderr)
                continue
            except Exception as e:
                print(f"Unexpected error: {e}", file=sys.stderr)
                traceback.print_exc()
                continue

async def main():
    server = SimpleMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
