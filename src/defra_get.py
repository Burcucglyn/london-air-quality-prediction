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
        self.capabilities_url = self.config.defra_capabilities_url 
        self.timeout = 30

    def post_capabilities(self, save_json=True):
        """ DEFRA uses SOS standard, which is different from LAQN. Order to fetch the data first I need to call capabilities first.
        get_capabilities pdf document:https://uk-air.defra.gov.uk/assets/documents/Example_SOS_queries_v1.3.pdf  
        post Capabilities JSON POST request using cURL curl -X POST -d "{\"request\": \"GetCapabilities\",\"service\":\"SOS\",\"version\":\"2.0.0\"}" https://uk-air.defra.gov.uk/sos-ukair/service/json"  
        So this function will show all available stations, phenomena (pollutants), and producers.
        Args:
            save_json : boolean response to JSON file.
        Returns: 
            dict: Capabilities response containing stations and phenomena.    
        """       
        # Use JSON endpoint with POST request
        url = self.capabilities_url
        
        # POST body with request parameters
        payload = {
            "request": "GetCapabilities",
            "service": "SOS",
            "version": "2.0.0"
        }

        print(f"Requesting: {url}")
        print(f"Payload: {payload}")

        # POST request with JSON payload
        response = requests.post(url, json=payload, timeout=self.timeout)

        print(f"Status code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")

        if response.status_code != 200 or not response.text.strip():
            raise Exception(f"API request failed or returned empty response: {response.status_code}")
        
        try:
            data = response.json()
        except Exception as e:
            print("Response text (first 500 chars):", response.text[:500])
            print("JSON decode error:", e)
            raise

        # Before parse  json to csv ensure output dir. 
        output_dir = Path('data/defra/capabilities')
        output_dir.mkdir(parents=True, exist_ok=True, encoding='utf-8')

        if save_csv:
            rows = self._capabilities_to_rows(data)
            csv_file = output_dir / 'capabilities.csv'
            df = pd.DataFrame(rows)
            pd.DataFrame(rows).to_csv(csv_file, index=False, encoding='utf-8')
            print(f"Capabilities CSV saved to: {csv_file}")


        #save json response.
        if save_json:
            output_file = output_dir / 'capabilities.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Capabilities saved to: {output_file}")
        return data
    
    def _capabilities_to_rows(self, data):
        """Helper function to parse capabilities JSON into rows for CSV.
        Args:
            data (dict): Capabilities JSON data.
        Returns:
            list: List of dict rows for CSV."""
        
        def norm_list(v):
            if v is None:
                return []
            return v if isinstance(v, list) else [v]

        def stringify(items):
            out = []
            for it in norm_list(items):
                if isinstance(it, dict):
                    out.append(
                        it.get('id')
                        or it.get('identifier')
                        or it.get('name')
                        or it.get('label')
                        or it.get('title')
                        or str(it)
                    )
                else:
                    out.append(str(it))
            return ';'.join([s for s in out if s])

        contents = data.get('contents') or {}
        offerings = (
            contents.get('offerings')
            or data.get('offerings')
            or []
        )

        rows = []
        for o in offerings:
            if not isinstance(o, dict):
                continue
            oid = o.get('id') or o.get('identifier') or o.get('name') or o.get('gml:id') or ''
            oname = o.get('name') or o.get('title') or o.get('label') or ''
            procedures = stringify(o.get('procedures') or o.get('procedure'))
            obs_props = stringify(o.get('observedProperties') or o.get('observedProperty') or o.get('phenomena'))
            fois = stringify(o.get('featureOfInterestIds') or o.get('featuresOfInterest') or o.get('featureOfInterest'))

            rows.append({
                'offering_id': oid,
                'offering_name': oname,
                'procedures': procedures,
                'observed_properties': obs_props,
                'features_of_interest': fois,
            })
        return rows
