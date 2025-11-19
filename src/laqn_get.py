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
    
    def get_hourly_data(self, site_code, species_code, start_date, end_date, period="Hourly", units="Metric", step="1"):
        """Fetch hourly air quality data for a specific site and species within a date range."""
        # normalize dates to YYYY-MM-DD (API expects simple date strings)
        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')

        url = self.config.get_hourly_data.format(
            SITECODE=site_code,
            SPECIESCODE=species_code,
            STARTDATE=start_date,
            ENDDATE=end_date,
            PERIOD=period,
            UNITS=units,
            STEP=step
        )
        response = requests.get(url)
        print(f"[get_hourly_data] URL: {url} Status: {response.status_code}")
        if response.status_code != 200 or not response.text.strip():
            print(f"[get_hourly_data] Response text: {response.text[:1000]}")
            return pd.DataFrame()

        try:
            data = response.json()
        except Exception as e:
            print("JSON decode error:", e)
            raise

        # Extract the relevant data (assuming it's under 'Data' -> 'HourlyData')
        hourly_data = data.get('Data', {}).get('HourlyData') or data.get('HourlyData') or data.get('Data', {}).get('Series') or []
        if isinstance(hourly_data, dict):  # Handle single data object

            #single object, I will ttry to find list inside.
            hourly_items = hourly_data.get('Item') or hourly_data.get('Reading') or [hourly_data]
        elif isinstance(hourly_data, list):
            hourly_items = hourly_data
        else:
            hourly_items = []

        df_hourly = pd.DataFrame(hourly_items)

        # If empty, inform and return
        if df_hourly.empty:
            print(f"[get_hourly_data] No hourly measurements returned for {site_code}/{species_code} ({start_date} to {end_date}) - returning empty DataFrame.")
            return df_hourly

        # Ensure site/species codes present in the DF
        if '@SiteCode' not in df_hourly.columns:
            df_hourly['@SiteCode'] = site_code
        if '@SpeciesCode' not in df_hourly.columns:
            df_hourly['@SpeciesCode'] = species_code

        # Normalize measurement/value column: create '@Value' if a common name exists
        value_candidates = ['@Value', 'Value', 'value', 'Reading', 'reading', 'Measurement', 'measurement']
        if '@Value' not in df_hourly.columns:
            for c in value_candidates:
                if c in df_hourly.columns:
                    df_hourly['@Value'] = df_hourly[c]
                    break

        return df_hourly
       

    """I will use the site codes from  sites_species_london.csv to fetch the hourly data for each site and species.
    I will create a loop to iterate through each site code and species code to fetch the data"""
    def helper_fetch_hourly_data(self, start_date, end_date, period="Hourly", units="Metric", step="1",
                               save_dir=None, sleep_sec=1):
        """
        Read site/species pairs from data/laqn/sites_species_london.csv and fetch hourly data for each pair.
        Returns dict keyed by (site_code, species_code) with DataFrame values. Optionally saves CSVs.
        """
        # read site/species pairs describe the paths.
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'laqn', 'sites_species_london.csv')
        df_sites_species = pd.read_csv(csv_path, encoding='utf-8')

        # normalise measurement date columns and filter pairs that cover the requested window
        df_sites_species['@DateMeasurementStarted'] = pd.to_datetime(df_sites_species.get('@DateMeasurementStarted'), errors='coerce')
        df_sites_species['@DateMeasurementFinished'] = pd.to_datetime(df_sites_species.get('@DateMeasurementFinished'), errors='coerce')

        start_ts = pd.to_datetime(start_date)
        end_ts = pd.to_datetime(end_date)

        mask = (
            (df_sites_species['@DateMeasurementStarted'].fillna(pd.Timestamp.min) <= end_ts) &
            (
                df_sites_species['@DateMeasurementFinished'].isna() |
                (df_sites_species['@DateMeasurementFinished'] >= start_ts)
            )
        )
        df_filtered = df_sites_species.loc[mask].copy()
        pairs = df_filtered[['@SiteCode', '@SpeciesCode']].drop_duplicates()
        print(f"[helper_fetch_hourly_data] Filtering: {len(df_sites_species)} rows -> {len(pairs)} valid site/species pairs for {start_date} to {end_date}")

        required = {'@SiteCode', '@SpeciesCode'}
        if not required.issubset(df_sites_species.columns):
            raise ValueError(f"CSV missing required columns: {required - set(df_sites_species.columns)}")
        
        #pairs set to avoid duplicates.
        results = {} # dict to hold DataFrames keyed by (site_code, species_code), add to empty dict.

        # iterate through each unique site/species pair. if loop
        if save_dir:
            out_dir = os.path.join(os.path.dirname(__file__), '..', save_dir)
            os.makedirs(out_dir, exist_ok=True)
        else:
            out_dir = None
        
        for _, row in pairs.iterrows():
            site_code = row['@SiteCode']
            species_code = row['@SpeciesCode']
            try:
                df_hourly = self.get_hourly_data(
                    site_code=site_code,
                    species_code=species_code,
                    start_date=start_date,
                    end_date=end_date,
                    period=period,
                    units=units,
                    step=step
                )
            except Exception as e:
                print(f"[ERROR] {site_code} {species_code}: {e}")
                continue

            if df_hourly.empty:
                print(f"[helper_fetch_hourly_data] Empty result for {site_code}/{species_code} - skipping save.")
                results[(site_code, species_code)] = df_hourly
                time.sleep(sleep_sec)
                continue

            results[(site_code, species_code)] = df_hourly

            if out_dir is not None:
                fname = f"{site_code}_{species_code}_{start_date}_{end_date}.csv"
                df_hourly.to_csv(os.path.join(out_dir, fname), index=False)

            time.sleep(sleep_sec) # to avoid hitting rate limits
        return results




"""DateMeasurementFinished column has missing values, as next approach i can find the empty values so that means that the measurement still ongoing.
And can filter the site/species pairs that have measurement date range covering the requested start_date to end_date.
so that will be give me better chance to pair the site codes/specieas and measurument results accordingto date range."""