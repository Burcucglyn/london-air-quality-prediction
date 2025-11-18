"""I will collect/get LAQN data from the API endpoints defined in config.py and will create functions for each endpoint to fetch the data.

1. get_groups: This function will fetch the available monitoring groups. (groups name London)
2. get_monitor_sites: This function will fetch monitoring sites for a given group name.
3. get_hourly_data: This function will fetch hourly air quality data for a specific site and species within a date range.
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

    def get_groups(self):
        """Fetch the available monitoring groups from the LAQN API."""
        url = self.config.get_groups
        response = requests.get(url)

        if response.status_code != 200 or not response.text.strip():
            raise Exception(f"API request failed or returned empty response: {response.status_code}")

        try:
            data = response.json()
        except Exception as e:
            print("JSON decode error:", e)
            raise
        df = pd.DataFrame(data['Groups']['Group'])

    
            

    
