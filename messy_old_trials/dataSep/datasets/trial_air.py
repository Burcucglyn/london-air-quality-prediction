""" Fetching and processing air quality data for London."""

import pandas as pd
from pathlib import Path
import requests
import multiprocessing as mp
import time
import json

"""Explore API data before saving it.
LondonAir/API open data source provides air quality data for various pollutants.
"""

#def func for exploring API data explore_api_lad. 

def explore_api_lad(SITECODE, SPECIESCODE, STARTDATE, ENDDATE, PERIOD, UNITS, STEP):
    """ created function to explore API data for seeing London's air quality data pollutants with time range."""
    """ This returns raw data based on 'SiteCode', 'SpeciesCode', 'StartDate', 'EndDate'. Default time period is 'hourly'. Data returned in JSON format"""
    url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={SITECODE}/SpeciesCode={SPECIESCODE}/StartDate={STARTDATE}/EndDate={ENDDATE}/Period={PERIOD}/Units={UNITS}/Step={STEP}/Json"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Had an error fetching data for {SITECODE} {SPECIESCODE} from {STARTDATE} to {ENDDATE}. Status code: {response.status_code}")
        return None
    
SITECODE = "TH2" # Site code for Mile End. found in londonair.org.uk and downloaded csv 
SPECIESCODE = "NO2" # List of pollutants to fetch data for
STARTDATE = "2025-01-01"
ENDDATE = "2025-02-25"
PERIOD = "Hourly"
UNITS = "ugm-3" #API unit for micrograms per cubic meter
STEP = "1"

def lad_api_info():
    """ Fetches and saves the API terms and conditions PDF."""
    url = f"https://api.erg.ic.ac.uk/AirQuality/Information/Terms/pdf"

    response = requests.get(url)
    if response.status_code == 200:
        with open("lad_api_info.pdf", "wb") as f:
            f.write(response.content)
        print("API information saved to lad_api_info.pdf")
    else:
        print(f"Had an error fetching API information. Status code: {response.status_code}")

if __name__ == "__main__":
#    lad_api_info() # Uncomment to fetch API information
    result = explore_api_lad(SITECODE, SPECIESCODE, STARTDATE, ENDDATE, PERIOD, UNITS, STEP)
    if result:
        print("Mile End Air Quality Data fetched.")
        
        # Extract the actual data from the nested JSON
        observations = result["RawAQData"]["Data"]
        
        # Create DataFrame from the observations
        df = pd.DataFrame(observations)
        
        print("Number of records:", len(df))
        print("Columns:", list(df.columns))
        print(df)
    else:
        print("Failed to fetch Mile End Air Quality Data")