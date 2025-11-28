"""" I will be using defra_get.py to fetch DEFRa from the API endpoints defined in config.py.
1.Check london station list.
2.For each London station:
    -check avaible pollutants,
3. after I know the first, main fetching function for 2023/2024/19.11.2025 hourly data fetching.

base url here: https://uk-air.defra.gov.uk/sos-ukair/static/doc/api-doc/#stations
"""

from config import Config
import pandas as pd 
import requests
import json

class DefraGet:
    """Class to DEFRA UK-AIR sensor observation services API fetching data.
    base defra_url: https://uk-air.defra.gov.uk/sos-ukair/api/v1
    Pollutant Codes Reference:
    -------------------------
    """

    def __init__(self):
        """Initialize DefraGet with base URL with config instance."""
        self.config = Config()
        self.base_url = self.config.defra_url
        self.timeout = 30
    
    def get_sites_species(self):
        """Fetch stations from DEFRA and return a flattened list."""
        url = f"{self.base_url}/stations"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        # Normalize to list
        if isinstance(data, list):
            stations = data
        elif isinstance(data, dict):
            stations = data.get("stations") or data.get("items") or data.get("data") or []
        else:
            stations = []

        flattened = []
        for s in stations:
            # Name fallbacks
            name = s.get("name") or s.get("label") or s.get("shortName") or s.get("stationName")

            # Coordinates from 'location'
            lat, lon = None, None
            loc = s.get("location") or {}
            if isinstance(loc, dict):
                lat = loc.get("lat") or loc.get("latitude")
                lon = loc.get("lon") or loc.get("lng") or loc.get("longitude")

            # Fallback: GeoJSON geometry
            if (lat is None or lon is None) and isinstance(s.get("geometry"), dict):
                coords = s["geometry"].get("coordinates")
                if isinstance(coords, (list, tuple)) and len(coords) >= 2:
                    lon, lat = coords[0], coords[1]

            flattened.append({
                "id": s.get("id") or s.get("identifier") or s.get("code"),
                "name": name,
                "lat": lat,
                "lon": lon,
            })
        return flattened