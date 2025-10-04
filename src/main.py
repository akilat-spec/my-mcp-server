#!/usr/bin/env python3
"""
Main entry point for the MCP Server
"""
import asyncio
import logging
from src.server import MyMCPServer
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """Main function to start the MCP server"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Starting {settings.SERVER_NAME} v{settings.SERVER_VERSION}")
        
        # Create and run MCP server
        server = MyMCPServer()
        await server.run()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())