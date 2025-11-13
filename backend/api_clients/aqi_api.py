"""
OpenAQ Air Quality API Client
Fetches live AQI data with fallback to mock data
"""
import os
import json
import requests
from typing import Dict, Any, List

# OpenAQ API endpoint
OPENAQ_URL = "https://api.openaq.org/v2/latest"

# Default city for AQI data
DEFAULT_CITY = "Delhi"


def _load_mock_data() -> Dict[str, Any]:
    """Load mock AQI data from GeoJSON file"""
    mock_path = os.path.join(
        os.path.dirname(__file__), "..", "mock_data", "aqi.geojson"
    )
    
    # Fallback to data folder if mock_data doesn't exist
    if not os.path.exists(mock_path):
        mock_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "aqi.geojson"
        )
    
    if os.path.exists(mock_path):
        with open(mock_path, 'r') as f:
            return json.load(f)
    
    # Ultimate fallback
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-0.1278, 51.5074]
                },
                "properties": {
                    "pm25": 22.5,
                    "aqi": 65,
                    "category": "Moderate"
                }
            }
        ]
    }


def _get_aqi_category(pm25: float) -> str:
    """Convert PM2.5 value to AQI category"""
    if pm25 <= 12:
        return "Good"
    elif pm25 <= 35.4:
        return "Moderate"
    elif pm25 <= 55.4:
        return "Unhealthy for Sensitive Groups"
    elif pm25 <= 150.4:
        return "Unhealthy"
    elif pm25 <= 250.4:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def _convert_openaq_to_geojson(openaq_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert OpenAQ API response to GeoJSON format
    """
    features = []
    
    if "results" in openaq_data:
        for result in openaq_data["results"]:
            location = result.get("location", {})
            coordinates = location.get("coordinates", {})
            
            # Extract coordinates
            lon = coordinates.get("longitude")
            lat = coordinates.get("latitude")
            
            if lon is None or lat is None:
                continue
            
            # Extract PM2.5 value
            pm25 = None
            measurements = result.get("measurements", [])
            
            for measurement in measurements:
                if measurement.get("parameter") == "pm25":
                    pm25 = measurement.get("value")
                    break
            
            if pm25 is None:
                continue
            
            # Calculate AQI category
            category = _get_aqi_category(pm25)
            
            # Calculate AQI value (simplified - using PM2.5 as base)
            # AQI formula: AQI = ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low
            if pm25 <= 12:
                aqi = int((pm25 / 12) * 50)
            elif pm25 <= 35.4:
                aqi = int(50 + ((pm25 - 12) / (35.4 - 12)) * 50)
            elif pm25 <= 55.4:
                aqi = int(100 + ((pm25 - 35.4) / (55.4 - 35.4)) * 50)
            elif pm25 <= 150.4:
                aqi = int(150 + ((pm25 - 55.4) / (150.4 - 55.4)) * 50)
            elif pm25 <= 250.4:
                aqi = int(200 + ((pm25 - 150.4) / (250.4 - 150.4)) * 50)
            else:
                aqi = int(300 + ((pm25 - 250.4) / (350.4 - 250.4)) * 100)
            
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "coordinates": [lon, lat],
                    "pm25": round(pm25, 2),
                    "aqi": aqi,
                    "category": category,
                    "station": location.get("name", "Unknown Station")
                }
            })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


def fetch_live_aqi() -> Dict[str, Any]:
    """
    Fetch live AQI data from OpenAQ API
    
    Returns:
        GeoJSON FeatureCollection with AQI data
        Falls back to mock data on error
    """
    try:
        params = {
            "city": DEFAULT_CITY,
            "limit": 100
        }
        
        # OpenAQ doesn't require API key for free tier
        response = requests.get(
            OPENAQ_URL,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        
        openaq_data = response.json()
        
        # Convert to GeoJSON
        geojson_data = _convert_openaq_to_geojson(openaq_data)
        
        # If conversion resulted in empty features, use mock data
        if not geojson_data.get("features"):
            return _load_mock_data()
        
        return geojson_data
        
    except requests.exceptions.Timeout:
        # Timeout - use mock data
        return _load_mock_data()
    except requests.exceptions.RequestException as e:
        # Any other request error - use mock data
        return _load_mock_data()
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        # Parsing error - use mock data
        return _load_mock_data()
    except Exception as e:
        # Any other error - use mock data
        return _load_mock_data()

