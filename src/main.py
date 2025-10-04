#!/usr/bin/env python3
"""
WORKING MCP Server - Correct Imports
"""
import asyncio
import sys
import json

async def main():
    """Simple MCP server implementation"""
    print("🚀 Starting MCP Server...", file=sys.stderr)
    
    try:
        # Basic MCP server using stdin/stdout
        while True:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            try:
                request = json.loads(line)
                print(f"Received: {request}", file=sys.stderr)
                
                # Handle different MCP methods
                if request.get("method") == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
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
                    
                elif request.get("method") == "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "result": {
                            "tools": [
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
                                    "description": "Simple calculator",
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
                        }
                    }
                    
                elif request.get("method") == "tools/call":
                    tool_name = request["params"]["name"]
                    arguments = request["params"].get("arguments", {})
                    
                    if tool_name == "greet":
                        name = arguments.get("name", "Friend")
                        result = f"Hello, {name}! Welcome to MCP Server!"
                        
                    elif tool_name == "calculator":
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
                        result = f"Unknown tool: {tool_name}"
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result
                                }
                            ]
                        }
                    }
                    
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "error": {
                            "code": -32601,
                            "message": "Method not found"
                        }
                    }
                
                # Send response
                print(json.dumps(response), flush=True)
                print(f"Sent: {response}", file=sys.stderr)
                
            except json.JSONDecodeError:
                print("Invalid JSON", file=sys.stderr)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                
    except KeyboardInterrupt:
        print("Server stopped by user", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())