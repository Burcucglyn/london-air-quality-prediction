"""
test_api.py
-----------
This module contains tests for the functions in data_collection.py.
It verifies API connectivity, site and pollutant fetching, data collection, and utility functions.

Tests:
1. API Connectivity:
   - test_api_connectivity: Tests basic API connectivity.

2. Sites and Pollutants:
   - test_sites_endpoint: Tests the sites endpoint.
   - test_pollutants_endpoint: Tests the pollutants endpoint.

3. Data Collection:
   - test_hourly_data: Tests the get_hourly_7days_fixed function.
   - test_year_parallel: Tests the collect_year_parallel function.
   - test_year_async_chunked: Tests the collect_year_async_chunked function.

4. Utilities:
   - test_runtime_estimation: Tests the estimate_total_runtime function.
   - test_combine_chunks: Tests the combine_chunks_to_hourly_wide function.
"""
import os
import time
import traceback
import requests
from pathlib import Path
from time import perf_counter
import pandas as pd
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

#------ import LAQN API func here ----
from src.data_collection import (
    LAQN_API,
    create_pollutants_csv,
    get_sites, save_pollutants_to_csv, get_pollutants, save_sites_to_csv,
    # collect_working_combinations,
    # collect_weekly_sample,
    # get_hourly_7days_fixed,
    # estimate_total_runtime,
    collect_year_parallel,
    collect_year_async_chunked,
    combine_chunks_to_hourly_wide
)

from datetime import datetime


# -------------------------------
# STEP 1: API CONNECTIVITY TESTS
# -------------------------------

def test_api_connectivity():
    """Test basic API connectivity with detailed output"""
    print("="*60)
    print("Testing API Connectivity")
    print("="*60)
    
    api = LAQN_API()
    
    print("1. Testing basic connectivity...")
    connected = api.test_connectivity()
    print(f"   API accessible: {connected}")
    
    if not connected:
        print("   API unreachable - possible causes:")
        print("      - Network restrictions/firewall")
        print("      - VPN issues")
        print("      - API server maintenance")
        print("   Try: Direct data downloads from London Datastore")
        return False
    
    print("   API is accessible!")
    return True

# -------------------------------
# STEP 2: SITES AND POLLUTANTS TESTS
# -------------------------------

""" Test the sites endpoint, fallbacks to creating a local CSV to prevent falling API
request failures """
def test_sites_endpoint():
    """Test the sites information endpoint."""
    print("\n" + "="*60)
    print("Testing Sites Endpoint")
    print("="*60)
    
    api = LAQN_API()
    
    print("1. Fetching London monitoring sites...")
    sites_df = api.get_sites()
    
    if sites_df.empty:
        print("   No sites returned from API")
        print("   Creating fallback sites CSV...")
        sites_file, fallback_df = save_sites_to_csv()
        print(f"   Created fallback with {len(fallback_df)} sites")
        sites_df = fallback_df
    else:
        print(f"   Found {len(sites_df)} sites from API")
    
    print(f"   Columns: {list(sites_df.columns)}")
    
    if '@SiteType' in sites_df.columns:
        site_types = sites_df['@SiteType'].value_counts()
        print(f"   Site types: {dict(site_types)}")
    
    print("\n   Sample sites:")
    for i, row in sites_df.head(5).iterrows():
        site_code = row.get('@SiteCode', 'Unknown')
        site_name = row.get('@SiteName', 'Unknown') 
        site_type = row.get('@SiteType', 'Unknown')
        print(f"      {site_code}: {site_name} ({site_type})")
    
    return sites_df

def test_species_endpoint():
    """Test the pollutants/species endpoint"""
    print("\n" + "="*60)
    print("Testing Species Endpoint")
    print("="*60)
    
    api = LAQN_API()
    
    print("1. Fetching available pollutants...")
    species_df = api.get_pollutants()
    
    if species_df.empty:
        print("   No species data returned")
        print("   Using standard species: NO2, O3, PM10, PM25, SO2, CO")
        return ['NO2', 'O3', 'PM10', 'PM25', 'SO2', 'CO']
    
    print(f"   Found {len(species_df)} pollutants")
    print(f"   Columns: {list(species_df.columns)}")
    
    if '@SpeciesCode' in species_df.columns:
        species_codes = species_df['@SpeciesCode'].tolist()[:10]
        print(f"   Available species: {species_codes}")
        return species_codes
    
    return ['NO2', 'O3', 'PM10', 'PM25', 'SO2', 'CO']

def test_sites_csv_creation():
    """Test automatic sites CSV creation"""
    print("\n" + "="*60)
    print("Testing Sites CSV Creation")
    print("="*60)
    
    print("1. Testing create_sites_csv()...")
    
    try:
        sites_file, sites_df = save_sites_to_csv()
        print(f"   Created sites CSV: {sites_file}")
        print(f"   Total sites: {len(sites_df)}")
        print(f"   Columns: {list(sites_df.columns)}")
        
        if '@SiteType' in sites_df.columns:
            site_types = sites_df['@SiteType'].value_counts()
            print(f"   Site types: {dict(site_types)}")
        
        print("   Sample sites:")
        for i, row in sites_df.head(3).iterrows():
            print(f"      {row.get('@SiteCode', 'Unknown')}: {row.get('@SiteName', 'Unknown')}")
            
    except Exception as e:
        print(f"   Sites CSV creation failed: {e}")

# -------------------------------
# STEP 3: DATA COLLECTION TESTS
# -------------------------------

def test_data_collection():
    """Test actual data collection with detailed diagnostics"""
    print("\n" + "="*60)
    print("Testing Data Collection")
    print("="*60)
    
    api = LAQN_API()
    
    # Test parameters
    test_sites = ['BL0', 'MY1', 'CT2']
    test_species = ['NO2', 'PM10']
    start_date = "01 Jan 2023"
    end_date = "07 Jan 2023"
    
    print(f"   Testing sites: {test_sites}")
    print(f"   Testing species: {test_species}")
    print(f"   Date range: {start_date} to {end_date}")
    
    all_records = []
    successful_collections = 0
    failed_collections = 0
    
    for site_code in test_sites:
        for species_code in test_species:
            print(f"\n   Collecting {site_code}/{species_code}...")
            
            try:
                records = api.get_data_robust(site_code, species_code, start_date, end_date)
                
                if records:
                    print(f"      Got {len(records)} records")
                    all_records.extend(records)
                    successful_collections += 1
                    
                    # Show sample data
                    sample = records[0] if records else {}
                    if sample.get('@Value'):
                        print(f"      Sample value: {sample['@Value']}")
                    if sample.get('@MeasurementDateGMT'):
                        print(f"      Sample time: {sample['@MeasurementDateGMT']}")
                else:
                    print(f"      No data returned")
                    failed_collections += 1
                    
            except Exception as e:
                print(f"      Error: {str(e)[:100]}")
                failed_collections += 1
            
            time.sleep(0.5)  # Rate limiting
    
    print(f"\n   Collection summary:")
    print(f"      Successful: {successful_collections}")
    print(f"      Failed: {failed_collections}")
    print(f"      Total records: {len(all_records)}")
    
    if all_records:
        # Data quality analysis
        print(f"\n   Data quality:")
        df = pd.DataFrame(all_records)
        
        for col in ['@Value', '@MeasurementDateGMT', '@SiteCode', '@SpeciesCode']:
            if col in df.columns:
                non_empty = df[col].notna() & (df[col] != '')
                total = len(df)
                percentage = (non_empty.sum() / total) * 100
                print(f"      {col}: {non_empty.sum()}/{total} ({percentage:.1f}%) populated")
        
        # Save test data
        test_file = "test_data_collection.csv"
        df.to_csv(test_file, index=False)
        print(f"   Saved test data: {test_file}")
        
        return df
    
    return pd.DataFrame()

def test_collection_functions():
    """Test the main collection functions"""
    print("\n" + "="*60)
    print("Testing Collection Functions")
    print("="*60)
    
    # Test 1: Weekly sample
    print("1. Testing collect_weekly_sample()...")
    try:
        result = collect_weekly_sample("test_weekly.csv")
        print(f"   Weekly sample: {result.get('rows', 0)} rows")
        print(f"   File: {result.get('out_file', 'None')}")
        print(f"   Success rate: {result.get('successful', 0)}/{result.get('successful', 0) + result.get('failed', 0)}")
    except Exception as e:
        print(f"   Weekly sample failed: {e}")
    
    # Test 2: Working combinations
    print("\n2. Testing collect_working_combinations()...")
    try:
        result = collect_working_combinations("test_working.csv")
        print(f"   Working combinations: {result.get('rows', 0)} rows")
        print(f"   File: {result.get('out_file', 'None')}")
    except Exception as e:
        print(f"   Working combinations failed: {e}")
    
    # Test 3: Fixed hourly collection  
    print("\n3. Testing get_hourly_7days_fixed()...")
    try:
        result = get_hourly_7days_fixed(
            site_codes=['BL0', 'MY1'], 
            species=['NO2', 'PM10'],
            output_file="test_hourly.csv",
            start_date="2023-01-01",
            end_date="2023-01-03"
        )
        print(f"   Hourly collection: {result.get('rows', 0)} rows")
        print(f"   File: {result.get('out_file', 'None')}")
    except Exception as e:
        print(f"   Hourly collection failed: {e}")

def test_runtime_estimation():
    """Test runtime estimation"""
    print("\n" + "="*60)
    print("Testing Runtime Estimation")
    print("="*60)
    
    print("1. Testing estimate_total_runtime()...")
    
    try:
        start_time = perf_counter()
        
        result = estimate_total_runtime(
            year=2023, 
            concurrency=20,
            sample_sites=3,
            sample_species=2,
            repeats=2
        )
        
        estimation_time = perf_counter() - start_time
        
        print(f"   Runtime estimation completed in {estimation_time:.2f}s")
        print(f"   Sample performance:")
        print(f"      Samples collected: {result.get('samples', 0)}")
        print(f"      Avg response time: {result.get('avg_time', 0):.3f}s")
        print(f"      Success rate: {result.get('success_rate', 0):.1%}")
        print(f"   Projections for full year:")
        print(f"      Sequential time: {result.get('sequential_hours', 0):.1f} hours")
        print(f"      Parallel time (20 workers): {result.get('parallel_hours', 0):.1f} hours")
        print(f"      Speedup factor: {result.get('speedup', 0):.1f}x")
        print(f"      Total requests needed: {result.get('total_requests', 0):,}")
        
    except Exception as e:
        print(f"   Runtime estimation failed: {e}")

def test_parallel_collection():
    """Test parallel year collection with limited scope"""
    print("\n" + "="*60)
    print("Testing Parallel Collection")
    print("="*60)
    
    print("1. Testing limited parallel collection...")
    
    try:
        # Test with very limited parameters to avoid overwhelming
        result = collect_year_parallel(
            year=2023,
            output_file="test_parallel_mini.csv",
            species=['NO2', 'PM10'],  # Only 2 species
            max_workers=3,            # Limited workers
            max_sites=2,              # Only 2 sites
            pause_s=0.5,             # Slower to be nice to API
            max_months=1             # Only January 2023
        )
        
        if result.get('error'):
            print(f"   Parallel collection failed: {result['error']}")
        else:
            print(f"   Parallel collection: {result.get('rows', 0)} rows")
            print(f"   File: {result.get('out_file', 'None')}")
            print(f"   Success rate: {result.get('successful', 0)}/{result.get('successful', 0) + result.get('failed', 0)}")
            
    except Exception as e:
        print(f"   Parallel collection failed: {e}")

def test_chunked_collection():
    """Test chunked async collection"""
    print("\n" + "="*60)
    print("Testing Chunked Collection")
    print("="*60)
    
    print("1. Testing chunked async collection (mini chunks)...")
    
    try:
        # Very small test chunks
        mini_chunks = [
            ("2023-01-01", "2023-01-07"),
            ("2023-01-08", "2023-01-14")
        ]
        
        result = collect_year_async_chunked(
            year=2023,
            output_prefix="data/raw/tests/mini_chunk",
            species=['NO2', 'PM10'],
            concurrency=5,
            date_chunks=mini_chunks
        )
        
        print(f"   Chunked collection completed")
        print(f"   Total chunks: {len(result['chunks'])}")
        print(f"   Total rows: {result['total_rows']}")
        print(f"   Summary file: {result.get('summary_file', 'None')}")
        
        # Show chunk details
        for chunk in result['chunks']:
            print(f"      Chunk {chunk['chunk']}: {chunk.get('rows', 0)} rows ({chunk['start']} to {chunk['end']})")
            
    except Exception as e:
        print(f"   Chunked collection failed: {e}")

def test_2023_data_collection():
    """Test the specialized 2023 data collection function"""
    print("\n" + "="*60)
    print("Testing 2023 Data Collection")
    print("="*60)
    
    print("1. Testing small 2023 sample...")
    
    try:
        # Import the new function
        from src.data_collection import collect_2023_london_data
        
        # Test with limited sites for faster testing
        result = collect_2023_london_data(
            output_file="test_2023_sample.csv",
            max_sites=3  # Limit to 3 sites for testing
        )
        
        if result.get('error'):
            print(f"   2023 collection failed: {result['error']}")
        else:
            print(f"   2023 collection results:")
            print(f"      Total records: {result.get('rows', 0)}")
            print(f"      Output file: {result.get('out_file', 'None')}")
            print(f"      Sites covered: {result.get('sites', 0)}")
            print(f"      Species covered: {result.get('species', 0)}")
            print(f"      Success rate: {result.get('successful', 0)}/{result.get('successful', 0) + result.get('failed', 0)}")
            
            # Check if we got actual measurement values
            if result.get('out_file') and os.path.exists(result['out_file']):
                df = pd.read_csv(result['out_file'])
                if '@Value' in df.columns:
                    non_empty_values = df['@Value'].notna() & (df['@Value'] != '')
                    print(f"      Values with data: {non_empty_values.sum()}/{len(df)}")
                    
                    if non_empty_values.sum() > 0:
                        sample_values = df[non_empty_values]['@Value'].head(3).tolist()
                        print(f"      Sample values: {sample_values}")
            
    except Exception as e:
        print(f"   2023 collection test failed: {e}")

def test_quarterly_collection():
    """Test quarterly 2023 data collection"""
    print("\n" + "="*60)
    print("Testing Quarterly Collection")
    print("="*60)
    
    print("1. Testing quarterly 2023 collection...")
    
    try:
        from src.data_collection import collect_2023_quarterly
        
        result = collect_2023_quarterly(
            output_prefix="test_2023_q",
            concurrency=5  # Low concurrency for testing
        )
        
        print(f"   Quarterly collection results:")
        print(f"      Total rows: {result['total_rows']}")
        print(f"      Quarters collected: {len(result['quarters'])}")
        print(f"      Summary file: {result.get('summary_file', 'None')}")
        
        for quarter_result in result['quarters']:
            quarter = quarter_result.get('quarter', 'Unknown')
            rows = quarter_result.get('rows', 0)
            print(f"         {quarter}: {rows} rows")
            
    except Exception as e:
        print(f"   Quarterly collection failed: {e}")

# -------------------------------
# STEP 4: UTILITY TESTS
# -------------------------------

# Note: test_runtime_estimation is already included in data collection section above

# -------------------------------
# Main Test Runner
# -------------------------------

def run_all_tests():
    """Run complete test suite"""
    print("LAQN API Comprehensive Test Suite")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test sequence
    tests = [
        ("API Connectivity", test_api_connectivity),
        ("Sites CSV Creation", test_sites_csv_creation),
        ("Sites Endpoint", test_sites_endpoint),
        ("Species Endpoint", test_species_endpoint),
        ("Data Collection", test_data_collection),
        ("Collection Functions", test_collection_functions),
        ("Runtime Estimation", test_runtime_estimation),
        ("Parallel Collection", test_parallel_collection),
        ("Chunked Collection", test_chunked_collection)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning {test_name}...")
            start_time = time.time()
            test_result = test_func()
            duration = time.time() - start_time
            results[test_name] = {'status': 'passed', 'duration': duration, 'result': test_result}
            print(f"   Completed in {duration:.2f}s")
        except Exception as e:
            duration = time.time() - start_time if 'start_time' in locals() else 0
            results[test_name] = {'status': 'failed', 'duration': duration, 'error': str(e)}
            print(f"   Failed after {duration:.2f}s: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)
    
    total_tests = len(tests)
    passed_tests = sum(1 for r in results.values() if r['status'] == 'passed')
    
    print(f"Tests passed: {passed_tests}/{total_tests}")
    print(f"Total time: {sum(r['duration'] for r in results.values()):.2f}s")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = result['status']
        duration = result['duration']
        print(f"   {status}: {test_name}: {duration:.2f}s")
        if 'error' in result:
            print(f"      Error: {result['error']}")
    
    # Recommendations
    print("\nRecommendations:")
    if not any(r['status'] == 'passed' for r in results.values()):
        print("   All tests failed - check network connectivity")
        print("   Try direct data downloads from London Datastore")
    elif results.get('API Connectivity', {}).get('status') == 'failed':
        print("   API unreachable - use direct download sources")
    else:
        print("   API working - you can collect data!")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

if __name__ == "__main__":
    # Create data directory

    os.makedirs("data/raw/tests", exist_ok=True)
    
    # Run all tests
    run_all_tests()
    
    # Additional 2023-specific tests
    print("\n" + "="*80)
    print("Running 2023-Specific Tests")
    print("="*80)
    
    test_2023_data_collection()
    test_quarterly_collection()