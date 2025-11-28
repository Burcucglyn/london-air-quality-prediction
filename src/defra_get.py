"""" I will be using defra_get.py to fetch DEFRa from the API endpoints defined in config.py.
1.Check london station list.
2.For each London station:
    -check avaible pollutants,
3. after I know the first, main fetching function for 2023/2024/19.11.2025 hourly data fetching.

base url here: https://uk-air.defra.gov.uk/sos-ukair/static/doc/api-doc/#stations
documentation of get capabilities: https://uk-air.defra.gov.uk/assets/documents/Example_SOS_queries_v1.3.pdf 
"""

from config import Config
import pandas as pd 
import requests
import json
import os
from pathlib import Path

class DefraGet:
    """Class to DEFRA UK-AIR data using (SOS)sensor observation services API fetching data.
    base defra_url: https://uk-air.defra.gov.uk/sos-ukair/api/v1
    SOS Standard Parameters:
    - service: SOS (required)
    - version: 2.0.0 (required)
    - request: GetCapabilities.
    """

    def __init__(self):
        """Initialize DefraGet with base URL with config instance."""
        self.config = Config()
        self.base_url = self.config.defra_url
        self.timeout = 30

    def get_capabilities(self, save_json=True):
        """ DEFRA  uses SOS standart, which is diffirent from LAQN order to fetch the data first I need to call capabilities first.
        get_capabilities pdf document:https://uk-air.defra.gov.uk/assets/documents/Example_SOS_queries_v1.3.pdf  
        So this function will shows all avaible stations, phenomena (pollutants), and producers.
        Args:
            save_jason : boolean response to JSON file.
        Returns: 
            dict: Capabilities response containing stations and phenomena.    
        """       
        #starting with url and setting the parameters.
        url = self.defra_url
        params = {
            'service': 'SOS',
            'version': '2.0.0',
            'request': 'GetCapabilities'
        }

        response = requests.get(url, params=params, timeout=self.timeout)

        if response.status_code != 200 or not response.text.strip():
            raise Exception(f"API request failed or returned empty response: {response.status_code}")
        
        try:
            data = response.json()
        except Exception as e:
            print("JSON decode error:", e)
            raise

        if save_json:
            output_dir = Path('data/defra/capabilities')
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / 'capabilities.json'

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Capabilities saved to: {output_file}")
        return data
    