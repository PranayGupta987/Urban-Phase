"""
LTA DataMall Traffic API Client for Singapore
Fetches live traffic data with fallback to mock data

Requirements:
- Use v4 TrafficSpeedBands endpoint:
  https://datamall2.mytransport.sg/ltaodataservice/v4/TrafficSpeedBands
- Add header: {"AccountKey": <env>, "accept": "application/json"}
- Return valid GeoJSON FeatureCollection with LineString geometries and
  properties: segment_id, speed, vehicle_count, congestion_level.
"""
import os
import json
import requests
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# LTA DataMall API endpoint (v4)
LTA_TRAFFIC_SPEED_URL = "https://datamall2.mytransport.sg/ltaodataservice/v4/TrafficSpeedBands"

LTA_ACCOUNT_KEY_ENV = "LTA_ACCOUNT_KEY"

def _load_mock_data() -> Dict[str, Any]:
    """
    Load mock traffic data - guaranteed valid GeoJSON around Singapore.

    NOTE: We intentionally ignore any existing traffic.geojson files which
    might contain London data and always return freshly generated segments
    around Singapore CBD.
    """
    logger.info("Using synthetic mock traffic data around Singapore")
    return _create_default_traffic_geojson()

def _create_default_traffic_geojson() -> Dict[str, Any]:
    """
    Create default valid GeoJSON for Singapore.

    Generates 15 synthetic segments around [103.851959, 1.290270].
    """
    base_lon = 103.851959
    base_lat = 1.290270

    features: List[Dict[str, Any]] = []
    for i in range(15):
        lon_offset = (i % 5) * 0.001
        lat_offset = (i // 5) * 0.001

        coordinates = [
            [base_lon + lon_offset, base_lat + lat_offset],
            [base_lon + lon_offset + 0.0007, base_lat + lat_offset + 0.0004],
            [base_lon + lon_offset + 0.0014, base_lat + lat_offset + 0.0008],
        ]

        # Simple speed & congestion pattern
        if i % 3 == 0:
            speed = 60.0
            congestion = "low"
            congestion_level = 0.2
            vehicle_count = 80
        elif i % 3 == 1:
            speed = 40.0
            congestion = "moderate"
            congestion_level = 0.5
            vehicle_count = 130
        else:
            speed = 20.0
            congestion = "high"
            congestion_level = 0.8
            vehicle_count = 220

        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates,
                },
                "properties": {
                    "segment_id": i + 1,
                    "speed": speed,
                    "avg_speed": speed,
                    "congestion": congestion,
                    "congestion_level": congestion_level,
                    "vehicle_count": vehicle_count,
                    "volume": vehicle_count,
                    "source": "mock",
                },
            }
        )

    return {"type": "FeatureCollection", "features": features}


def _parse_geom_linestring(geom: str) -> List[List[float]]:
    """
    Parse LTA 'Geom' (WKT LINESTRING) into list of [lon, lat] coordinates.

    Example:
      "LINESTRING (103.851959 1.29027, 103.8525 1.291, ...)"
    """
    try:
        geom = geom.strip()
        if not geom.upper().startswith("LINESTRING"):
            return []

        start = geom.find("(")
        end = geom.rfind(")")
        if start == -1 or end == -1 or end <= start:
            return []

        coords_str = geom[start + 1 : end]
        coord_pairs = coords_str.split(",")
        coords: List[List[float]] = []
        for pair in coord_pairs:
            parts = pair.strip().split()
            if len(parts) != 2:
                continue
            lon = float(parts[0])
            lat = float(parts[1])
            coords.append([lon, lat])
        return coords
    except Exception as e:
        logger.error(f"Error parsing Geom LINESTRING: {e}", exc_info=True)
        return []

def _convert_lta_to_geojson(lta_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert LTA DataMall response to GeoJSON.

    We prioritise the 'Geom' WKT for real geometries. If missing or invalid,
    we fall back to synthetic coordinates around Singapore.
    """
    features: List[Dict[str, Any]] = []

    records = lta_data.get("value") or lta_data.get("Value") or []

    for idx, item in enumerate(records[:50]):  # limit for performance
        try:
            link_id = item.get("LinkID", idx + 1)
            speed_band = int(item.get("SpeedBand", 3))

            # v4 includes Geom
            geom = item.get("Geom") or item.get("Geometry")
            coords = _parse_geom_linestring(geom) if geom else []

            # If Geom was unusable, generate synthetic coordinates
            if len(coords) < 2:
                base_lon = 103.851959 + ((idx % 5) * 0.001)
                base_lat = 1.290270 + ((idx // 5) * 0.001)
                coords = [
                    [base_lon, base_lat],
                    [base_lon + 0.001, base_lat + 0.0005],
                    [base_lon + 0.002, base_lat + 0.0010],
                ]

            speed = max(10.0, min(80.0, float(speed_band) * 10.0))

            if speed < 20:
                congestion = "high"
                congestion_level = 0.8
            elif speed < 40:
                congestion = "moderate"
                congestion_level = 0.5
            else:
                congestion = "low"
                congestion_level = 0.2

            vehicle_count = max(50, min(300, int(250 - speed * 1.5)))

            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords,
                    },
                    "properties": {
                        "segment_id": int(link_id) if str(link_id).isdigit() else idx + 1,
                        "link_id": link_id,
                        "speed": float(speed),
                        "avg_speed": float(speed),
                        "congestion": congestion,
                        "congestion_level": float(congestion_level),
                        "vehicle_count": int(vehicle_count),
                        "volume": int(vehicle_count),
                        "source": "lta_live",
                    },
                }
            )
        except Exception as e:
            logger.warning(f"Error converting LTA record to feature: {e}", exc_info=True)
            continue

    if not features:
        logger.warning("No usable LTA traffic records; falling back to mock data")
        return _create_default_traffic_geojson()

    return {"type": "FeatureCollection", "features": features}

def fetch_live_traffic() -> Dict[str, Any]:
    """
    Fetch live traffic data from LTA DataMall v4.

    Always returns a valid GeoJSON FeatureCollection with LineString geometries
    and properties including: segment_id, speed, vehicle_count, congestion_level.
    """
    api_key = os.getenv(LTA_ACCOUNT_KEY_ENV)

    if not api_key:
        logger.warning("LTA_ACCOUNT_KEY not set; using mock traffic data")
        return _load_mock_data()

    try:
        headers = {
            "AccountKey": api_key,
            "accept": "application/json",
        }

        logger.info("Requesting live traffic data from LTA v4 TrafficSpeedBands")
        response = requests.get(
            LTA_TRAFFIC_SPEED_URL,
            headers=headers,
            timeout=10,
        )

        if response.status_code != 200:
            logger.error(
                f"LTA API error {response.status_code}: {response.text[:500]}"
            )
            return _load_mock_data()

        lta_data = response.json()
        geojson_data = _convert_lta_to_geojson(lta_data)

        features = geojson_data.get("features", [])
        logger.info(f"Traffic API returning {len(features)} features")

        if not features:
            logger.warning("LTA response contained no features; using mock traffic data")
            return _load_mock_data()

        return geojson_data

    except Exception as e:
        logger.error(f"Error fetching LTA traffic data: {e}", exc_info=True)
        return _load_mock_data()
