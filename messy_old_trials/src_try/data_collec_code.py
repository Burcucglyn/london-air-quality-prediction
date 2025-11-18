"""
LAQN API Data Collection Functions - Complete Package
Includes all collection functions, API fixes, and site creation
"""

from pathlib import Path
import logging
import asyncio
import random
import math
from datetime import datetime, timedelta
from threading import Thread
import threading
import time
from time import perf_counter
import concurrent.futures
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, urljoin
import csv
import pandas as pd
import requests
import aiohttp
from tqdm import tqdm
from io import StringIO
import json
import os

logger = logging.getLogger(__name__)


def create_sites_csv():
    """Read sites data from existing CSV file or create fallback if not found"""
    
    # Multiple possible paths to try
    possible_paths = [
        "/Users/burdzhuchaglayan/Desktop/data science projects/air-pollution-levels/data/raw-2trr/sites.csv",
        "data/raw-2trr/sites.csv",
        "data/raw/sites.csv",
        "../data/raw-2trr/sites.csv"
    ]
    
    for user_sites_path in possible_paths:
        try:
            if os.path.exists(user_sites_path):
                print(f"Found and reading sites from: {user_sites_path}")
                sites_df = pd.read_csv(user_sites_path)
                
                # Ensure the output directory exists
                Path('data/raw').mkdir(parents=True, exist_ok=True)
                
                # Copy to expected location for collection functions
                output_file = 'data/raw/sites_code_name.csv'
                sites_df.to_csv(output_file, index=False)
                
                print(f"Successfully loaded {len(sites_df)} sites from your file")
                print(f"Available columns: {list(sites_df.columns)}")
                
                # Show first few sites
                if len(sites_df) > 0:
                    print("First few sites:")
                    for i in range(min(3, len(sites_df))):
                        row = sites_df.iloc[i]
                        site_code = row.iloc[0] if len(row) > 0 else 'Unknown'
                        site_name = row.iloc[1] if len(row) > 1 else 'Unknown'
                        print(f"  {site_code}: {site_name}")
                
                return output_file, sites_df
                
        except Exception as e:
            print(f"Could not read from {user_sites_path}: {e}")
            continue
    
    print("Could not find your sites.csv file in any expected location")
    print("Creating a comprehensive London sites list...")
    
    # Enhanced sites list with more London monitoring sites
    sites_data = {
        '@SiteCode': [
            'BL0', 'MY1', 'CT2', 'TD0', 'BG3', 'LW2', 'CD1', 'EA8', 'TH4', 'CR8',
            'BX1', 'HV1', 'KC1', 'RB4', 'WM5', 'ST5', 'HG4', 'IS6', 'EN1', 'HR1',
            'WA2', 'BR2', 'KF1', 'LD2', 'NM3', 'CW1', 'BN1', 'HF4', 'SU6', 'TW1',
            'LH0', 'GN0', 'GR4', 'HS1', 'MW1', 'NK1', 'RK1', 'WL1', 'ER1', 'GN3'
        ],
        '@SiteName': [
            'Bloomsbury', 'Marylebone Road', 'City Road', 'Tower Bridge', 'Brent Greenwich', 
            'Lambert', 'Camden Roadside', 'Ealing Horn Lane', 'Thames', 'Croydon',
            'Bexley', 'Havering', 'Kensington Chelsea', 'Redbridge', 'Westminster',
            'Southwark', 'Haringey', 'Islington', 'Enfield', 'Harrow',
            'Wandsworth', 'Bromley', 'Kingston', 'Lambeth', 'Newham', 
            'City of London', 'Barnet', 'Hammersmith Fulham', 'Sutton', 'Tower Hamlets',
            'Lewisham', 'Greenwich', 'Greenwich 4', 'Hounslow', 'Merton', 'North Kensington',
            'Richmond', 'Waltham Forest', 'Erith', 'Greenwich 3'
        ],
        '@SiteType': ['Urban Background'] * 40,
        '@LocalAuthorityName': ['London'] * 40,
        '@Latitude': [51.52 + (i * 0.01) for i in range(40)],
        '@Longitude': [-0.13 + (i * 0.01) for i in range(40)],
        '@DateOpened': ['1993-01-01'] * 40,
        '@DateClosed': [''] * 40
    }
    
    df = pd.DataFrame(sites_data)
    
    # Create data directory if it doesn't exist
    Path('data/raw').mkdir(parents=True, exist_ok=True)
    
    # Save to the expected location
    output_file = 'data/raw/sites_code_name.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Created comprehensive sites file: {output_file}")
    print(f"Contains {len(df)} London monitoring sites")
    
    return output_file, df



"""Here I define a function for collecting 2023 LAQN site informations for connected boroughts in London
the headers of the csv dataset I want to create are below:
@LocalAuthorityCode,@LocalAuthorityName,@SiteCode,@SiteName,@SiteType,@DateClosed,
@DateOpened,@Latitude,@Longitude,@LatitudeWGS84,@LongitudeWGS84,@DisplayOffsetX,
@DisplayOffsetY,@DataOwner,@DataManager,@SiteLink
I will be using this ds for doing readings according to the site's in londan and fetch 2023
all data in the future"""
def collect_2023_london_data(output_file="london_2023_data.csv", max_sites=None):
    """
    Specialized function to collect 2023 London air quality data with actual values
    Focuses on getting measurement data that actually contains values
    """
    
    print("Starting 2023 London air quality data collection...")
    
    # Ensure sites file exists
    sites_file, sites_df = create_sites_csv()
    
    # Target species - the 6 main pollutants
    target_species = ['NO2', 'O3', 'PM10', 'PM25', 'SO2', 'CO']
    
    # Get site codes
    site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
    all_site_codes = sites_df[site_col].astype(str).tolist()
    
    if max_sites:
        all_site_codes = all_site_codes[:max_sites]
    
    print(f"Targeting {len(all_site_codes)} sites and {len(target_species)} species")
    print(f"Sites: {all_site_codes[:10]}..." if len(all_site_codes) > 10 else f"Sites: {all_site_codes}")
    print(f"Species: {target_species}")
    
    # Try multiple date ranges through 2023
    date_ranges = [
        ("01 Jan 2023", "31 Jan 2023"),   # January
        ("01 Feb 2023", "28 Feb 2023"),   # February  
        ("01 Mar 2023", "31 Mar 2023"),   # March
        ("01 Apr 2023", "30 Apr 2023"),   # April
        ("01 May 2023", "31 May 2023"),   # May
        ("01 Jun 2023", "30 Jun 2023"),   # June
        ("01 Jul 2023", "31 Jul 2023"),   # July
        ("01 Aug 2023", "31 Aug 2023"),   # August
        ("01 Sep 2023", "30 Sep 2023"),   # September
        ("01 Oct 2023", "31 Oct 2023"),   # October
        ("01 Nov 2023", "30 Nov 2023"),   # November
        ("01 Dec 2023", "31 Dec 2023"),   # December
    ]
    
    api = LAQN_API()
    all_records = []
    successful_collections = 0
    failed_collections = 0
    
    print(f"\nCollecting data for 2023...")
    
    for month_idx, (start_date, end_date) in enumerate(date_ranges, 1):
        print(f"\nMonth {month_idx}/12: {start_date} to {end_date}")
        month_records = []
        
        for site_code in all_site_codes:
            for species_code in target_species:
                
                try:
                    # Try the improved robust collection
                    records = api.get_data_robust(site_code, species_code, start_date, end_date)
                    
                    if records:
                        # Filter records that have actual measurement values
                        valid_records = [r for r in records if r.get('@Value') and str(r.get('@Value')).strip() not in ['', 'nan', 'None']]
                        
                        if valid_records:
                            month_records.extend(valid_records)
                            successful_collections += 1
                            print(f"  {site_code}/{species_code}: {len(valid_records)} records")
                        else:
                            failed_collections += 1
                    else:
                        failed_collections += 1
                        
                except Exception as e:
                    failed_collections += 1
                    print(f"  {site_code}/{species_code}: Error - {str(e)[:50]}")
                
                time.sleep(0.1)  # Rate limiting
        
        print(f"Month {month_idx} collected: {len(month_records)} records")
        all_records.extend(month_records)
        
        # Save progress periodically
        if month_idx % 3 == 0:  # Save every 3 months
            if all_records:
                temp_df = pd.DataFrame(all_records)
                temp_file = f"temp_2023_data_q{month_idx//3}.csv"
                temp_df.to_csv(temp_file, index=False)
                print(f"Saved progress: {temp_file} ({len(all_records)} total records)")
    
    # Final results
    print(f"\nCollection completed!")
    print(f"Successful requests: {successful_collections}")
    print(f"Failed requests: {failed_collections}")
    print(f"Total records with values: {len(all_records)}")
    
    if all_records:
        # Create final DataFrame
        df = pd.DataFrame(all_records)
        
        # Data quality report
        print(f"\nData quality summary:")
        print(f"Total records: {len(df)}")
        print(f"Unique sites: {df['@SiteCode'].nunique()}")
        print(f"Unique species: {df['@SpeciesCode'].nunique()}")
        
        if '@MeasurementDateGMT' in df.columns:
            df['@MeasurementDateGMT'] = pd.to_datetime(df['@MeasurementDateGMT'], errors='coerce')
            date_range = f"{df['@MeasurementDateGMT'].min()} to {df['@MeasurementDateGMT'].max()}"
            print(f"Date range: {date_range}")
        
        # Value statistics
        if '@Value' in df.columns:
            numeric_values = pd.to_numeric(df['@Value'], errors='coerce')
            valid_values = numeric_values.dropna()
            print(f"Numeric values: {len(valid_values)}/{len(df)} ({100*len(valid_values)/len(df):.1f}%)")
            if len(valid_values) > 0:
                print(f"Value range: {valid_values.min():.2f} to {valid_values.max():.2f}")
        
        # Save final file
        df.to_csv(output_file, index=False)
        print(f"\nSaved final data: {output_file}")
        
        return {
            "out_file": output_file,
            "rows": len(all_records),
            "successful": successful_collections,
            "failed": failed_collections,
            "sites": df['@SiteCode'].nunique() if '@SiteCode' in df.columns else 0,
            "species": df['@SpeciesCode'].nunique() if '@SpeciesCode' in df.columns else 0
        }
    
    else:
        print("\nNo data with values collected.")
        return {
            "out_file": None,
            "rows": 0,
            "successful": 0,
            "failed": failed_collections,
            "error": "No measurement values found in API responses"
        }


def collect_2023_quarterly(output_prefix="2023_quarterly", concurrency=10):
    """
    Collect 2023 data in quarterly chunks with better error handling
    """
    
    print("Collecting 2023 data in quarterly chunks...")
    
    quarterly_chunks = [
        ("2023-01-01", "2023-03-31", "Q1"),
        ("2023-04-01", "2023-06-30", "Q2"), 
        ("2023-07-01", "2023-09-30", "Q3"),
        ("2023-10-01", "2023-12-31", "Q4")
    ]
    
    results = []
    total_rows = 0
    
    for start_date, end_date, quarter in quarterly_chunks:
        print(f"\nCollecting {quarter}: {start_date} to {end_date}")
        
        result = collect_year_async_chunk(
            year=2023,
            output_file=f"{output_prefix}_{quarter}.csv",
            species=['NO2', 'O3', 'PM10', 'PM25', 'SO2', 'CO'],
            concurrency=concurrency,
            start_date=start_date,
            end_date=end_date
        )
        
        result.update({"quarter": quarter, "start": start_date, "end": end_date})
        results.append(result)
        total_rows += result.get("rows", 0)
        
        print(f"{quarter} completed: {result.get('rows', 0)} rows")
    
    # Create summary
    summary_df = pd.DataFrame(results)
    summary_file = f"{output_prefix}_summary.csv"
    summary_df.to_csv(summary_file, index=False)
    
    print(f"\nQuarterly collection completed:")
    print(f"Total rows across all quarters: {total_rows}")
    print(f"Summary saved: {summary_file}")
    
    return {
        "quarters": results,
        "total_rows": total_rows,
        "summary_file": summary_file
    }


class LAQN_API:
    """Enhanced LAQN API client with robust error handling and multiple endpoint support"""
    base_url = "https://api.erg.ic.ac.uk/AirQuality/"

    def __init__(self, timeout=60, max_retries=5):
        # Session with improved retry/backoff for unreliable API
        sess = requests.Session()
        sess.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Increased timeout and retries for this slow API
        self.timeout = timeout
        
        try:
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            
            # More aggressive retry strategy for unreliable API
            retry = Retry(
                total=max_retries,
                backoff_factor=1.0,  # Increased backoff 
                status_forcelist=[429, 500, 502, 503, 504, 520, 521, 522, 523, 524],
                allowed_methods=["GET", "POST"],
                raise_on_status=False  # Don't raise exceptions immediately
            )
            adapter = HTTPAdapter(max_retries=retry)
            sess.mount("https://", adapter)
            sess.mount("http://", adapter)
        except Exception:
            pass
            
        self.session = sess
        self.lock = threading.Lock()

    def test_connectivity(self):
        """Test if we can reach the API"""
        try:
            url = f"{self.base_url}Information/Species/Json"
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except Exception:
            return False
        

    '''Fetches the list of monitoring sites from the LAQN API and saves it to a CSV file.'''
    def get_sites(self) -> pd.DataFrame:
        """Fetch all monitoring sites with multiple endpoint attempts"""
        endpoints = [
            "Information/MonitoringSites/GroupName=London/Json",
            "Information/MonitoringSites/Json",
            "Information/MonitoringSites/GroupName=All/Json"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                resp = self.session.get(url, timeout=self.timeout)
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    # Try different JSON structures
                    sites = None
                    if 'Sites' in data and 'Site' in data['Sites']:
                        sites = data['Sites']['Site']
                    elif 'Site' in data:
                        sites = data['Site']
                    elif isinstance(data, list):
                        sites = data
                    
                    if sites:
                        df = pd.json_normalize(sites)
                        return df
                        
            except Exception:
                continue
                
        return pd.DataFrame()

    def get_data_robust(self, site_code, species_code, start_date, end_date):
        """Get data with multiple format attempts"""
        
        endpoints = [
            f"Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json",
            f"Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/csv",
            f"Data/Site/SiteCode={site_code}/StartDate={start_date}/EndDate={end_date}/Json"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, timeout=self.timeout)
                
                if response.status_code == 200:
                    
                    # Try JSON first
                    if 'Json' in endpoint:
                        try:
                            data = response.json()
                            return self._parse_json_data(data, site_code, species_code)
                        except:
                            continue
                    
                    # Try CSV
                    elif 'csv' in endpoint:
                        try:
                            return self._parse_csv_data(response.text, site_code, species_code)
                        except:
                            continue
                            
            except Exception:
                continue
        
        return []
    
    def _parse_json_data(self, data, site_code, species_code):
        """Parse JSON response into records"""
        records = []
        
        if isinstance(data, dict):
            data_list = None
            for key in ['RawAQData', 'Data', 'HourlyAQData', 'Values', 'Measurements']:
                if key in data:
                    data_list = data[key]
                    break
            
            if isinstance(data_list, dict) and 'Data' in data_list:
                data_list = data_list['Data']
            
            if isinstance(data_list, list):
                for item in data_list:
                    record = self._extract_record(item, site_code, species_code)
                    if record:
                        records.append(record)
        
        return records
    
    def _parse_csv_data(self, text, site_code, species_code):
        """Parse CSV response into records"""
        records = []
        
        try:
            if not text.strip() or 'html' in text.lower()[:100]:
                return []
            
            df = pd.read_csv(StringIO(text))
            
            if len(df) > 0:
                for _, row in df.iterrows():
                    record = self._extract_record(row.to_dict(), site_code, species_code)
                    if record:
                        records.append(record)
            
        except Exception:
            pass
            
        return records
    
    def _extract_record(self, item, default_site_code, default_species_code):
        """Extract a standardized record from various data formats"""
        
        if hasattr(item, 'get'):
            get_func = item.get
        else:
            get_func = lambda k, default: item.get(k, default) if k in item else default
        
        # Try different field name variations
        measurement_date = (
            get_func('@MeasurementDateGMT', '') or
            get_func('MeasurementDateGMT', '') or
            get_func('DateTime', '') or
            get_func('Date', '') or
            get_func('Timestamp', '')
        )
        
        value = (
            get_func('@Value', '') or
            get_func('Value', '') or
            get_func('Concentration', '') or
            get_func('Reading', '')
        )
        
        site_code = (
            get_func('@SiteCode', default_site_code) or
            get_func('SiteCode', default_site_code) or
            default_site_code
        )
        
        species_code = (
            get_func('@SpeciesCode', default_species_code) or
            get_func('SpeciesCode', default_species_code) or
            get_func('Species', default_species_code) or
            default_species_code
        )
        
        # Only return record if we have a valid timestamp and value
        if measurement_date and str(value).strip() and str(value) not in ['', 'nan', 'None']:
            return {
                '@MeasurementDateGMT': measurement_date,
                '@LocalAuthorityName': get_func('@LocalAuthorityName', ''),
                '@SiteCode': site_code,
                '@SiteName': get_func('@SiteName', ''),
                '@SiteType': get_func('@SiteType', ''),
                '@SpeciesCode': species_code,
                '@Value': value,
                '@DateClosed': get_func('@DateClosed', ''),
                '@DateOpened': get_func('@DateOpened', ''),
                '@Latitude': get_func('@Latitude', ''),
                '@Longitude': get_func('@Longitude', '')
            }
        
        return None
    """ Fetches the list of pollutants (species) from the LAQN API."""
    def get_pollutants(self) -> pd.DataFrame:
        """Fetch pollutant/species list with robust JSON parsing"""
        url = f"{self.base_url}Information/Species/Json"
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()

            species_list = None
            if isinstance(data, dict):
                if 'Species' in data and isinstance(data['Species'], dict) and 'Species' in data['Species']:
                    species_list = data['Species']['Species']

            if species_list is None and isinstance(data, dict):
                for key in ('Species', 'Data', 'RawData', 'RawAQData', 'Items', 'ItemList', 'SpeciesList'):
                    v = data.get(key)
                    if isinstance(v, list):
                        species_list = v
                        break
                    if isinstance(v, dict) and 'Species' in v and isinstance(v['Species'], list):
                        species_list = v['Species']
                        break

            def _find_first_list(obj):
                if isinstance(obj, list):
                    return obj
                if isinstance(obj, dict):
                    for val in obj.values():
                        res = _find_first_list(val)
                        if res:
                            return res
                return None

            if species_list is None:
                species_list = _find_first_list(data)

            if not species_list:
                return pd.DataFrame()

            df = pd.json_normalize(species_list)
            return df
            
        except Exception:
            return pd.DataFrame()

    def get_site_species(self) -> pd.DataFrame:
        """Fetch site-species combinations using JSON endpoint"""
        try:
            url = urljoin(self.base_url, "Information/MonitoringSiteSpecies/GroupName=London/Json")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            if 'Sites' in data and 'Site' in data['Sites']:
                df = pd.json_normalize(data['Sites']['Site'])
                return df
            else:
                return pd.DataFrame()
                
        except Exception:
            return pd.DataFrame()


def collect_working_combinations(output_file="london_jan2023_data.csv"):
    """Collect data for proven working site-species combinations"""
    # Proven working combinations from testing
    working_sites = {
        'BL0': ['NO2', 'O3', 'PM10', 'PM25', 'SO2'],
        'LW2': ['NO2', 'O3', 'PM10'], 
        'CT2': ['CO', 'NO2', 'PM10'],
        'MY1': ['CO', 'NO2', 'PM10', 'PM25'],
        'CD1': ['CO', 'NO2', 'PM10']
    }
    
    # Prepare collection parameters
    site_codes = list(working_sites.keys())
    all_species = []
    for species_list in working_sites.values():
        all_species.extend(species_list)
    unique_species = list(set(all_species))
    
    # Collect using proven combinations
    result = get_hourly_7days_fixed(
        site_codes=site_codes,
        start_date="2023-01-01", 
        end_date="2023-01-31",  # Full January
        species=unique_species,
        output_file=output_file
    )
    
    return result


def collect_weekly_sample(output_file="london_weekly_sample.csv"):
    """Collect small weekly sample for testing"""
    # Use proven working sites
    working_sites = ['BL0', 'MY1', 'CT2']
    working_species = ['NO2', 'PM10', 'CO']
    
    result = get_hourly_7days_fixed(
        site_codes=working_sites,
        start_date="2023-01-01",
        end_date="2023-01-08", 
        species=working_species,
        output_file=output_file
    )
    
    return result


def get_hourly_7days_fixed(site_codes=None, start_date="2023-01-01", end_date="2023-01-08", 
                          species=None, output_file="weekly_data.csv", max_sites=None):
    """Collect hourly data for specified date range with improved error handling"""
    species = species or ["NO2", "O3", "PM10", "PM25", "SO2"]
    
    # Ensure sites CSV exists
    if not site_codes:
        sites_csv_path = 'data/raw/sites_code_name.csv'
        if not os.path.exists(sites_csv_path):
            print(f"Creating missing sites CSV: {sites_csv_path}")
            create_sites_csv()
        
        api = LAQN_API()
        sites_df = api.get_sites()
        
        if sites_df.empty:
            # Use our created sites as fallback
            sites_df = pd.read_csv(sites_csv_path)
        
        # Find site code column
        site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
        site_codes = sites_df[site_col].tolist()
        if max_sites:
            site_codes = site_codes[:max_sites]
    
    # Convert dates to API format
    start_api = datetime.fromisoformat(start_date).strftime("%d %b %Y")
    end_api = datetime.fromisoformat(end_date).strftime("%d %b %Y")
    
    # Use improved data collection
    api = LAQN_API()
    records = []
    successful_requests = 0
    failed_requests = 0
    
    for site_code in site_codes:
        for species_code in species:
            try:
                site_records = api.get_data_robust(site_code, species_code, start_api, end_api)
                if site_records:
                    records.extend(site_records)
                    successful_requests += 1
                else:
                    failed_requests += 1
                    
            except Exception as e:
                failed_requests += 1
                logger.error(f"Error collecting {site_code}/{species_code}: {e}")
            
            time.sleep(0.3)  # Rate limiting
    
    # Save to CSV
    if records:
        df = pd.DataFrame(records)
        df.to_csv(output_file, index=False)
        
        return {
            "out_file": output_file, 
            "rows": len(records), 
            "successful": successful_requests, 
            "failed": failed_requests
        }
    else:
        return {
            "out_file": None, 
            "rows": 0, 
            "successful": 0, 
            "failed": failed_requests
        }


def estimate_total_runtime(
    year: int = 2023,
    sites_csv: str = "data/raw/sites_code_name.csv",
    species: Optional[List[str]] = None,
    concurrency: int = 60,
    date_chunks: Optional[List[Tuple[str, str]]] = None,
    sample_sites: int = 5,
    sample_species: int = 2,
    repeats: int = 2,
) -> Dict:
    """Probe a few API requests to estimate total runtime"""

    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]
    if date_chunks is None:
        date_chunks = [
            (f"{year}-01-01", f"{year}-03-31"),  # Q1
            (f"{year}-04-01", f"{year}-06-30"),  # Q2
            (f"{year}-07-01", f"{year}-09-30"),  # Q3
            (f"{year}-10-01", f"{year}-12-31"),  # Q4
        ]
    
    # Load site list from CSV; fallback to API sites
    p = Path(sites_csv)
    if p.exists():
        sites_df = pd.read_csv(p)
        site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
        site_codes = sites_df[site_col].astype(str).unique().tolist()
    else:
        api = LAQN_API()
        sites_df = api.get_sites()
        if sites_df is None or sites_df.empty:
            return {"error": "no sites available to estimate"}
        site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
        site_codes = sites_df[site_col].astype(str).unique().tolist()

    if not site_codes:
        return {"error": "no site codes found"}

    # Choose samples
    sample_sites = min(sample_sites, len(site_codes))
    sample_species = min(sample_species, len(species))
    samples_sites = random.sample(site_codes, sample_sites)
    samples_species = random.sample(species, sample_species)

    api = LAQN_API()
    base = api.base_url

    # Use first chunk date range for timing probe
    start_iso, end_iso = date_chunks[0]
    start_api = datetime.fromisoformat(start_iso).strftime("%d %b %Y")
    end_api = datetime.fromisoformat(end_iso).strftime("%d %b %Y")

    # Timing collection
    timings = []
    for sc in samples_sites:
        for sp in samples_species:
            url = (
                f"{base}Data/SiteSpecies/SiteCode={quote(str(sc))}/"
                f"SpeciesCode={quote(str(sp))}/StartDate={quote(start_api)}/EndDate={quote(end_api)}/csv"
            )
            for _ in range(repeats):
                t0 = perf_counter()
                try:
                    r = api.session.get(url, timeout=60)
                    # Read small slice to ensure transfer
                    _ = r.text[:1]
                    dt = perf_counter() - t0
                    timings.append(dt)
                except Exception:
                    # If request fails, count as a longer attempt to be conservative
                    timings.append(5.0)
                time.sleep(0.1)

    if not timings:
        return {"error": "no timings collected"}

    # Calculate estimates
    avg_request_s = sum(timings) / len(timings)
    min_request_s = min(timings)
    max_request_s = max(timings)
    
    n_sites = len(site_codes)
    n_species = len(species)
    n_chunks = len(date_chunks)
    total_requests = n_sites * n_species * n_chunks

    # Estimated wall time assuming perfect saturation of concurrency
    eta_seconds = math.ceil(total_requests / max(1, concurrency)) * avg_request_s

    def _fmt(s):
        s = int(round(s))
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        if h:
            return f"{h}h{m:02d}m{sec:02d}s"
        if m:
            return f"{m}m{sec:02d}s"
        return f"{sec}s"

    return {
        "avg_request_s": round(avg_request_s, 3),
        "min_request_s": round(min_request_s, 3),
        "max_request_s": round(max_request_s, 3),
        "sampled_requests": len(timings),
        "total_sites": n_sites,
        "total_species": n_species,
        "chunks": n_chunks,
        "total_requests": total_requests,
        "concurrency": concurrency,
        "eta_seconds": int(eta_seconds),
        "eta_human": _fmt(eta_seconds)
    }


def collect_year_parallel(
    year: int,
    output_file: str = None,
    species: Optional[List[str]] = None,
    max_workers: int = 24,
    pause_s: float = 0.05,
    max_sites: Optional[int] = None,
) -> Dict:
    """Collect full year of data using parallel processing"""
    
    # Default species to collect
    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]
    
    # Auto-generate output filename if not provided
    if output_file is None:
        output_file = f"data/raw/LAQN_{year}_parallel.csv"

    # Set date strings (ISO) then format to LAQN API form
    start_iso = f"{year}-01-01"
    end_iso = f"{year}-12-31"

    # Use LAQN_API instance and session
    api = LAQN_API()
    sites_df = api.get_sites()
    base = api.base_url
    
    if sites_df is None or sites_df.empty:
        return {
            "error": "No sites available",
            "out_file": None,
            "rows": 0,
            "year": year
        }
    
    # Extract site codes
    site_col = next(
        (c for c in ("@SiteCode", "SiteCode", "siteCode") 
         if c in sites_df.columns), 
        sites_df.columns[0]
    )
    
    site_codes = sites_df[site_col].astype(str).unique().tolist()
    
    if max_sites:
        site_codes = site_codes[:int(max_sites)]

    # Per-site worker: fetch all species for one site
    def _worker_fetch(site_code: str):
        """Fetch all species data for a single site"""
        records = []
        
        for sp in species:
            # Format dates to LAQN expected "01 Jan 2023"
            start_api = datetime.fromisoformat(start_iso).strftime("%d %b %Y")
            end_api = datetime.fromisoformat(end_iso).strftime("%d %b %Y")
            
            # Build API URL with CSV endpoint
            url = (
                f"{base}Data/SiteSpecies/"
                f"SiteCode={quote(str(site_code))}/"
                f"SpeciesCode={quote(str(sp))}/"
                f"StartDate={quote(start_api)}/"
                f"EndDate={quote(end_api)}/"
                f"csv"
            )
            
            try:
                # Use api.session for pooling and retries
                response = api.session.get(url, timeout=60)
                
                if response.status_code == 200:
                    # Parse CSV response
                    from io import StringIO
                    csv_data = StringIO(response.text)
                    df = pd.read_csv(csv_data)
                    
                    # Process each CSV row as a measurement
                    for _, row in df.iterrows():
                        record = {
                            '@MeasurementDateGMT': row.get('@MeasurementDateGMT', ''),
                            '@LocalAuthorityName': row.get('@LocalAuthorityName', ''),
                            '@SiteCode': row.get('@SiteCode', site_code),
                            '@SiteName': row.get('@SiteName', ''),
                            '@SiteType': row.get('@SiteType', ''),
                            '@SpeciesCode': sp,
                            '@Value': row.get('@Value', ''),
                            '@DateClosed': row.get('@DateClosed', ''),
                            '@DateOpened': row.get('@DateOpened', ''),
                            '@Latitude': row.get('@Latitude', ''),
                            '@Longitude': row.get('@Longitude', '')
                        }
                        records.append(record)
                else:
                    logger.warning(f"HTTP error {response.status_code} for site {site_code}, species {sp}")
            except Exception as e:
                logger.error(f"Error fetching data for site {site_code}, species {sp}: {e}")
        
        return records if records else None
    
    # Parallel execution
    all_records = []
    success = 0
    fail = 0
    total_sites = len(site_codes)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(_worker_fetch, s): s for s in site_codes}
        with tqdm(total=total_sites, desc="Sites", unit="site") as pbar:
            for fut in concurrent.futures.as_completed(futures):
                s = futures[fut]
                try:
                    r = fut.result()
                    if r:
                        all_records.extend(r)
                        success += 1
                    else:
                        fail += 1
                except Exception:
                    fail += 1
                
                pbar.update(1)
                pbar.set_postfix({"succ": success, "fail": fail, "recs": len(all_records)})
                time.sleep(pause_s)

    # Save all records to CSV
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(output_file, index=False)
        
        return {
            "error": None,
            "out_file": output_file,
            "rows": len(all_records),
            "successful": success,
            "failed": fail,
            "year": year
        }
    else:
        return {
            "error": "No data collected",
            "out_file": None,
            "rows": 0,
            "year": year
        }


def collect_year_async_chunked(
    year: int = 2023,
    sites_csv: str = "data/raw/sites_code_name.csv",
    output_prefix: str = "data/raw/2023_async_chunk",
    species: Optional[List[str]] = None,
    concurrency: int = 60,
    connector_limit: int = 80,
    retries: int = 2,
    pause_s: float = 0.0,
    date_chunks: Optional[List[Tuple[str, str]]] = None,
) -> dict:
    """Fetch full year in chunks (default 4 quarters)"""
    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]
    if date_chunks is None:
        date_chunks = [
            (f"{year}-01-01", f"{year}-03-31"),  # Q1
            (f"{year}-04-01", f"{year}-06-30"),  # Q2
            (f"{year}-07-01", f"{year}-09-30"),  # Q3
            (f"{year}-10-01", f"{year}-12-31"),  # Q4
        ]

    summary = []
    total_rows = 0
    start = perf_counter()
    
    for idx, (start_iso, end_iso) in enumerate(date_chunks, start=1):
        start_api = datetime.fromisoformat(start_iso).strftime("%d %b %Y")
        end_api = datetime.fromisoformat(end_iso).strftime("%d %b %Y")
        chunk_out = f"{output_prefix}_chunk{idx}.csv"
        
        # Call the async collection function for this chunk
        res = collect_year_async_chunk(
            year=year,
            sites_csv=sites_csv,
            output_file=chunk_out,
            species=species,
            concurrency=concurrency,
            connector_limit=connector_limit,
            retries=retries,
            pause_s=pause_s,
            start_date=start_iso,
            end_date=end_iso
        )
        res.update({"chunk": idx, "start": start_iso, "end": end_iso, "file": chunk_out})
        summary.append(res)
        total_rows += res.get("rows", 0)
        
        # Progress tracking with ETA
        elapsed = perf_counter() - start
        done_chunks = idx
        remaining_chunks = len(date_chunks) - done_chunks
        avg_per_chunk = elapsed / done_chunks if done_chunks else 0
        eta = avg_per_chunk * remaining_chunks
    
    summary_file = f"{output_prefix}_summary.csv"
    pd.DataFrame(summary).to_csv(summary_file, index=False)
    return {"chunks": summary, "total_rows": total_rows, "summary_file": summary_file}


def collect_year_async_chunk(
    year: int = 2023,
    sites_csv: str = "data/raw/sites_code_name.csv",
    output_file: str = "data/raw/2023_async_chunk.csv",
    species: Optional[List[str]] = None,
    concurrency: int = 100,
    connector_limit: int = 100,
    retries: int = 2,
    pause_s: float = 0.0,
    start_date: str = None,
    end_date: str = None,
):
    """Modified version of async collection for specific date ranges (chunks)"""
    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]

    # Create sites CSV if it doesn't exist
    p = Path(sites_csv)
    if not p.exists():
        print(f"Sites CSV not found at {sites_csv}, creating it...")
        sites_file, sites_df = create_sites_csv()
        print(f"Created sites CSV with {len(sites_df)} sites")
    else:
        sites_df = pd.read_csv(p)
    
    site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
    site_codes = sites_df[site_col].astype(str).unique().tolist()

    # Use provided date range or default to full year
    if start_date and end_date:
        start_api = datetime.fromisoformat(start_date).strftime("%d %b %Y")
        end_api = datetime.fromisoformat(end_date).strftime("%d %b %Y")
    else:
        start_api = datetime.fromisoformat(f"{year}-01-01").strftime("%d %b %Y")
        end_api = datetime.fromisoformat(f"{year}-12-31").strftime("%d %b %Y")
    
    api = LAQN_API()
    base = api.base_url

    total_tasks = len(site_codes) * len(species)
    q = asyncio.Queue(maxsize=1000)

    header = ["@MeasurementDateGMT","@LocalAuthorityName","@SiteCode","@SiteName","@SiteType","@SpeciesCode","@Value","@DateClosed","@DateOpened","@Latitude","@Longitude"]
    stats = {"rows": 0, "success_tasks": 0, "failed_tasks": 0}

    async def writer():
        with open(output_file, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=header)
            w.writeheader()
            while True:
                item = await q.get()
                if item is None:
                    q.task_done()
                    break
                w.writerow(item)
                stats["rows"] += 1
                q.task_done()

    async def _run():
        conn = aiohttp.TCPConnector(limit=connector_limit, force_close=False)
        timeout = aiohttp.ClientTimeout(total=120)
        sem = asyncio.Semaphore(concurrency)
        
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            worker_tasks = []
            writer_task = asyncio.create_task(writer())
            total_success = 0
            total_fail = 0
            
            for sc in site_codes:
                for sp in species:
                    worker_tasks.append(asyncio.create_task(
                        _fetch_and_enqueue(session, sem, q, base, sc, sp, start_api, end_api,
                                           retries=retries, timeout=timeout.total)
                    ))
                    if pause_s:
                        await asyncio.sleep(pause_s)
                    
            for res_task in asyncio.as_completed(worker_tasks):
                success_count, fail_count = await res_task
                total_success += success_count
                total_fail += fail_count
                    
            await q.put(None)
            await q.join()
            await writer_task
            return total_success, total_fail

    total_success, total_fail = asyncio.run(_run())

    return {
        "out_file": output_file, 
        "rows": stats["rows"], 
        "successful_tasks": total_success, 
        "failed_tasks": total_fail
    }


async def _fetch_and_enqueue(session, sem, queue, base, site_code, sp, start_api, end_api, retries=2, timeout=60):
    """Helper function for async data fetching using CSV endpoint"""
    url = f"{base}Data/SiteSpecies/SiteCode={quote(str(site_code))}/SpeciesCode={quote(str(sp))}/StartDate={quote(start_api)}/EndDate={quote(end_api)}/csv"
    attempt = 0
    
    while attempt <= retries:
        attempt += 1
        async with sem:
            try:
                async with session.get(url, timeout=timeout) as resp:
                    status = resp.status
                    if status != 200:
                        # Non-200, retry
                        if attempt <= retries:
                            await asyncio.sleep(0.5 * attempt)
                            continue
                        return 0, 1
                    
                    try:
                        # Read CSV response
                        text_data = await resp.text()
                        from io import StringIO
                        csv_data = StringIO(text_data)
                        df = pd.read_csv(csv_data)
                    except Exception:
                        # Bad CSV
                        return 0, 1
                    
                    count = 0
                    # Process each CSV row
                    for _, row in df.iterrows():
                        csv_row = {
                            "@MeasurementDateGMT": row.get("@MeasurementDateGMT", ""),
                            "@LocalAuthorityName": row.get("@LocalAuthorityName", ""),
                            "@SiteCode": row.get("@SiteCode", site_code),
                            "@SiteName": row.get("@SiteName", ""),
                            "@SiteType": row.get("@SiteType", ""),
                            "@SpeciesCode": sp,
                            "@Value": row.get("@Value", ""),
                            "@DateClosed": row.get("@DateClosed", ""),
                            "@DateOpened": row.get("@DateOpened", ""),
                            "@Latitude": row.get("@Latitude", ""),
                            "@Longitude": row.get("@Longitude", "")
                        }
                        await queue.put(csv_row)
                        count += 1
                    return count, 0
                    
            except asyncio.TimeoutError:
                if attempt <= retries:
                    await asyncio.sleep(0.5 * attempt)
                    continue
                return 0, 1
            except Exception:
                if attempt <= retries:
                    await asyncio.sleep(0.5 * attempt)
                    continue
                return 0, 1
    return 0, 1


def combine_chunks_to_hourly_wide(
    chunk_files: List[str],
    output_file: str = "data/raw/2023_async_hourly_wide.csv",
) -> pd.DataFrame:
    """Combine chunk CSVs and pivot to one row per hour/site, columns per species"""
    # Load all chunks
    frames = []
    for fpath in chunk_files:
        p = Path(fpath)
        if p.exists():
            frames.append(pd.read_csv(p))

    if not frames:
        raise FileNotFoundError("no chunk files found to combine")

    # Combine DataFrames
    df = pd.concat(frames, ignore_index=True)
    
    # Clean and process timestamps
    df["@MeasurementDateGMT"] = pd.to_datetime(df["@MeasurementDateGMT"], errors="coerce")
    df = df.dropna(subset=["@MeasurementDateGMT", "@SpeciesCode"])
    
    # Pivot to wide format
    wide = (
        df.pivot_table(
            index=["@MeasurementDateGMT", "@SiteCode"],
            columns="@SpeciesCode",
            values="@Value",
            aggfunc="first",
        )
        .reset_index()
        .sort_values(["@SiteCode", "@MeasurementDateGMT"])
    )
    wide.columns.name = None
    wide.to_csv(output_file, index=False)
    
    return wide