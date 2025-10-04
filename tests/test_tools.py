import pytest
import asyncio
from src.tools.example_tools import ExampleTools

class TestExampleTools:
    """Test cases for example tools"""
    
    @pytest.mark.asyncio
    async def test_get_weather_success(self):
        """Test successful weather retrieval"""
        result = await ExampleTools.get_weather("London")
        assert "content" in result
        assert "Weather in London" in result["content"][0]["text"]
    
    @pytest.mark.asyncio
    async def test_get_weather_empty_city(self):
        """Test weather retrieval with empty city"""
        result = await ExampleTools.get_weather("")
        assert "Error" in result["content"][0]["text"]
    
    @pytest.mark.asyncio
    async def test_calculate_bmi_success(self):
        """Test successful BMI calculation"""
        result = await ExampleTools.calculate_bmi(70, 175)
        assert "content" in result
        assert "BMI" in result["content"][0]["text"]
    
    @pytest.mark.asyncio
    async def test_calculate_bmi_invalid_input(self):
        """Test BMI calculation with invalid input"""
        result = await ExampleTools.calculate_bmi(0, 175)
        assert "Error" in result["content"][0]["text"]
    
    @pytest.mark.asyncio
    async def test_text_analyzer_success(self):
        """Test successful text analysis"""
        test_text = "Hello world. This is a test!"
        result = await ExampleTools.text_analyzer(test_text)
        assert "content" in result
        assert "Word count" in result["content"][0]["text"]
    
    @pytest.mark.asyncio
    async def test_text_analyzer_empty_text(self):
        """Test text analysis with empty text"""
        result = await ExampleTools.text_analyzer("")
        assert "Error" in result["content"][0]["text"]