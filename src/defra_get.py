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
        self.rest_base_url = self.config.defra_url

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
    
    """3. Step:
    I have fetch post capabilities to see available stations and pollutants on DEFRa UK-AIR API.
    Also fetched EU Air Quality pollutant vocabulary to map pollutant URIs to codes and names.
    Capabilities csv and json file's not necessarly showing station codes either coordinates.
    DEFRA SOS method gives 'DescribeSensor' method to get station details according to json file. 
    As next step I will be implementing DEFRA DescribeSensor method to get station details including
    coordinates."""

    def describe_sensor(self, procedure_uri: str) -> Dict[str, Any]:
        """Get station metadata usin DescribeSensor request.
        Fetches sensor description for a given procedure URI using DescribeSensor SOS method.
        Args:
            procedure_uri (str): The procedure URI of the sensor/station."""
        
        # using json endpoint for describe sensor
        url= self.capabilities_url

        payload = {
            "request": "DescribeSensor",
            "service": "SOS",
            "version": "2.0.0",
            "procedure": procedure_uri,
            "procedureDescriptionFormat": "http://www.opengis.net/sensorml/2.0"
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"error fetching DescribeSensor for {procedure_uri}: {e}")
            return {} 

    """4. Step: adding REST API method to fetch defra's data, it has clean and simple REST API endpoint.
    has buuilt in station coordinates.
    Documentation: https://uk-air.defra.gov.uk/sos-ukair/static/doc/api-doc/#stations  
    here is the url: https://uk-air.defra.gov.uk/sos-ukair/api/v1.
    what it gives:
        Get All Stations:
            GET /api/v1/stations

            Returns stations with:
                            Station ID
                            Station name
                            Coordinates (latitude/longitude)
                            Bounding box for filtering
        Filter Stations by Location
            GET /api/v1/stations?bbox={"ll":{"type":"Point","coordinates":[-0.5,51.3]},"ur":{"type":"Point","coordinates":[0.3,51.7]}}
        This gets only London stations using bounding box.

        Get Timeseries Data
            GET /api/v1/timeseries/{id}/getData
            Returns hourly pollution measurements.
    """

    def get_london_stations(self, save_csv: bool = True) -> pd.DataFrame:
        """Get only London stations with their pollutants (timeseries) in one call.
        
        Uses bounding box filter to fetch ONLY London data from API.
        Returns DataFrame ready for analysis.
        
        Returns:
            pd.DataFrame: London stations with coordinates and available pollutants.
        """
 
        
        # London bounding box
        min_lon, min_lat, max_lon, max_lat = self.config.london_bbox

        # adding bbox parameter for API (uses GeoJSON Point format)
        
        url = f"{self.rest_base_url}/stations"
        params = { "expanded": "true" }
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            stations = response.json()
            
            if not stations or not isinstance(stations, list):
                print("No stations returned")
                return pd.DataFrame()
            
            # Flatten nested JSON into DataFrame rows
            rows = []
            for station in stations:
                if not isinstance(station, dict):
                    continue
                
                # Extract station metadata
                properties = station.get('properties', {})
                station_id = properties.get('id', '')
                station_name = properties.get('label', '')
                
                # Extract coordinates
                geom = station.get('geometry', {})
                coords = geom.get('coordinates', [])

                if len(coords) < 2:
                    continue

                lat = coords[0]  # First coordinate is latitude
                lon = coords[1]  # Second coordinate is longitude

                # Filter to London bounding box
                if not (min_lon <= lon <= max_lon and min_lat <= lat <= max_lat):
                    continue
                
                # Extract timeseries (pollutants) disc.
                timeseries = properties.get('timeseries', {})
                
                # Extract timeseries (pollutants)
                timeseries = station.get('properties', {}).get('timeseries', [])
                
                if not timeseries or not isinstance(timeseries, dict):
                    # Station with no pollutants - still include it
                    rows.append({
                        'station_id': station_id,
                        'station_name': station_name,
                        'latitude': lat,
                        'longitude': lon,
                        'timeseries_id': None,
                        'pollutant': None
                    })
                else:
                    # Iterate over dict items (key is timeseries_id)
                    for ts_id, ts_data in timeseries.items():
                        if isinstance(ts_data, dict):
                            # Extract pollutant name from offering label
                            offering_label = ts_data.get('offering', {}).get('label', '')
                            
                            rows.append({
                                'station_id': station_id,
                                'station_name': station_name,
                                'latitude': lat,
                                'longitude': lon,
                                'timeseries_id': ts_id,
                                'pollutant': offering_label
                            })
            
            df = pd.DataFrame(rows)
            
            print(f"Found {df['station_id'].nunique()} London stations with {len(df)} pollutant measurements.")
            
            if save_csv:
                output_dir = Path('data/defra')
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / 'london_stations_pollutants.csv'
                df.to_csv(output_file, index=False, encoding='utf-8')
                print(f"Saved to: {output_file}.")
            
            return df
            
        except Exception as e:
            print(f"Error fetching London stations: {e}")
            return pd.DataFrame()
    
        
    def get_timeseries_data (self, timeseries_id: str, timespan: str=None) -> Dict[str,Any]:
        """ Function for get pollution measurements for a timeseries.
        args:
            timeseries_id: the timeseries identifier.
            timespan: ISO formatted period 
        returns:
                dict: json response with measurement values and timestamp.    """
        
        url = f"{self.rest_base_url}/timeseries/{timeseries_id}/getData"
        params = {}
        if timespan:
            params["timespan"] = timespan
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
           
            #parse the values from response
            values = data.get('values', [])
            if not values:
                return pd.DataFrame()
            
            df = pd.DataFrame(values)
            df['timeseries_id'] = timeseries_id
            return df

        except Exception as e:
            print(f"Error fetching data for timeseries {timeseries_id}: {e}")
            return pd.DataFrame()
    


"""2. STEP: Fetch and parse EU Air Quality pollutant vocabulary.
Downloads pollutant definitions from EU EEA (European Environment Agency)
and creates a mapping CSV for decoding pollutant URIs.
"""

class euAirPollutantVocab:
    """Class to fetch and parse EU Air Quality pollutant vocabulary."""
    def __init__(self):
        cfg = Config() #I hit unboundLocalError without this line.
        self.base_url = Config.eu_pollutant_vocab_url
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
    
    def process_vocab(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean the vocabulary data.
        
        Args:
            df: Raw DataFrame from CSV
            
        Returns:
            Cleaned DataFrame with standard columns
        """
        if df.empty:
            return df
        
        # Normalise column names (strip spaces)
        df_norm = df.rename(columns=lambda c: str(c).strip())

        # Build cleaned DataFrame with safe defaults.
        df_clean = pd.DataFrame()
        df_clean['uri'] = df['URI']
        df_clean['uri_code'] = df['URI'].apply(self.extract_uri_code)
        df_clean['pollutant_name'] = df['Label']
        df_clean['pollutant_code'] = df['Notation']
        df_clean['definition'] = df['Definition']
        df_clean['status'] = df['Status']
        
        # Remove rows with missing essential data
        initial_count = len(df_clean)
        df_clean = df_clean.dropna(subset=['uri_code', 'pollutant_code'])
        df_clean = df_clean[df_clean['uri_code'] != '']
        
        removed = initial_count - len(df_clean)
        if removed > 0:
            print(f"  Removed {removed} rows with missing data")

        return df_clean
    
    def save_vocab(self, df: pd.DataFrame, output_path: str = 'data/defra/pollutant_mapping.csv') -> None:
        """Saves the processed vocabulary DataFrame to CSV.
        
        Args:
            df: Processed DataFrame.
            output_path: Path to save CSV.
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Vocabulary saved to: {output_file}")

