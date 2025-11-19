"""I will collect/get LAQN data from the API endpoints defined in config.py and will create functions for each endpoint to fetch the data.

1. get_monitor_sites: This function will fetch monitoring sites for a given group name with species information.
2. get_hourly_data: This function will fetch hourly air quality data for a specific site and species within a date range.
"""

#import statements below for necessary libraries to make API requests and handle data.
import requests
import json, csv, os

#config.py file importing Config class to access the API endpoint URLs.
from config import Config
import pandas as pd
# import response
import time # to handle rate limiting by adding delays between requests if necessary.
# iso date parsing import below.
from dateutil.parser import isoparse
import time


class laqnGet:
    """Class to keep get_groups, get_monitor_sites functions to under one roof."""

    def __init__(self):
        """Initialize the laqnGet class with Config instance."""
        self.config = Config()
    

    """Get_site_species url gave 400 bad request error. To understand the issure, I checked the API url on postman.
    Foound out that the data strucure nested inside sites key. So I modified the functions accordingly.
    {
    "Sites": {
        "Site": [
            {....
             }
    """
    def get_sites_species(self):
        """Fetch all monitoring sites and their species for London from the LAQN API."""
        url = self.config.get_sites_species.format(GROUPNAME="London")
        response = requests.get(url)

        if response.status_code != 200 or not response.text.strip():
            raise Exception(f"API request failed or returned empty response: {response.status_code}")

        try:
            data = response.json()
        except Exception as e:
            print("JSON decode error:", e)
            raise

        # Extract the list of monitoring sites. key:value pairs.
        sites = data.get('Sites', {}).get('Site', [])
        flattened_data = []

        # nested loop iterating site inside sites list.
        for site in sites:
            site_metadata = {key: value for key, value in site.items() if not isinstance(value, (list, dict))}
            species_data = site.get('Species', [])
            if isinstance(species_data, dict):  # Handle single species object
                species_data = [species_data]
            for species in species_data:
                flattened_data.append({**site_metadata, **species})

        # Create a DataFrame from the flattened data.
        df_sites_species = pd.DataFrame(flattened_data)

        # commented out saving to csv for testing purposes.
        # Save to CSV
        # output_dir = os.path.join('data', 'laqn')
        # os.makedirs(output_dir, exist_ok=True)
        # output_path = os.path.join(output_dir, 'sites_species_london.csv')
        # df_sites_species.to_csv(output_path, index=False)
        return df_sites_species
    
    def get_hourly_data(self, site_code, species_code, start_date, end_date):
        """Fetch hourly air quality data for a specific site and species within a date range."""
        # normalize dates to YYYY-MM-DD (API expects simple date strings)
        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')

        url = self.config.get_hourly_data.format(
            SITECODE=site_code,
            SPECIESCODE=species_code,
            STARTDATE=start_date,
            ENDDATE=end_date
        )
        response = requests.get(url, timeout=30)
        print(f"[get_hourly_data] URL: {url} Status: {response.status_code}")
        if response.status_code != 200 or not response.text.strip():
            print(f"[get_hourly_data] Response text: {response.text[:1000]}")
            return pd.DataFrame()
        

        try:
            data = response.json()
        except Exception as e:
            print(f"JSON decode error: {e}")
            return pd.DataFrame()

        # ERawAQData exsist in data dictionary, then check if Data key exists inside RawAQData, boolean true/true to proceed.
        if 'RawAQData' in data and 'Data' in data['RawAQData']:
             # result rawdata can be either a list of measurements or a single measurement dict.
            raw_data = data['RawAQData']['Data']
            

            if isinstance(raw_data, dict):
                raw_data = [raw_data]
            
            #create DataFrame from raw_data list of dicts.
            df_hourly = pd.DataFrame(raw_data)
            
            # Add site/species codes if not present
            if '@SiteCode' not in df_hourly.columns:
                df_hourly['@SiteCode'] = site_code
            if '@SpeciesCode' not in df_hourly.columns:
                df_hourly['@SpeciesCode'] = species_code
            
            return df_hourly
        else:
            print(f"[get_hourly_data] Unexpected response structure")
            return pd.DataFrame()
       

    """I will use the site codes from  actv_sites_species.csv.csv to fetch the hourly data for each site and species.
    I will create a loop to iterate through each site code and species code to fetch the data"""
    def helper_fetch_hourly_data(self, start_date, end_date, save_dir=None, sleep_sec=1):
        """
        Read site/species pairs from data/laqn/actv_sites_species.csv and fetch hourly data for each pair.
    
        Args:
            start_date (str): Start date in ISO format (e.g., "2023-01-01T00:00:00").
            end_date (str): End date in ISO format (e.g., "2023-01-08T23:59:59").
            save_dir (str, optional): Directory to save individual CSV files.
            sleep_sec (float): Sleep time between requests to avoid rate limiting.
            
        Returns:
            dict: Dictionary keyed by (site_code, species_code) with DataFrame values.
        """
        url = self.config.get_hourly_data
        #Convert dates to API format ISO, copy-pasted from check.py
        try:
            api_start_date = isoparse(start_date).strftime("%Y-%m-%d")
            api_end_date = isoparse(end_date).strftime("%Y-%m-%d")
        except Exception as e:
            raise ValueError(f"Data format ISO not working, check here: {e}")

        # read site/species pairs describe the paths.
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'laqn', 'actv_sites_species.csv')
        
        try:
            df_sites_species = pd.read_csv(csv_path, encoding='utf-8')
            print(f"loaded {len(df_sites_species)} rows from {csv_path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't find the file Burcu, try again +102390239480 time more maybe than: {csv_path}")
        except Exception as e:
                raise ValueError(f"I'm getting an error reading the CSV file Burcu, check here: {e}")

        # validate CSV read
        if df_sites_species.empty:
            raise ValueError("Stop being sloppy and fix the path, the file is not empty, impossible!")
        
        # took of the block of code to normalise @ prefix columns as the csv is already cleaned.
        required = {'SiteCode', 'SiteName', 'SpeciesCode', 'SpeciesName'}
        if not required.issubset(df_sites_species.columns):
            raise ValueError(f"CSV missing required columns: {required - set(df_sites_species.columns)}")
        
        # filter site/species pairs based on measurement dates overlapping with requested date range
        pairs = df_sites_species[['SiteCode', 'SpeciesCode']].drop_duplicates()
        total_pairs = len(pairs) # total site/species pairs number to use in progress tracking.
        print(f"Found {len(pairs)} unique site/species pairs to fetch data for {api_start_date} to {api_end_date}")

        results = {}# dict to hold DataFrames keyed by (site_code, species_code), add to empty dict.

        # iterate through each unique site/species pair. if loop
        if save_dir:
            out_dir = os.path.join(os.path.dirname(__file__), '..', save_dir)
            os.makedirs(out_dir, exist_ok=True)
            print(f"Will save CSVs to: {out_dir}")
        else:
            out_dir = None
        
        #changing tuple to progress count.
        for idx, (_, row) in enumerate(pairs.iterrows(), 1):
            site_code = row['SiteCode']
            species_code = row['SpeciesCode']
            try:
                #added formatting here to replace string placeholders on get_hourly_data url.
                formatted_url = url.format(
                    SITECODE=site_code,
                    SPECIESCODE=species_code,
                    STARTDATE=api_start_date,
                    ENDDATE=api_end_date,
                )

                #let's request the url here. hope it says 200ok.
                response = requests.get(formatted_url, timeout=30)

                if response.status_code ==200:
                    data = response.json()

                    #extract data from response.
                    if 'RawAQData' in data and 'Data' in data['RawAQData']:
                        raw_data = data['RawAQData']['Data']

                        #handle the single record case (dict instead of list) vs multiple records list.
                        if isinstance(raw_data, dict):
                            raw_data = [raw_data]
                        
                        #create dataframe
                        df_hourly = pd.DataFrame(raw_data)

                        if df_hourly.empty:
                            print(f"No data for this periofd {site_code}/{species_code} - skipping.")
                        else:
                            print(f"Retrieved {len(df_hourly)} records for {site_code}/{species_code}.")

                            #store in results 
                            results[(site_code, species_code)] = df_hourly

                            #save to csv if out_dir specified.
                            if out_dir is not None:
                                fname = f"{site_code}_{species_code}_{api_start_date}_{api_end_date}.csv"
                                df_hourly.to_csv(os.path.join(out_dir, fname), index=False)
                    else: 
                        print(f"Failed to response because of structure.")
                else:
                    print(f" HTTP {response.status_code}.")
            except requests.exceptions.Timeout:
                    print(f"Request timeout for site {site_code}, species {species_code}.")
            except Exception as e:
                print(f"Error fetching data, try again Burcu.")
        
            #adding sleep to avoid rate limiting.
            if idx < total_pairs:
                time.sleep(sleep_sec)
        print(f"\nComleted: {len(results)}/{total_pairs} fetched.")
        return results

            

"""I created new file actv_sitescsv from sites_species_london.csv to include only active monitoring sites in London.
And now I will swap the names in helper_fetch_hourly_data function to read from actv_sitescsv.csv instead of 
sites_species_london.csv. Test the function after modification on laqn_test.py, if this time data will be fetched properly."""

