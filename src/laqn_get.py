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

        # Save to CSV
        output_dir = os.path.join('data', 'laqn')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'sites_species_london.csv')
        df_sites_species.to_csv(output_path, index=False)
        return df_sites_species






