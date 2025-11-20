import pandas as pd
import os
import requests 
from src.laqn_get import laqnGet
from config import Config
import json
from dateutil.parser import isoparse

# df = pd.read_csv("data/laqn/sites_species_london.csv", parse_dates=['@DateMeasurementStarted','@DateMeasurementFinished'])
# print(df['@DateMeasurementStarted'].min(), df['@DateMeasurementStarted'].max())
# print(df['@DateMeasurementFinished'].min(), df['@DateMeasurementFinished'].max())

# g = laqnGet()
# print(g.get_hourly_data("TD0", "NO2", "2023-01-01", "2023-01-07").head())


# csv_path = 'data/laqn/actv_sites_species.csv'
# print(f"Looking for CSV at: {os.path.abspath(csv_path)}")
# print(f"File exists: {os.path.exists(csv_path)}")

# # Try to read through the CSV and print some info
# try:
#     df = pd.read_csv(csv_path)
#     print(f"CSV loaded: {len(df)} rows")
#     print(f"Columns: {df.columns.tolist()}")
#     print(f"First row: {df.iloc[0].to_dict()}")
# except Exception as e:
#     print(f"Error reading CSV: {e}")



# Test parameters
site_code = "BG1"
species_code = "NO2"
start_date_iso = "2023-01-01T00:00:00"
end_date_iso = "2023-01-02T23:59:59"

# Convert ISO to API format (YYYY-MM-DD)
start_date = isoparse(start_date_iso).strftime("%Y-%m-%d")
end_date = isoparse(end_date_iso).strftime("%Y-%m-%d")

print(f"Date conversion:")
print(f"ISO format: {start_date_iso} -> API format: {start_date}")
print(f"ISO format: {end_date_iso} -> API format: {end_date}")


#first without period/unit/step parameters

# print("Test 1: URL with Period/Units/Step parameters")
# print("="*80)

# url = Config.get_hourly_data.format(
#     SITECODE=site_code,
#     SPECIESCODE=species_code,
#     STARTDATE=start_date,
#     ENDDATE=end_date,
#     PERIOD="hour",
#     UNITS="ugm3",
#     STEP="1"
# )

# print(f"Testing API URL:")
# print(f"URL: {url}")
# print(f"\nSite: {site_code}")
# print(f"Species: {species_code}")
# print(f"Date range: {start_date} to {end_date}")

# try:
#     response = requests.get(url, timeout=30)
#     print(f"\nResponse Status: {response.status_code}")
    
#     if response.status_code == 200:
#         print(f"Request code 200 that's good.")
        
#         data = response.json()
#         print(f"\nJSON keys: {data.keys()}")
#         print(f"\nFirst 500 characters:")
#         print(str(data)[:500])
        
#         if 'RawAQData' in data and 'Data' in data['RawAQData']:
#             df = pd.DataFrame(data['RawAQData']['Data'])
#             print(f"\nDataFrame created.")
#             print(f"Shape: {df.shape}")
#             print(f"Columns: {df.columns.tolist()}")
#             print(f"\nFirst 5 rows:")
#             print(df.head())
#         else:
#             print("\nNo data in expected structure")
#             print(f"Full response: {data}")
#     else:
#         print(f"Request failed: {response.status_code}")
#         print(f"Response: {response.text[:500]}")
        
# except Exception as e:
#     print(f"Error occurred: {e}")


# #second test without period/unit/step parameters

# print("Test 2: URL without Period/Units/Step parameters")
# print("="*80)

# simple_url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"

# print(f"Testing API URL:")
# print(f"URL: {simple_url}")
# print(f"\nSite: {site_code}")
# print(f"Species: {species_code}")
# print(f"Date range: {start_date} to {end_date}")

# try:
#     response = requests.get(simple_url, timeout=30)
#     print(f"\nResponse Status: {response.status_code}")
    
#     if response.status_code == 200:
#         print(f"Request code 200 that's good.")
        
#         data = response.json()
#         print(f"\nJSON keys: {data.keys()}")
#         print(f"\nFirst 500 characters:")
#         print(str(data)[:500])
        
#         if 'RawAQData' in data and 'Data' in data['RawAQData']:
#             df = pd.DataFrame(data['RawAQData']['Data'])
#             print(f"\nDataFrame created.")
#             print(f"Shape: {df.shape}")
#             print(f"Columns: {df.columns.tolist()}")
#             print(f"\nFirst 5 rows:")
#             print(df.head())
#         else:
#             print("\nNo data in expected structure")
#             print(f"Full response: {data}")
#     else:
#         print(f"Request failed: {response.status_code}")
#         print(f"Response: {response.text[:500]}")
        
# except Exception as e:
#     print(f"Error occurred: {e}")


# #third test csv format

print("Test 3: CSV format")
print("="*80)

csv_url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/csv"


print(f"Testing API URL:")
print(f"URL: {csv_url}")
print(f"\nSite: {site_code}")
print(f"Species: {species_code}")
print(f"Date range: {start_date} to {end_date}")

try:
    from io import StringIO
    
    response = requests.get(csv_url, timeout=30)
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"Request code 200 that's good.")
        print(f"\nResponse length: {len(response.text)} characters")
        print(f"\nFirst 500 characters:")
        print(response.text[:500])
        
        df = pd.read_csv(StringIO(response.text))
        print(f"\nDataFrame created.")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"\nFirst 5 rows:")
        print(df.head())
    else:
        print(f"Request failed: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"Error occurred: {e}")

# Build URL from Config
url = Config.get_hourly_data.format(
    SITECODE=site_code,
    SPECIESCODE=species_code,
    STARTDATE=start_date,
    ENDDATE=end_date,
    PERIOD="hour",
    UNITS="ugm3",
    STEP="1"
)

print(f"Testing API URL:")
print(f"URL: {url}")
print(f"\nSite: {site_code}")
print(f"Species: {species_code}")
print(f"Date: {start_date}")

try:
    # Make the request
    response = requests.get(url, timeout=30)
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"Request code 200 that's good.")
        
        # Parse JSON response
        data = response.json()
        print(f"\nJSON keys: {data.keys()}")
        print(f"\nFirst 500 characters:")
        print(str(data)[:500])
        
        # Try to convert to DataFrame if data exists
        if 'RawAQData' in data and 'Data' in data['RawAQData']:
            df = pd.DataFrame(data['RawAQData']['Data'])
            print(f"\DataFrame created.")
            print(f"Shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"\nFirst 5 rows:")
            print(df.head())
        else:
            print("\nNo data in expected structure")
            print(f"Full response: {data}")
    else:
        print(f"Request failed: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"Error: {e}")


