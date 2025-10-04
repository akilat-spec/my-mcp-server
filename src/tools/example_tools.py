from typing import Dict, Any
import requests
from src.utils.helpers import validate_tool_inputs, create_success_response, create_error_response

class ExampleTools:
    """Example MCP tools implementation"""
    
    @staticmethod
    async def get_weather(city: str) -> Dict[str, Any]:
        """Get weather information for a city"""
        try:
            # This is a mock implementation - replace with real API
            if not city:
                return create_error_response("City parameter is required")
            
            # Simulate API call
            # In real implementation, you would call a weather API
            weather_data = {
                "city": city,
                "temperature": "22°C",
                "conditions": "Sunny",
                "humidity": "65%"
            }
            
            response_text = f"""
Weather in {weather_data['city']}:
- Temperature: {weather_data['temperature']}
- Conditions: {weather_data['conditions']}
- Humidity: {weather_data['humidity']}
"""
            return create_success_response(response_text)
            
        except Exception as e:
            return create_error_response(f"Failed to get weather: {str(e)}")
    
    @staticmethod
    async def calculate_bmi(weight: float, height: float) -> Dict[str, Any]:
        """Calculate BMI from weight and height"""
        try:
            if weight <= 0 or height <= 0:
                return create_error_response("Weight and height must be positive numbers")
            
            # Calculate BMI
            height_in_meters = height / 100  # Convert cm to meters
            bmi = weight / (height_in_meters ** 2)
            
            # Determine BMI category
            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 25:
                category = "Normal weight"
            elif bmi < 30:
                category = "Overweight"
            else:
                category = "Obese"
            
            response_text = f"""
BMI Calculation Results:
- Weight: {weight} kg
- Height: {height} cm
- BMI: {bmi:.2f}
- Category: {category}
"""
            return create_success_response(response_text)
            
        except Exception as e:
            return create_error_response(f"BMI calculation failed: {str(e)}")
    
    @staticmethod
    async def text_analyzer(text: str) -> Dict[str, Any]:
        """Analyze text and provide statistics"""
        try:
            if not text:
                return create_error_response("Text parameter is required")
            
            # Basic text analysis
            word_count = len(text.split())
            char_count = len(text)
            sentence_count = text.count('.') + text.count('!') + text.count('?')
            
            response_text = f"""
Text Analysis Results:
- Character count: {char_count}
- Word count: {word_count}
- Sentence count: {sentence_count}
- Average word length: {char_count/word_count:.2f} characters
"""
            return create_success_response(response_text)
            
        except Exception as e:
            return create_error_response(f"Text analysis failed: {str(e)}")