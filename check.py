import pandas as pd
import os
import requests 
from src.getData.laqn_get import laqnGet
from config import Config
import json
from dateutil.parser import isoparse
from pathlib import Path

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

# print("Test 3: CSV format")
# print("="*80)

# csv_url = f"https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/csv"


# print(f"Testing API URL:")
# print(f"URL: {csv_url}")
# print(f"\nSite: {site_code}")
# print(f"Species: {species_code}")
# print(f"Date range: {start_date} to {end_date}")

# try:
#     from io import StringIO
    
#     response = requests.get(csv_url, timeout=30)
#     print(f"\nResponse Status: {response.status_code}")
    
#     if response.status_code == 200:
#         print(f"Request code 200 that's good.")
#         print(f"\nResponse length: {len(response.text)} characters")
#         print(f"\nFirst 500 characters:")
#         print(response.text[:500])
        
#         df = pd.read_csv(StringIO(response.text))
#         print(f"\nDataFrame created.")
#         print(f"Shape: {df.shape}")
#         print(f"Columns: {df.columns.tolist()}")
#         print(f"\nFirst 5 rows:")
#         print(df.head())
#     else:
#         print(f"Request failed: {response.status_code}")
#         print(f"Response: {response.text[:500]}")
        
# except Exception as e:
#     print(f"Error occurred: {e}")

# # Build URL from Config
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
# print(f"Date: {start_date}")

# try:
#     # Make the request
#     response = requests.get(url, timeout=30)
#     print(f"\nResponse Status: {response.status_code}")
    
#     if response.status_code == 200:
#         print(f"Request code 200 that's good.")
        
#         # Parse JSON response
#         data = response.json()
#         print(f"\nJSON keys: {data.keys()}")
#         print(f"\nFirst 500 characters:")
#         print(str(data)[:500])
        
#         # Try to convert to DataFrame if data exists
#         if 'RawAQData' in data and 'Data' in data['RawAQData']:
#             df = pd.DataFrame(data['RawAQData']['Data'])
#             print(f"\DataFrame created.")
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
#     print(f"Error: {e}")


""" I need to check defra pollutants yearly."""
base_path = Path(__file__).parent
defra_base = base_path / 'data' / 'defra'

pollutants_by_year = {}

def load_station_pollutants():
    """Load pollutants from london_stations_clean.csv."""
    stations_file = defra_base / 'test' / 'london_stations_clean.csv'
    
    if not stations_file.exists():
        print(f"Station file not found: {stations_file}")
        return None
    
    print(f"Loading station data from: {stations_file}")
    df = pd.read_csv(stations_file)
    print(f"Loaded {len(df)} records.")
    print(f"Columns: {df.columns.tolist()}")
    
    if 'pollutant_available' not in df.columns:
        print("Column 'pollutant_available' not found in CSV.")
        return None
    
    unique_pollutants = df['pollutant_available'].unique()
    print(f"\nFound {len(unique_pollutants)} unique pollutants in station.")
    
    return sorted(unique_pollutants)

def scan_defra_directories():
    """Scan DEFRA measurement directories for pollutants."""
    pollutants_by_year = {}
    
    print("\n" + "="*80)
    print("DEFRA pollutants:")
    print("="*80)
    
    for year_dir in sorted(defra_base.glob('*measurements')):
        year = year_dir.name.replace('measurements', '')
        pollutants = set()
        file_count = 0
        
        print(f"\nScanning {year}measurements/")
        
        for station_dir in year_dir.glob('*'):
            if not station_dir.is_dir():
                continue
            
            for csv_file in station_dir.glob('*.csv'):
                parts = csv_file.stem.split('__')
                if len(parts) == 2:
                    pollutant = parts[0]
                    pollutants.add(pollutant)
                    file_count += 1
        
        pollutants_by_year[year] = sorted(pollutants)
        print(f"  Found {len(pollutants)} unique pollutants in {file_count} files.")
    
    return pollutants_by_year

def compare_pollutants(metadata_pollutants, directory_pollutants):
    """Compare pollutants from metadata vs directories."""
    print("\n" + "="*80)
    print("POLLUTANT COMPARISON")
    print("="*80)
    
    if metadata_pollutants is None:
        print("No metadata pollutants to compare.")
        return
    
    metadata_set = set(metadata_pollutants)
    all_dir_pollutants = set()
    
    for pollutants in directory_pollutants.values():
        all_dir_pollutants.update(pollutants)
    
    print(f"\nPollutants in metadata: {len(metadata_set)}")
    print(f"Pollutants in directories: {len(all_dir_pollutants)}")
    
    only_in_metadata = metadata_set - all_dir_pollutants
    only_in_directories = all_dir_pollutants - metadata_set
    common = metadata_set & all_dir_pollutants
    
    print(f"Common pollutants: {len(common)}")
    
    if only_in_metadata:
        print(f"\nOnly in metadata ({len(only_in_metadata)}):")
        for p in sorted(only_in_metadata):
            print(f"  - {p}")
    
    if only_in_directories:
        print(f"\nOnly in directories ({len(only_in_directories)}):")
        for p in sorted(only_in_directories):
            print(f"  - {p}")

def pollutant_mapping(metadata_pollutants, directory_pollutants):
    """Create pollutant mapping CSV from actual data."""
    
    all_pollutants = set()
    
    if metadata_pollutants:
        all_pollutants.update(metadata_pollutants)
    
    for pollutants in directory_pollutants.values():
        all_pollutants.update(pollutants)
    
    if not all_pollutants:
        print("\nNo pollutants found to create mapping.")
        return None
    
    mapping_data = []
    for pollutant in sorted(all_pollutants):
        mapping_data.append({
            'defra_code': pollutant,
            'found_in_metadata': pollutant in (metadata_pollutants or []),
            'found_in_2023': pollutant in directory_pollutants.get('2023', []),
            'found_in_2024': pollutant in directory_pollutants.get('2024', []),
            'found_in_2025': pollutant in directory_pollutants.get('2025', []),
            'chemical_formula': '',
            'category': '',
            'cas_number': '',
            'description': '',
            'health_impact': ''
        })
    
    df = pd.DataFrame(mapping_data)
    return df

def print_summary(pollutants_by_year):
    """Print detailed summary of pollutants by year."""
    print("\n" + "="*80)
    print("DEFRA POLLUTANT SUMMARY BY YEAR")
    print("="*80)
    
    for year in sorted(pollutants_by_year.keys()):
        print(f"\n{year} ({len(pollutants_by_year[year])} pollutants):")
        for i, pollutant in enumerate(pollutants_by_year[year], 1):
            print(f"  {i:2d}. {pollutant}")
    
    all_pollutants = set()
    for pollutants in pollutants_by_year.values():
        all_pollutants.update(pollutants)
    
    print("\n" + "="*80)
    print(f"TOTAL UNIQUE POLLUTANTS ACROSS ALL YEARS: {len(all_pollutants)}")
    print("="*80)
    for i, pollutant in enumerate(sorted(all_pollutants), 1):
        print(f"  {i:2d}. {pollutant}")
    
    if len(pollutants_by_year) > 1:
        common_pollutants = set(pollutants_by_year[list(pollutants_by_year.keys())[0]])
        for pollutants in pollutants_by_year.values():
            common_pollutants &= set(pollutants)
        
        print("\n" + "="*80)
        print(f"POLLUTANTS COMMON TO ALL YEARS: {len(common_pollutants)}")
        print("="*80)
        for i, pollutant in enumerate(sorted(common_pollutants), 1):
            print(f"  {i:2d}. {pollutant}")

def main():
    """Main execution function."""
    
    print("="*80)
    print("DEFRA POLLUTANT ANALYSIS")
    print("="*80)
    
    metadata_pollutants = load_station_pollutants()
    
    directory_pollutants = scan_defra_directories()
    
    compare_pollutants(metadata_pollutants, directory_pollutants)
    
    print_summary(directory_pollutants)
    
    mapping_df = pollutant_mapping(metadata_pollutants, directory_pollutants)
    
    if mapping_df is not None:
        output_path = defra_base / 'pollutant_mapping.csv'
        mapping_df.to_csv(output_path, index=False)
        
        print("\n" + "="*80)
        print("POLLUTANT MAPPING CSV CREATED")
        print("="*80)
        print(f"File saved to: {output_path}")
        print(f"Total pollutants: {len(mapping_df)}")
        print(f"\nColumns:")
        print(f"defra_code: Pollutant name as used in DEFRA files")
        print(f"found_in_metadata: Present in london_stations_clean.csv")
        print(f"found_in_2023/2024/2025: Present in measurement directories")
        print(f"chemical_formula: To be filled")
        
        print(f"\nSample data:")
        print(mapping_df[['defra_code', 'found_in_metadata', 'found_in_2023', 'found_in_2024', 'found_in_2025']].head(10).to_string())
        
        in_all_years = mapping_df[
            mapping_df['found_in_2023'] & 
            mapping_df['found_in_2024'] & 
            mapping_df['found_in_2025']
        ]
        print(f"\nPollutants in all three years: {len(in_all_years)}")


if __name__ == "__main__":
    main()