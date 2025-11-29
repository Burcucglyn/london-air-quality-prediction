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
from typing import Dict, List, Any
from io import StringIO #csv reading from response text.(string)

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
        self.capabilities_url = self.config.defra_capabilities_url 
        self.timeout = 30

    def post_capabilities(self, save_json: bool = True, save_csv: bool = True) -> Dict[str, Any]:
        """ DEFRA uses SOS standard, which is different from LAQN. Order to fetch the data first I need to call capabilities first.
        get_capabilities pdf document:https://uk-air.defra.gov.uk/assets/documents/Example_SOS_queries_v1.3.pdf  
        post Capabilities JSON POST request using cURL curl -X POST -d "{\"request\": \"GetCapabilities\",\"service\":\"SOS\",\"version\":\"2.0.0\"}" https://uk-air.defra.gov.uk/sos-ukair/service/json"  
        So this function will show all available stations, phenomena (pollutants), and producers.
        Args:
            save_json (bool): Save raw JSON response.
            save_csv (bool): Save flattened CSV derived from JSON.
        Returns:
            dict: Capabilities response containing stations and phenomena.
        """
        # Use JSON endpoint with POST request
        url = self.capabilities_url
        payload = {"request": "GetCapabilities", "service": "SOS", "version": "2.0.0"}

        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()

        data = response.json()  # expected JSON from /service/json

        output_dir = Path('data/defra/capabilities')
        output_dir.mkdir(parents=True, exist_ok=True)

        # commented out CSV and JSON save below for now to speed up testing.
        if save_csv:
            rows = self._capabilities_to_rows(data)
            csv_file = output_dir / 'capabilities.csv'
            pd.DataFrame(rows).to_csv(csv_file, index=False, encoding='utf-8')
            print(f"Capabilities CSV saved to: {csv_file}")

        if save_json:
            json_file = output_dir / 'capabilities.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Capabilities JSON saved to: {json_file}")

        return data
    
    def _capabilities_to_rows(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Helper function to parse capabilities JSON into rows for CSV.
        Args:
            data (dict): Capabilities JSON data.
        Returns:
            list: List of dict rows for CSV."""
        
        contents = data.get('contents', {})

        if isinstance(contents, dict):
            offerings = contents.get('observationOfferings', [])
        elif isinstance(contents, list):
            offerings = contents
        else:
            offerings = data.get('observationOfferings', [])

        rows = []

        for o in offerings:
            if not isinstance(o, dict):
                continue
            # Extract relevant fields
            identifier =o.get('identifier', '')
            name = o.get('name', '')

            #extract procedures, observed properties, features of interest.
            procedure_list = o.get('procedure', [])
            procedure = procedure_list[0] if procedure_list else ''

            obs_prop_list = o.get('observableProperty', [])
            observable_property = ';'.join(obs_prop_list) if obs_prop_list else ''

            # Extract time range (phenomenonTime is a list with [start, end])
            phenom_time = o.get('phenomenonTime', [])
            start_time = phenom_time[0] if len(phenom_time) > 0 else ''
            end_time = phenom_time[1] if len(phenom_time) > 1 else ''
            
            # Extract result time (when data was last updated)
            result_time = o.get('resultTime', [])
            result_start = result_time[0] if len(result_time) > 0 else ''
            result_end = result_time[1] if len(result_time) > 1 else ''



            rows.append({
                'offering_id': identifier,
                'offering_name': name,
                'procedure': procedure,
                'observable_property': observable_property,
                'phenomenon_time_start': start_time,
                'phenomenon_time_end': end_time,
                'result_time_start': result_start,
                'result_time_end': result_end,
            })
        return rows
    

"""2. STEP: Fetch and parse EU Air Quality pollutant vocabulary.

Downloads pollutant definitions from EU EEA (European Environment Agency)
and creates a mapping CSV for decoding pollutant URIs.
"""

class euAirPollutantVocab:
    """Class to fetch and parse EU Air Quality pollutant vocabulary."""
    def __init__(self):
        base_url = Config.eu_pollutant_vocab_url
        self.timeout = 30

    #check the url on postman and url returns csv, so I will fetch it as csv directly.
    def fetch_vocab(self) -> pd.DataFrame:
        """Fetches the pollutant vocabulary CSV and returns as DataFrame.
        Returns:
            DataFrame with all pollutants.
        """

        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()

            # Read CSV directly from response text.
            df = pd.read_csv(StringIO(response.text))

            return df
        
        except Exception as e:
            print(f"Error fetching pollutant vocabulary: {e}")
            return pd.DataFrame()
        
    def extract_uri_code(self, uri: str) -> str:
        """The function for extracting pollutant code from  Uniform Resource Identifier (URI).
        DEFRA uses URIs for pollutants in their data. so this function will be extracting pollutant code from URI and return their uri code and name.
        Extracts pollutant code from URI.
        Args:
            uri (str): Pollutant URI.
        Returns:
            str: Extracted pollutant code.
        """
        if pd.isna(uri) or not isinstance(uri, str):
            return ''
        return uri.split('/')[-1]  # Get last part after '/'
        

