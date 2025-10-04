#!/usr/bin/env python3
"""
MCP Server - Fully MCP Protocol Compliant
"""
import json
import sys
import time

class MCPServer:
    def __init__(self):
        self.initialized = False
        self.client_info = None
        
    def handle_initialize(self, request_id, params):
        """Handle initialization request"""
        self.initialized = True
        self.client_info = params.get("clientInfo", {})
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {}
                },
                "serverInfo": {
                    "name": "my-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
        print(f"Initialized with client: {self.client_info}", file=sys.stderr)
        return response
    
    def handle_tools_list(self, request_id):
        """Handle tools/list request"""
        if not self.initialized:
            return self.create_error(request_id, -32002, "Server not initialized")
            
        tools = [
            {
                "name": "greet",
                "description": "A friendly greeting tool that welcomes users",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Your name for personalized greeting"
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "calculator",
                "description": "Perform basic mathematical operations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string", 
                            "description": "The operation to perform: add, subtract, multiply, or divide",
                            "enum": ["add", "subtract", "multiply", "divide"]
                        },
                        "a": {
                            "type": "number",
                            "description": "The first number"
                        },
                        "b": {
                            "type": "number",
                            "description": "The second number"
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
    
    def handle_tools_call(self, request_id, name, arguments):
        """Handle tools/call request"""
        if not self.initialized:
            return self.create_error(request_id, -32002, "Server not initialized")
            
        try:
            if name == "greet":
                user_name = arguments.get("name", "Friend")
                result_text = f"Hello, {user_name}! Welcome to my MCP server! 👋"
                
            elif name == "calculator":
                operation = arguments.get("operation", "add")
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                
                if operation == "add":
                    result_text = f"{a} + {b} = {a + b}"
                elif operation == "subtract":
                    result_text = f"{a} - {b} = {a - b}"
                elif operation == "multiply":
                    result_text = f"{a} × {b} = {a * b}"
                elif operation == "divide":
                    if b == 0:
                        result_text = "❌ Error: Cannot divide by zero"
                    else:
                        result_text = f"{a} ÷ {b} = {a / b:.2f}"
                else:
                    return self.create_error(request_id, -32602, f"Invalid operation: {operation}")
            else:
                return self.create_error(request_id, -32601, f"Tool not found: {name}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ]
                }
            }
            
        except Exception as e:
            return self.create_error(request_id, -32603, f"Tool execution failed: {str(e)}")
    
    def create_error(self, request_id, code, message):
        """Create standardized error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    def handle_request(self, request):
        """Main request handler"""
        try:
            method = request.get("method")
            request_id = request.get("id")
            params = request.get("params", {})
            
            print(f"Handling method: {method}", file=sys.stderr)
            
            if method == "initialize":
                return self.handle_initialize(request_id, params)
            elif method == "tools/list":
                return self.handle_tools_list(request_id)
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                return self.handle_tools_call(request_id, name, arguments)
            elif method == "notifications/cancelled":
                # Acknowledge cancellation but no response needed
                print("Request cancelled", file=sys.stderr)
                return None
            elif method == "shutdown":
                # Handle graceful shutdown
                print("Shutdown requested", file=sys.stderr)
                sys.exit(0)
            else:
                return self.create_error(request_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            print(f"Error handling request: {e}", file=sys.stderr)
            return self.create_error(request.get("id"), -32603, f"Internal server error: {str(e)}")
    
    def run(self):
        """Main server loop - synchronous version for better compatibility"""
        print("🚀 MCP Server starting...", file=sys.stderr)
        print("✅ Server ready and waiting for requests", file=sys.stderr)
        
        while True:
            try:
                # Read from stdin (blocking)
                line = sys.stdin.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON request
                request = json.loads(line)
                print(f"📨 Received request: {method if (method := request.get('method')) else 'unknown'}", file=sys.stderr)
                
                # Handle request
                response = self.handle_request(request)
                
                # Send response if not None
                if response is not None:
                    response_json = json.dumps(response)
                    print(response_json, flush=True)
                    print(f"📤 Sent response for: {request.get('method')}", file=sys.stderr)
                else:
                    print(f"ℹ️  No response needed for: {request.get('method')}", file=sys.stderr)
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}", file=sys.stderr)
                continue
            except KeyboardInterrupt:
                print("🛑 Server stopped by user", file=sys.stderr)
                break
            except Exception as e:
                print(f"💥 Unexpected error: {e}", file=sys.stderr)
                continue

def main():
    server = MCPServer()
    server.run()

if __name__ == "__main__":
    main()
