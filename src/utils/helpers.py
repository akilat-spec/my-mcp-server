import json
import logging
from typing import Any, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_tool_inputs(inputs: Dict[str, Any], required_fields: list) -> bool:
    """Validate tool input parameters"""
    for field in required_fields:
        if field not in inputs:
            logger.error(f"Missing required field: {field}")
            return False
    return True

def create_success_response(content: str) -> Dict[str, Any]:
    """Create standardized success response"""
    return {
        "content": [{
            "type": "text",
            "text": content
        }]
    }

def create_error_response(error_message: str) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "content": [{
            "type": "text",
            "text": f"Error: {error_message}"
        }]
    }