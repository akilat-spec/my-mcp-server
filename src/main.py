#!/usr/bin/env python3
"""
MCP Server - HTTP Version for Smithey Scanning
"""
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class MCPHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle MCP requests"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            request = json.loads(post_data.decode('utf-8'))
            
            print(f"📨 Received request: {request}", file=sys.stderr)
            
            # Handle the request
            response = self.handle_mcp_request(request)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_json = json.dumps(response).encode('utf-8')
            self.wfile.write(response_json)
            print(f"📤 Sent response: {response}", file=sys.stderr)
            
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            self.send_error(500, str(e))
    
    def handle_mcp_request(self, request):
        """Handle MCP protocol requests"""
        method = request.get("method")
        request_id = request.get("id")
        
        if method == "initialize":
            return {
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
        
        elif method == "tools/list":
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
                                "description": "add, subtract, multiply, divide",
                                "enum": ["add", "subtract", "multiply", "divide"]
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
        
        elif method == "tools/call":
            params = request.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            if name == "greet":
                result = f"Hello, {arguments.get('name', 'Friend')}! Welcome to MCP Server!"
            elif name == "calculator":
                op = arguments.get("operation", "add")
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                
                if op == "add": result = f"{a} + {b} = {a + b}"
                elif op == "subtract": result = f"{a} - {b} = {a - b}"
                elif op == "multiply": result = f"{a} × {b} = {a * b}"
                elif op == "divide": 
                    if b == 0: result = "Error: Cannot divide by zero"
                    else: result = f"{a} ÷ {b} = {a / b}"
                else: result = f"Unknown operation: {op}"
            else:
                result = f"Unknown tool: {name}"
            
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
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    def log_message(self, format, *args):
        """Override to log to stderr instead of stdout"""
        print(f"🌐 HTTP {format % args}", file=sys.stderr)

def run_server():
    """Run the HTTP server"""
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPHandler)
    
    print(f"🚀 MCP HTTP Server running on port {port}", file=sys.stderr)
    print("✅ Server ready for Smithey scanning", file=sys.stderr)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("🛑 Server stopped", file=sys.stderr)
    except Exception as e:
        print(f"💥 Server error: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_server()
