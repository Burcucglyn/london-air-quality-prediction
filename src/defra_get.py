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
        url = f"{Config.defra_url}/stations"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()  # define data from the response

        stations = data if isinstance(data, list) else data.get('stations', [])
        flattened = []
        for s in stations:
            flattened.append({
                "id": stations.get("id"),
                "name": stations.get("name"),
                "lat": stations.get("location", {}).get("lat"),
                "lon": stations.get("location", {}).get("lng"),
            })
        return flattened


            # Get station ID for species lookup.
            # Note: DEFRA uses 'id', 'stationId', or 'code' instead of LAQN's embedded structure
            station_id = station.get('id') or station.get('stationId') or station.get('code')
            
            if not station_id:
                continue
            
            # Fetch species for this station.
            # Note: DEFRA requires separate API call per station, LAQN includes species in initial response
            try:
                species_url = f"{self.config.defra_url}/stations/{station_id}/species"
                species_response = requests.get(species_url, timeout=self.timeout)
                
                if species_response.status_code == 200:
                    species_data = species_response.json()
                    
                    # Handle different response formats.
                    if isinstance(species_data, dict):
                        species_list = species_data.get('species', [])
                    elif isinstance(species_data, list):
                        species_list = species_data
                    else:
                        species_list = []
                    
                    if isinstance(species_list, dict):  # Handle single species object
                        species_list = [species_list]
                    
                    for species in species_list:
                        # Note: DEFRA may return species as strings or dicts, LAQN always returns dicts
                        if isinstance(species, str):
                            species_dict = {'species_code': species}
                        else:
                            species_dict = species
                        
                        flattened_data.append({**station_metadata, **species_dict})
                
            except Exception as e:
                print(f"Error fetching species for station {station_id}: {e}")
                continue

        # Create a DataFrame from the flattened data.
        df_sites_species = pd.DataFrame(flattened_data)

        return df_sites_species







