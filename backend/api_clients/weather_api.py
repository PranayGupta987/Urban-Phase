"""
OpenWeather API Client
Fetches live weather data
"""
import os
import json
import requests
from typing import Dict, Any

# OpenWeather API endpoint
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Default city for weather data
DEFAULT_CITY = "Delhi"


def _load_mock_weather() -> Dict[str, Any]:
    """Load mock weather data"""
    return {
        "temp": 25.5,
        "humidity": 65,
        "description": "clear sky",
        "city": DEFAULT_CITY,
        "source": "mock"
    }


def fetch_live_weather() -> Dict[str, Any]:
    """
    Fetch live weather data from OpenWeather API
    
    Returns:
        JSON object with weather data (temp, humidity, description)
        Falls back to mock data on error
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        # No API key, use mock data
        return _load_mock_weather()
    
    try:
        params = {
            "q": DEFAULT_CITY,
            "appid": api_key,
            "units": "metric"  # Use Celsius
        }
        
        response = requests.get(
            OPENWEATHER_URL,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Extract relevant fields
        result = {
            "temp": weather_data.get("main", {}).get("temp"),
            "humidity": weather_data.get("main", {}).get("humidity"),
            "description": weather_data.get("weather", [{}])[0].get("description", "unknown"),
            "city": weather_data.get("name", DEFAULT_CITY),
            "source": "live"
        }
        
        # Validate that we got the required fields
        if result["temp"] is None or result["humidity"] is None:
            return _load_mock_weather()
        
        return result
        
    except requests.exceptions.Timeout:
        # Timeout - use mock data
        return _load_mock_weather()
    except requests.exceptions.RequestException as e:
        # Any other request error - use mock data
        return _load_mock_weather()
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        # Parsing error - use mock data
        return _load_mock_weather()
    except Exception as e:
        # Any other error - use mock data
        return _load_mock_weather()

