#!/usr/bin/env python3
"""
MCP Server - Debug Version
"""
import json
import sys
import time

print("🚀 MCP Server Starting...", file=sys.stderr)
print("Python version:", sys.version, file=sys.stderr)
print("Working directory check", file=sys.stderr)

class MCPServer:
    def __init__(self):
        self.initialized = False
        print("✅ MCP Server class initialized", file=sys.stderr)
        
    def handle_initialize(self, request_id, params):
        print("📨 Handling initialize request", file=sys.stderr)
        self.initialized = True
        
        response = {
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
        print(f"✅ Sending initialize response: {response}", file=sys.stderr)
        return response
    
    def handle_tools_list(self, request_id):
        print("📨 Handling tools/list request", file=sys.stderr)
        tools = [
            {
                "name": "greet",
                "description": "A friendly greeting tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Your name"}
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
                        "operation": {"type": "string", "description": "add, subtract, multiply, divide"},
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["operation", "a", "b"]
                }
            }
        ]
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }
        print(f"✅ Sending tools list: {len(tools)} tools", file=sys.stderr)
        return response
    
    def handle_request(self, request):
        try:
            method = request.get("method")
            request_id = request.get("id")
            params = request.get("params", {})
            
            print(f"🔍 Received request - Method: {method}, ID: {request_id}", file=sys.stderr)
            
            if method == "initialize":
                return self.handle_initialize(request_id, params)
            elif method == "tools/list":
                return self.handle_tools_list(request_id)
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                print(f"🔧 Tool call: {name} with args: {arguments}", file=sys.stderr)
                
                if name == "greet":
                    result = f"Hello, {arguments.get('name', 'Friend')}!"
                elif name == "calculator":
                    op = arguments.get("operation", "add")
                    a = arguments.get("a", 0)
                    b = arguments.get("b", 0)
                    if op == "add": result = f"{a} + {b} = {a+b}"
                    elif op == "subtract": result = f"{a} - {b} = {a-b}"
                    elif op == "multiply": result = f"{a} × {b} = {a*b}"
                    elif op == "divide": result = f"{a} ÷ {b} = {a/b}" if b != 0 else "Error: division by zero"
                    else: result = f"Unknown operation: {op}"
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
                print(f"❌ Unknown method: {method}", file=sys.stderr)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
                
        except Exception as e:
            print(f"💥 Error in handle_request: {e}", file=sys.stderr)
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def run(self):
        print("🔄 Starting main server loop...", file=sys.stderr)
        line_count = 0
        
        while True:
            try:
                # Read line from stdin
                line = sys.stdin.readline()
                line_count += 1
                
                if not line:
                    print(f"📭 No more input (line {line_count})", file=sys.stderr)
                    time.sleep(0.1)
                    continue
                
                line = line.strip()
                if not line:
                    print(f"📭 Empty line (line {line_count})", file=sys.stderr)
                    continue
                
                print(f"📥 Received line {line_count}: {line[:100]}...", file=sys.stderr)
                
                # Parse JSON
                request = json.loads(line)
                print(f"📨 Parsed JSON request", file=sys.stderr)
                
                # Handle request
                response = self.handle_request(request)
                
                # Send response
                if response:
                    response_json = json.dumps(response)
                    print(f"📤 Sending response: {response_json}", file=sys.stderr)
                    print(response_json, flush=True)
                    sys.stdout.flush()
                    print("✅ Response sent and flushed", file=sys.stderr)
                else:
                    print("ℹ️ No response to send", file=sys.stderr)
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}", file=sys.stderr)
            except Exception as e:
                print(f"💥 Unexpected error: {e}", file=sys.stderr)
                time.sleep(0.1)

def main():
    print("🎯 Starting MCP Server main function", file=sys.stderr)
    server = MCPServer()
    server.run()

if __name__ == "__main__":
    main()
