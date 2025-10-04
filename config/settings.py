import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Server Configuration
    SERVER_NAME = os.getenv("MCP_SERVER_NAME", "my-mcp-server")
    SERVER_VERSION = os.getenv("MCP_SERVER_VERSION", "1.0.0")
    SERVER_DESCRIPTION = os.getenv("MCP_SERVER_DESCRIPTION", "My Python MCP Server")
    
    # Server Settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()