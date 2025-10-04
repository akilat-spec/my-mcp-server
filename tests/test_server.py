import pytest
import asyncio
from src.server import MyMCPServer

class TestMCPServer:
    """Test cases for MCP server"""
    
    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test server initialization"""
        server = MyMCPServer()
        assert server is not None
        assert server.server is not None
    
    # Add more server tests as needed