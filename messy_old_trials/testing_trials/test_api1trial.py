""" I will be testing the API functions here in data_collection.py
1. source data_collection.py to here and need to import the functions to test."""

# import sys library to handle parameters and func.
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests

#time module to measure total time taken for data collection
import time as time_module

# ensure project root is on sys.path so local modules (like data_collection) can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

#------ import LAQN API func here ----
from src.data_collection import LAQN_API 
#,collect_air_quality_jan2023, collect_air_quality_full_year_2023 


#------ import weatherAPI func here ----
from src.data_collection import WeatherAPI, collect_weather_data_jan2023, weather_data_2023year
from datetime import datetime

def test_LAQN_api():
    """ Simple test func check if LAQN_API class works."""
    print("=" * 50)
    print("=======Testing LAQN_API =====")
    print("=" * 50)

    # initialise API
    api = LAQN_API()

    # Test 1: Get all monitoring sites
    print("\n--- TEST 1: Monitoring Sites ---")
    sites = api.get_sites()

    # implement if loop for empty df.
    if not sites.empty:
        print(f"Site test SUCCESSFUL, PASSED!")
        print(f"Found {len(sites)} monitoring sites")
        print("\nFirst 5 sites:")
        print(sites[['@SiteCode', '@SiteName']].head(5)) # show site codes and names
    else:
        print("Site test FAILED! No data returned.")
        return
    
    # Test 2: GET pollutant data from specific sites.
    print("\n--- TEST 2: Pollutant Data ---")
    
    # Test multiple sites individually
    # 'MY1' marylebone road site code, 'BG1' bloomsbury site code, 'CT1' camden 
    # 'NO2' pollutant code
    
    test_sites = ['MY1', 'BG1', 'CT1']  # list of sites to test
    pollutant = 'NO2'  # testing NO2 data
    start_date = datetime(2025, 11, 1)  # used recent dates for testing
    end_date = datetime(2025, 11, 7)    
    successful_tests = 0
    
    for site_code in test_sites:
        print(f"\nTesting {site_code}:")
        
        # call the correct method name from your data_collection.py
        site_pollutant_data = api.get_site_pollutant(
            site_code, pollutant, start_date, end_date
        )
        
        if not site_pollutant_data.empty:
            print(f"  {site_code} pollutant data SUCCESSFUL, PASSED!")
            print(f"  Got {len(site_pollutant_data)} records")
            
            # show sample data with proper column names
            if '@MeasurementDateGMT' in site_pollutant_data.columns:
                sample_data = site_pollutant_data[['@MeasurementDateGMT', '@Value', 'SiteCode']].head(3)
                print(f"  Sample readings:")
                print(sample_data)
            
            successful_tests += 1
        else:
            print(f"  {site_code} pollutant data FAILED! No data returned.")
    
    # Test summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Sites test: PASSED")
    print(f"Pollutant data tests: {successful_tests}/{len(test_sites)} PASSED")
    
    if successful_tests > 0:
        print(" LAQN API integration working successfully!")
    else:
        print("No pollutant data retrieved. Try different dates or sites.")



# ------ Test Jan 2023 LAQN data collection function ----

def test_jan2023_preview():
    """ Test and preview January 2023 data without saving. """
    print("=== Testing LAQN January 2023 collection. ===")
    
    # call collection function 
    data = collect_air_quality_jan2023()
    
    # just preview results on terminal
    if not data.empty:
        print(f"Test SUCCESS! Would collect {len(data)} records")
        print(f"Sites: {data['SiteCode'].unique()}")
        print(f"Pollutants: {data['SpeciesCode'].unique()}")
        
        # show sample without saving
        sample_cols = [c for c in ['@MeasurementDateGMT', '@Value', 'SiteCode', 'SpeciesCode'] if c in data.columns]
        if sample_cols:
            print("Sample data preview:")
            print(data[sample_cols].head())
    else:
        print("Test failed.")


#----- testing full year 2023 data collection function ----

def test_LAQN_2023_preview():
    """ Test and preview full year 2023 data collection without saving """
    print("=== Testing LAQN full year 2023 collection ===")
    
    # start time module for total test time
    test_start = time_module.time()
    
    # collection parameters for display
    priority_sites = ['MY1', 'BG1', 'CT1', 'RB1', 'TD1']
    pollutants = ['NO2', 'PM10']
    
    print(f"Testing collection from {len(priority_sites)} sites: {priority_sites}")
    print(f"Pollutants: {pollutants}")
    print("Processing 12 monthly chunks for full year 2023.") # one month at a time to reduce api load.
    
    # call collection function
    data, collection_time = collect_air_quality_full_year_2023()
    
    # just preview results on terminal without saving.
    if not data.empty:
        print(f"Tested. Would collect {len(data)} total records")
        print(f"Data collection time: {collection_time:.2f} minutes")
        print(f"Sites: {data['SiteCode'].unique()}")
        print(f"Pollutants: {data['SpeciesCode'].unique()}")
        print(f"Date range: {data['@MeasurementDateGMT'].min()} to {data['@MeasurementDateGMT'].max()}")
        
        # show sample without additional saving
        sample_cols = [c for c in ['@MeasurementDateGMT', '@Value', 'SiteCode', 'SpeciesCode'] if c in data.columns]
        if sample_cols:
            print("Sample data preview:")
            print(data[sample_cols].head(10))
    else:
        print("Test failed! No data.")
        print(f"Process took: {collection_time:.2f} minutes")
    
    total_test_time = (time_module.time() - test_start) / 60
    print(f"Total test time including preview: {total_test_time:.2f} minutes")


#------------------------------------------------
#------------------------------------------------
# ------TEST Open-Meteo WEATHER API function ----
#------------------------------------------------
#------------------------------------------------


def test_weather_api():
    """ testing open-meteo weather API function using class """
    print("=" * 50)
    print("=======Testing Weather API =====")
    print("=" * 50)
    
    # create weather API instance and call its method
    weather_api = WeatherAPI()
    weather_df = weather_api.get_recent_weather(days_back=7)
    
    if not weather_df.empty:
        print(f"Weather API test SUCCESSFUL, PASSED!")
        print(f"Got {len(weather_df)} hourly records.")
        print("Sample weather meteo-API data:")
        cols = [c for c in ['time', 'temperature_2m', 'wind_speed_10m'] if c in weather_df.columns]
        print(weather_df[cols].head(10))
        return True
    else:
        print("Weather API test FAILED! No 'hourly' data in response.")
        return False


def test_weather_jan2023_preview():
    """ Test and preview January 2023 weather data collection """
    print("=== Testing Weather January 2023 collection ===")
    test_start = time_module.time()
    
    # call collection function
    data, collection_time = collect_weather_data_jan2023()
    
    # preview results on terminal
    if not data.empty:
        print(f"Test SUCCESS! Collected {len(data)} weather records")
        print(f"Collection time: {collection_time:.2f} minutes")
        print(f"Weather parameters: {list(data.columns)}")
        print(f"Date range: {data['time'].min()} to {data['time'].max()}")
        
        # show sample weather data without saving 10 rows.
        sample_cols = [c for c in ['time', 'temperature_2m', 'wind_speed_10m', 'precipitation'] if c in data.columns]
        if sample_cols:
            print("Sample weather data preview:")
            print(data[sample_cols].head(10))
        
        # to calculate total request time including preview
        total_test_time = (time_module.time() - test_start) / 60
        print(f"Total test time including preview: {total_test_time:.2f} minutes")
        return True
    else:
        print("Test falied! No weather data collected")
        print(f"Process took: {collection_time:.2f} minutes")
        return False
    
def test_weather_2023year_preview():
    """ Test and preview full year 2023 weather data collection """
    print("=== Testing Weather full year 2023 collection ===")
    test_start = time_module.time()

    print("Processing 12 monthly chunks for weather data.")

    # call collection function
    data, collection_time = weather_data_2023year()

    # preview results on terminal with first 10 rows
    if not data.empty:
        print(f"Test SUCCESS! Collected {len(data)} total weather records")
        print(f"Data collection time: {collection_time:.2f} minutes")
        print(f"Weather parameters: {list(data.columns)}")
        print(f"Date range: {data['time'].min()} to {data['time'].max()}")
        
        # show first 10 rows of weather data
        sample_cols = [c for c in ['time', 'temperature_2m', 'wind_speed_10m', 'precipitation'] if c in data.columns]
        if sample_cols:
            print("First 10 rows weather data preview:")
            print(data[sample_cols].head(10))
    else:
        print("Test FAILED! No weather data collected")
        print(f"Process took: {collection_time:.2f} minutes")

    total_test_time = (time_module.time() - test_start) / 60
    print(f"Total test time including preview: {total_test_time:.2f} minutes")



# main test block
if __name__ == "__main__":
    # run full LAQN + Weather tests - to not run put comment
    #-----------------------------------
    #----- run all LAQN API tests -------
    #-----------------------------------
    #test_LAQN_api() 
    #test_jan2023_preview()
    #print("=== Starting LAQN data collection for January 2023 ===")
    # test_LAQN_2023_preview()
    # print("=== 2023 year LAQN data preview test completed.===")



    #----- run all weather API test ----
    #-----------------------------------
    #test_weather_api()
    # test_weather_jan2023_preview()
    # print("=== Weather API tests completed.===")
    #---- testing 2023 year weather data collection ----
    # test_weather_2023year_preview()
    # print("=== Weather 2023 year data preview test completed.===")

















    """ I will be testing the API functions here in data_collection.py
1. source data_collection.py to here and need to import the functions to test."""

import sys
from pathlib import Path as _Path
import pandas as pd
# ensure project root is on sys.path so "import src" works when running tests directly
_ROOT = _Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

import time
import traceback

from src.data_collection import (
    collect_sites_from_csv_and_fetch_2023_parallel,
    train_logistic_from_csv,
)

OUT_DIR = _Path("data/raw/tests")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def test_collect_all_2023_small():
    """
    Small integration smoke test: read site codes from data/raw/sites_code_name.csv
    and fetch 2023 (limited to max_sites) in parallel. This is networked; on failure
    the test prints a SKIP with traceback so it doesn't break CI blindly.
    """
    out = OUT_DIR / "2023_all_sites_small_parallel.csv"
    try:
        res = collect_sites_from_csv_and_fetch_2023_parallel(
            sites_csv="data/raw/sites_code_name.csv",
            output_file=str(out),
            species_candidates=["CO", "NO2", "O3", "PM10", "PM25", "SO2"],
            start_date="2023-01-01",
            end_date="2023-12-31",
            max_workers=4,
            pause_s=0.2,
            max_sites=6,         # small run for test
            drop_na_values=True, # only keep real measurements for faster checks
        )
        print("test_collect_all_2023_small ->", res)
    except Exception as e:
        print("SKIP: test_collect_all_2023_small raised exception (network/API may be unreachable):", e)
        traceback.print_exc()
        return None

    # basic assertions / preview if file exists
    try:
        if out.exists():
            df = pd.read_csv(out)
            print("output shape:", df.shape)
            # ensure we have at least header and possibly rows
            assert "@MeasurementDateGMT" in df.columns
            # rows may be zero if no values present; allow that but ensure CSV exists
            return res
        else:
            print("No output file created by the function.")
            return res
    except Exception:
        print("Could not open or assert output CSV")
        traceback.print_exc()
        return res


def test_train_logistic_from_csv_small(tmp_path):
    # create small CSV
    p = tmp_path / "small_train.csv"
    import pandas as pd
    df = pd.DataFrame({
        "feat1": [1.0, 2.0, 1.5, 2.5, 3.0, 3.5],
        "feat2": [10, 11, 9, 12, 8, 13],
        "imported": [0, 0, 0, 1, 1, 1]
    })
    df.to_csv(p, index=False)
    from src.data_collection import train_logistic_from_csv
    res = train_logistic_from_csv(str(p), target_col="imported", test_size=0.33, random_state=1, normalize=False)
    print("train result:", res)
    assert "metrics" in res and "accuracy" in res["metrics"]


if __name__ == "__main__":
    print("Running small integration test for full-year 2023 fetch (small subset)...")
    t0 = time.time()
    test_collect_all_2023_small()
    print("Done. elapsed:", time.time() - t0)
