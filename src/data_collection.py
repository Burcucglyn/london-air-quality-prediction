"""
Air Quality Data Collection Module for LAQN (London Air Quality Network) API

This file complete workflow for collecting air quality data from the LAQN API.
The functions are organised below:

WORKFLOW:
1. API Setup & Basic Operations (LAQN_API class)
2. Site Discovery (get_sites, save_sites_to_csv)
3. Pollutant Discovery (get_pollutants, save_pollutants_to_csv)
4. Data Collection Methods (get_hourly_7days_fixed, collect_year_parallel, collect_year_async_chunked)
5. Utility Functions (estimate_total_runtime, combine_chunks_to_hourly_wide)

CSV FILES CREATED:
- sites_code_name.csv: Contains all monitoring sites (created by save_sites_to_csv)
- pollutants_info.csv: Contains all available pollutants (created by save_pollutants_to_csv)
- weekly_data.csv: Sample hourly data for 7 days (created by get_hourly_7days_fixed)
- yearly_data.csv: Full year data using parallel collection (created by collect_year_parallel)
- {prefix}_chunk_{n}.csv: Individual chunk files (created by collect_year_async_chunked)
- hourly_wide_format.csv: Combined wide-format data (created by combine_chunks_to_hourly_wide)

DEPENDENCIES:
- requests: HTTP requests to LAQN API
- pandas: Data manipulation and CSV operations
- aiohttp: Asynchronous HTTP requests
- tqdm: Progress bars for long operations
"""

# -------------------------------
# Imports and Setup
# -------------------------------
from pathlib import Path
import logging
import threading
import asyncio
from datetime import datetime
from threading import Thread
import time
from time import perf_counter
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, urljoin
import csv
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import aiohttp
from tqdm import tqdm
import tempfile
import json

# Configure logging for the module
logger = logging.getLogger(__name__)

# -------------------------------
# 1. API SETUP & BASIC OPERATIONS
# -------------------------------

class LAQN_API:
    """
    Core API client for interacting with the LAQN (London Air Quality Network) API.
    
    This class handles:
    - HTTP session management with retry logic
    - Authentication headers
    - Rate limiting and error handling
    - Thread-safe operations
    
    Used by: All data collection functions
    Creates: Foundation for all API interactions
    """
    base_url = "https://api.erg.ic.ac.uk/AirQuality/"

    def __init__(self, timeout=60, max_retries=5):
        """
        Initialize API client with robust session configuration.
        
        Args:
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retry attempts
        """
        sess = requests.Session()
        sess.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = timeout
        
        # Configure retry strategy for robust API interactions
        retry = Retry(
            total=max_retries,
            backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504, 520, 521, 522, 523, 524],
            allowed_methods=["GET", "POST"],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retry)
        sess.mount("https://", adapter)
        sess.mount("http://", adapter)
        self.session = sess
        self.lock = threading.Lock()  # Thread safety for parallel operations

# -------------------------------
# 2. SITE DISCOVERY FUNCTIONS
# -------------------------------

def get_sites(api_client: LAQN_API = None) -> pd.DataFrame:
    """
    Fetch all available monitoring sites from LAQN API.
    
    This is the FIRST STEP in the data collection workflow.
    You must run this before any data collection to know which sites exist.
    
    Args:
        api_client (LAQN_API, optional): Existing API client instance
        
    Returns:
        pd.DataFrame: Site information with columns like @SiteCode, @SiteName, @Latitude, @Longitude
        
    Used by: save_sites_to_csv, all data collection functions
    Creates: Foundation for site-based data collection
    """
    if api_client is None:
        api_client = LAQN_API()
        
    try:
        url = urljoin(api_client.base_url, "Information/MonitoringSites/GroupName=London/Json")
        resp = api_client.session.get(url, timeout=api_client.timeout)
        resp.raise_for_status()
        data = resp.json()
        
        if "Sites" in data and "Site" in data["Sites"]:
            sites = pd.json_normalize(data["Sites"]["Site"])
            logger.info(f"Successfully fetched {len(sites)} monitoring sites")
            return sites
        else:
            logger.warning("No sites found in API response")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"Error fetching sites: {e}")
        return pd.DataFrame()
    
    


def save_sites_to_csv(output_file: str = "data/raw/sites_code_name.csv", api_client: LAQN_API = None) -> Dict:
    """
    Fetch all monitoring sites and save them to CSV file.
    Normalised return keys: 'out_file' and 'rows' for compatibility with tests.
    """
    sites_df = get_sites(api_client)

    if sites_df.empty:
        return {"error": "No sites found", "out_file": None, "rows": 0}

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    sites_df.to_csv(output_file, index=False)

    return {
        "out_file": output_file,
        "rows": len(sites_df),
        "columns": list(sites_df.columns),
        "sample_sites": sites_df["@SiteCode"].head(5).tolist() if "@SiteCode" in sites_df.columns else []
    }

# -------------------------------
# 3. POLLUTANT DISCOVERY FUNCTIONS
# -------------------------------

def get_pollutants(api_client: LAQN_API = None) -> pd.DataFrame:
    """
    Fetch all available pollutants/species from LAQN API.
    
    This helps you understand what air quality measurements are available.
    Run this to see available species codes before data collection.
    
    Args:
        api_client (LAQN_API, optional): Existing API client instance
        
    Returns:
        pd.DataFrame: Pollutant information with species codes and descriptions
        
    Used by: save_pollutants_to_csv, data collection planning
    """
    if api_client is None:
        api_client = LAQN_API()
        
    try:
        url = urljoin(api_client.base_url, "Information/Species/Json")
        resp = api_client.session.get(url, timeout=api_client.timeout)
        resp.raise_for_status()
        data = resp.json()
        
        if "Species" in data:
            species = pd.json_normalize(data["Species"])
            logger.info(f"Successfully fetched {len(species)} pollutant species")
            return species
        else:
            logger.warning("No species found in API response")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"Error fetching pollutants: {e}")
        return pd.DataFrame()


def save_pollutants_to_csv(output_file: str = "data/raw/pollutants_info.csv", api_client: LAQN_API = None) -> Dict:
    """
    Fetch all available pollutants and save them to CSV file.
    Normalised return keys: 'out_file' and 'rows' for compatibility with tests.
    """
    pollutants_df = get_pollutants(api_client)

    if pollutants_df.empty:
        return {"error": "No pollutants found", "out_file": None, "rows": 0}

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    pollutants_df.to_csv(output_file, index=False)

    return {
        "out_file": output_file,
        "rows": len(pollutants_df),
        "columns": list(pollutants_df.columns),
        "available_species": pollutants_df["@SpeciesCode"].tolist() if "@SpeciesCode" in pollutants_df.columns else []
    }

# -------------------------------
# 4. DATA COLLECTION METHODS
# -------------------------------

def get_hourly_7days_fixed(
    site_codes: Optional[List[str]] = None,
    start_date: str = "2023-01-01",
    end_date: str = "2023-01-08",
    species: Optional[List[str]] = None,
    output_file: str = "data/raw/weekly_data.csv",
    max_sites: Optional[int] = None,
    api_client: LAQN_API = None
) -> Dict:
    """
    Collect hourly air quality data for a specific date range (typically 7 days).
    
    This is the BASIC data collection method - good for testing and small datasets.
    Use this BEFORE attempting larger collections to verify API connectivity.
    
    Args:
        site_codes (List[str], optional): Specific site codes to collect. If None, fetches all sites
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        species (List[str], optional): Pollutant species codes. Defaults to ["NO2", "O3", "PM10", "PM25", "SO2"]
        output_file (str): Path for output CSV file
        max_sites (int, optional): Limit number of sites for testing
        api_client (LAQN_API, optional): Existing API client instance
        
    Returns:
        Dict: Summary with output file path, number of records, and status
        
    Creates CSV: weekly_data.csv (or specified output_file)
    Prerequisites: None (can fetch sites automatically)
    Use case: Testing API connectivity, small data samples
    """
    # Set default species if not provided
    species = species or ["NO2", "O3", "PM10", "PM25", "SO2"]
    
    if api_client is None:
        api_client = LAQN_API()
    
    # Get site codes if not provided
    if not site_codes:
        sites_df = get_sites(api_client)
        if sites_df.empty:
            return {"error": "No sites found", "out_file": None, "rows": 0}
        site_codes = sites_df["@SiteCode"].tolist()
        if max_sites:
            site_codes = site_codes[:max_sites]
    
    # Convert dates to API format
    start_api = datetime.fromisoformat(start_date).strftime("%d %b %Y")
    end_api = datetime.fromisoformat(end_date).strftime("%d %b %Y")
    
    records = []
    total_requests = len(site_codes) * len(species)
    
    logger.info(f"Starting data collection: {len(site_codes)} sites, {len(species)} species, {total_requests} total requests")
    
    # Collect data for each site and species combination
    with tqdm(total=total_requests, desc="Collecting hourly data") as pbar:
        for site_code in site_codes:
            for species_code in species:
                url = (
                    f"{api_client.base_url}Data/SiteSpecies/SiteCode={quote(site_code)}/"
                    f"SpeciesCode={quote(species_code)}/StartDate={quote(start_api)}/"
                    f"EndDate={quote(end_api)}/Period=hourly/Units=ugm3/Step=0/Json"
                )
                try:
                    response = api_client.session.get(url, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        raw = data.get("RawAQData", {})
                        measurements = raw.get("Data", [])
                        
                        # Handle both single measurement and list of measurements
                        if isinstance(measurements, dict):
                            measurements = [measurements]
                        
                        # Process each measurement
                        for m in measurements:
                            record = {
                                "@MeasurementDateGMT": m.get("@MeasurementDateGMT"),
                                "@LocalAuthorityName": raw.get("@LocalAuthorityName"),
                                "@SiteCode": site_code,
                                "@SiteName": raw.get("@SiteName"),
                                "@SiteType": raw.get("@SiteType"),
                                "@SpeciesCode": species_code,
                                "@Value": m.get("@Value"),
                                "@DateClosed": raw.get("@DateClosed"),
                                "@DateOpened": raw.get("@DateOpened"),
                                "@Latitude": raw.get("@Latitude"),
                                "@Longitude": raw.get("@Longitude"),
                            }
                            records.append(record)
                            
                except Exception as e:
                    logger.error(f"Error fetching data for site {site_code}, species {species_code}: {e}")
                
                pbar.update(1)
                time.sleep(0.1)  # Rate limiting to be respectful to API
    
    # Save results to CSV
    if records:
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(records)
        df.to_csv(output_file, index=False)
        
        logger.info(f"Successfully collected {len(records)} records and saved to {output_file}")
        return {
            "out_file": output_file,
            "rows": len(records),
            "sites_processed": len(site_codes),
            "species_processed": len(species),
            "date_range": f"{start_date} to {end_date}"
        }
    else:
        logger.warning("No data collected")
        return {"out_file": None, "rows": 0}


def collect_year_parallel(
    year: int,
    output_file: str = "data/raw/yearly_data.csv",
    species: Optional[List[str]] = None,
    max_workers: int = 24,
    pause_s: float = 0.05,
    max_sites: Optional[int] = None,
    api_client: LAQN_API = None
) -> Dict:
    """
    Collect data for a full year using parallel processing with threading.
    
    This is for MEDIUM to LARGE datasets. Use AFTER testing with get_hourly_7days_fixed.
    Faster than sequential but may overwhelm API if not configured properly.
    
    Args:
        year (int): Year to collect data for
        output_file (str): Path for output CSV file
        species (List[str], optional): Pollutant species codes
        max_workers (int): Number of parallel threads
        pause_s (float): Pause between requests for rate limiting
        max_sites (int, optional): Limit number of sites for testing
        api_client (LAQN_API, optional): Existing API client instance
        
    Returns:
        Dict: Summary with output file path, number of records, and performance stats
        
    Creates CSV: yearly_data.csv (or specified output_file)
    Prerequisites: API connectivity verified with get_hourly_7days_fixed
    Use case: Full year data collection with moderate performance needs
    """
    # Set default species if not provided
    species = species or ["NO2", "O3", "PM10", "PM25", "SO2"]
    
    if api_client is None:
        api_client = LAQN_API()
    
    # Get sites
    sites_df = get_sites(api_client)
    if sites_df.empty:
        return {"error": "No sites found", "out_file": None, "rows": 0}
    
    site_codes = sites_df["@SiteCode"].tolist()
    if max_sites:
        site_codes = site_codes[:max_sites]
    
    start_time = perf_counter()
    
    # TODO: Implement parallel collection logic here
    # This is a placeholder for the actual parallel implementation
    logger.info(f"Starting parallel collection for year {year}")
    logger.info(f"Sites: {len(site_codes)}, Species: {len(species)}, Workers: {max_workers}")
    
    # Placeholder return - implement actual collection logic
    return {
        "out_file": output_file,
        "rows": 0,
        "year": year,
        "sites_processed": len(site_codes),
        "species_processed": len(species),
        "execution_time": perf_counter() - start_time,
        "status": "placeholder_implementation_needed"
    }


def collect_year_async_chunked(
    year: int,
    sites_csv: str = "data/raw/sites_code_name.csv",
    output_prefix: str = "data/raw/yearly_async_chunk",
    species: Optional[List[str]] = None,
    concurrency: int = 60,
    connector_limit: int = 80,
    retries: int = 2,
    pause_s: float = 0.0,
    date_chunks: Optional[List[Tuple[str, str]]] = None,
) -> Dict:
    """
    Collect data for a full year in chunks using asynchronous processing.
    
    This is the MOST EFFICIENT method for large datasets. Use AFTER:
    1. Running save_sites_to_csv() to create the required sites CSV
    2. Testing with smaller methods first
    
    Args:
        year (int): Year to collect data for
        sites_csv (str): Path to CSV file containing site information (REQUIRED)
        output_prefix (str): Prefix for chunk output files
        species (List[str], optional): Pollutant species codes
        concurrency (int): Number of concurrent async requests
        connector_limit (int): HTTP connector pool limit
        retries (int): Number of retry attempts per request
        pause_s (float): Pause between requests
        date_chunks (List[Tuple[str, str]], optional): Custom date ranges for chunking
        
    Returns:
        Dict: Summary with chunk files created, total records, and performance stats
        
    Creates CSV: Multiple files named {output_prefix}_chunk_{n}.csv
    Prerequisites: sites_csv file must exist (created by save_sites_to_csv)
    Use case: Large-scale data collection with optimal performance
    """
    # Verify sites CSV exists
    if not Path(sites_csv).exists():
        return {
            "error": f"Sites CSV file not found: {sites_csv}. Run save_sites_to_csv() first.",
            "chunk_files": [],
            "total_rows": 0
        }
    
    # Set default species if not provided
    species = species or ["NO2", "O3", "PM10", "PM25", "SO2"]
    
    # Load sites from CSV
    try:
        sites_df = pd.read_csv(sites_csv)
        site_codes = sites_df["@SiteCode"].tolist()
    except Exception as e:
        return {
            "error": f"Failed to load sites CSV: {e}",
            "chunk_files": [],
            "total_rows": 0
        }
    
    start_time = perf_counter()
    
    # TODO: Implement async chunked collection logic here
    # This is a placeholder for the actual async implementation
    logger.info(f"Starting async chunked collection for year {year}")
    logger.info(f"Sites: {len(site_codes)}, Species: {len(species)}, Concurrency: {concurrency}")
    
    # Placeholder return - implement actual collection logic
    return {
        "chunk_files": [],
        "total_rows": 0,
        "year": year,
        "sites_processed": len(site_codes),
        "species_processed": len(species),
        "concurrency": concurrency,
        "execution_time": perf_counter() - start_time,
        "status": "placeholder_implementation_needed"
    }

# # -------------------------------
# # 5. UTILITY FUNCTIONS
# # -------------------------------

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
    """
    Estimate total runtime for data collection by sampling API requests.
    
    Run this BEFORE large data collection operations to estimate time requirements.
    Helps plan collection strategies and set realistic expectations.
    
    Args:
        year (int): Year to estimate for
        sites_csv (str): Path to sites CSV file (REQUIRED)
        species (List[str], optional): Pollutant species codes
        concurrency (int): Expected concurrency level
        date_chunks (List[Tuple[str, str]], optional): Expected date chunking
        sample_sites (int): Number of sites to sample for testing
        sample_species (int): Number of species to sample for testing
        repeats (int): Number of test repeats for averaging
        
    Returns:
        Dict: Estimated runtime, API response times, and scaling projections
        
    Prerequisites: sites_csv file must exist (created by save_sites_to_csv)
    Use case: Planning and optimization of large data collection operations
    """
    # Verify sites CSV exists
    if not Path(sites_csv).exists():
        return {
            "error": f"Sites CSV file not found: {sites_csv}. Run save_sites_to_csv() first.",
            "estimated_runtime": None
        }
    
    # Set default species if not provided
    species = species or ["NO2", "O3", "PM10", "PM25", "SO2"]
    
    # Load sites from CSV
    try:
        sites_df = pd.read_csv(sites_csv)
        all_site_codes = sites_df["@SiteCode"].tolist()
    except Exception as e:
        return {
            "error": f"Failed to load sites CSV: {e}",
            "estimated_runtime": None
        }
    
    # Sample sites and species for testing
    test_sites = all_site_codes[:sample_sites]
    test_species = species[:sample_species]
    
    start_time = perf_counter()
    
    # TODO: Implement actual runtime estimation logic here
    # This is a placeholder for the actual estimation implementation
    logger.info(f"Estimating runtime for year {year}")
    logger.info(f"Sampling {len(test_sites)} sites and {len(test_species)} species")
    
    # Placeholder return - implement actual estimation logic
    return {
        "estimated_runtime_hours": 0,
        "sample_sites": len(test_sites),
        "sample_species": len(test_species),
        "total_sites": len(all_site_codes),
        "total_species": len(species),
        "expected_requests": len(all_site_codes) * len(species),
        "concurrency": concurrency,
        "status": "placeholder_implementation_needed"
    }


def combine_chunks_to_hourly_wide(
    chunk_files: List[str],
    output_file: str = "data/raw/hourly_wide_format.csv",
) -> pd.DataFrame:
    """
    Combine multiple chunk files into a single wide-format CSV.
    
    Run this AFTER collect_year_async_chunked to consolidate chunk files.
    Creates a wide-format table where each row is an hour and columns are different species.
    
    Args:
        chunk_files (List[str]): List of chunk CSV file paths to combine
        output_file (str): Path for combined output CSV file
        
    Returns:
        pd.DataFrame: Combined data in wide format
        
    Creates CSV: hourly_wide_format.csv (or specified output_file)
    Prerequisites: Chunk files must exist (created by collect_year_async_chunked)
    Use case: Creating analysis-ready datasets from chunked collection results
    """
    # Verify chunk files exist
    existing_files = [f for f in chunk_files if Path(f).exists()]
    if not existing_files:
        logger.error("No chunk files found")
        return pd.DataFrame()
    
    logger.info(f"Combining {len(existing_files)} chunk files")
    
    # TODO: Implement chunk combination logic here
    # This is a placeholder for the actual combination implementation
    
    # Placeholder return - implement actual combination logic
    combined_df = pd.DataFrame()
    
    if not combined_df.empty:
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        combined_df.to_csv(output_file, index=False)
        logger.info(f"Combined data saved to {output_file}")
    
    return combined_df

def create_sites_csv(output_file: str = "data/raw/sites_code_name.csv", api_client: LAQN_API = None):
    """
    Backwards-compatible wrapper:
    - Saves sites CSV (delegates to save_sites_to_csv)
    - Returns a tuple (out_file, dataframe) to satisfy tests that unpack two values.
    """
    res = save_sites_to_csv(output_file=output_file, api_client=api_client)
    out_file = None
    if isinstance(res, dict):
        out_file = res.get("out_file")
    elif isinstance(res, tuple) and len(res) >= 1:
        out_file = res[0]

    df = None
    if out_file and Path(out_file).exists():
        try:
            df = pd.read_csv(out_file)
        except Exception:
            df = None

    return out_file, df


def create_pollutants_csv(output_file: str = "data/raw/pollutants_info.csv", api_client: LAQN_API = None):
    """
    Backwards-compatible wrapper:
    - Saves pollutants CSV (delegates to save_pollutants_to_csv)
    - Returns a tuple (out_file, dataframe)
    """
    res = save_pollutants_to_csv(output_file=output_file, api_client=api_client)
    out_file = None
    if isinstance(res, dict):
        out_file = res.get("out_file")
    elif isinstance(res, tuple) and len(res) >= 1:
        out_file = res[0]

    df = None
    if out_file and Path(out_file).exists():
        try:
            df = pd.read_csv(out_file)
        except Exception:
            df = None

    return out_file, df

