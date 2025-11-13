"""
HERE Maps Traffic API Client
Fetches live traffic data with fallback to mock data
"""
import os
import json
import requests
from typing import Dict, Any

# HERE Maps Traffic API endpoint
HERE_TRAFFIC_URL = "https://traffic.ls.hereapi.com/traffic/6.3/flow.json"

# Hardcoded bounding box for a small city (Delhi, India)
# Format: minLat,minLon,maxLat,maxLon
DEFAULT_BBOX = "28.4,77.0,28.7,77.3"


def _load_mock_data() -> Dict[str, Any]:
    """Load mock traffic data from GeoJSON file"""
    mock_path = os.path.join(
        os.path.dirname(__file__), "..", "mock_data", "traffic.geojson"
    )
    
    # Fallback to data folder if mock_data doesn't exist
    if not os.path.exists(mock_path):
        mock_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "traffic.geojson"
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
                    "type": "LineString",
                    "coordinates": [[-0.1278, 51.5074], [-0.1268, 51.5084]]
                },
                "properties": {
                    "speed": 25,
                    "congestion": "moderate"
                }
            }
        ]
    }


def _convert_here_to_geojson(here_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert HERE Maps traffic response to simplified GeoJSON format
    """
    features = []
    
    if "RWS" in here_data:
        for rw in here_data["RWS"]:
            if "RW" in rw:
                for road in rw["RW"]:
                    if "FIS" in road:
                        for flow_item in road["FIS"]:
                            if "FI" in flow_item:
                                for flow in flow_item["FI"]:
                                    # Extract geometry (SHP - shape points)
                                    coordinates = []
                                    if "SHP" in flow:
                                        for shp in flow["SHP"]:
                                            if "value" in shp:
                                                # HERE returns coordinates as "lat,lon"
                                                coords = shp["value"].split(",")
                                                if len(coords) == 2:
                                                    # GeoJSON uses [lon, lat]
                                                    coordinates.append([
                                                        float(coords[1]),
                                                        float(coords[0])
                                                    ])
                                    
                                    # Extract traffic properties
                                    speed = None
                                    congestion = "unknown"
                                    
                                    if "CF" in flow:
                                        for cf in flow["CF"]:
                                            if "SU" in cf:
                                                speed = cf["SU"].get("SU", None)
                                            if "JF" in cf:
                                                jf = cf["JF"]
                                                # Convert jam factor to congestion level
                                                if jf < 0.3:
                                                    congestion = "low"
                                                elif jf < 0.7:
                                                    congestion = "moderate"
                                                else:
                                                    congestion = "high"
                                    
                                    if coordinates and len(coordinates) >= 2:
                                        features.append({
                                            "type": "Feature",
                                            "geometry": {
                                                "type": "LineString",
                                                "coordinates": coordinates
                                            },
                                            "properties": {
                                                "speed": speed,
                                                "congestion": congestion
                                            }
                                        })
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


def fetch_live_traffic() -> Dict[str, Any]:
    """
    Fetch live traffic data from HERE Maps API
    
    Returns:
        GeoJSON FeatureCollection with traffic data
        Falls back to mock data on error
    """
    api_key = os.getenv("HERE_API_KEY")
    
    if not api_key:
        # No API key, use mock data
        return _load_mock_data()
    
    try:
        params = {
            "apiKey": api_key,
            "bbox": DEFAULT_BBOX,
            "responseattributes": "shp"
        }
        
        response = requests.get(
            HERE_TRAFFIC_URL,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        
        here_data = response.json()
        
        # Convert to GeoJSON
        geojson_data = _convert_here_to_geojson(here_data)
        
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

