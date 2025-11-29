"""Testing file for defra_get.py. This file will contain test cases for each function defined in defra_get.py to ensure they work as expected.
To run the tests, defra_get.py and config.py files should be in the src/ folder and import here.
"""

import unittest
import pandas as pd
import os
import sys
import json
import requests
from pathlib import Path
# Add project root to path for imports.
proj_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(proj_root))

from src.defra_get import DefraGet, euAirPollutantVocab
from config import Config
from io import StringIO # for CSV reading from response text.

class TestDefraGet(unittest.TestCase):
    """Class to test DefraGet class functions."""

    def setUp(self):
        """Set up the DefraGet instance for testing."""
        self.defra_getter = DefraGet()

    def test_post_capabilities(self):
        """Test the post_capabilities function."""

        """commented out full test to speed up routine testing.
        Uncomment to run full pipeline test.    """
        # print("\n" + "="*80)
        # print("TEST: post_capabilities()")
        # print("="*80)
        
        # # I don't want to save files over and over during testing, so disable saving for test.
        # capabilities = self.defra_getter.post_capabilities(save_json=False, save_csv=False)
        
        # # Check if response is valid.
        # self.assertIsInstance(capabilities, dict, "Expected dict response.")
        # self.assertGreater(len(capabilities), 0, "Capabilities should not be empty.")

        # # Check structure - contents might be dict or the offerings might be at top level
        # contents = capabilities.get('contents', {})
    
        # # Handle if contents is a dict
        # if isinstance(contents, dict):
        #     offerings = contents.get('observationOfferings', [])
        # # Handle if contents is already a list (the offerings)
        # elif isinstance(contents, list):
        #     offerings = contents
        # # Fallback try to get offerings directly from capabilities
        # else:
        #     offerings = capabilities.get('observationOfferings', [])

        # print(f"\nNumber of offerings found: {len(offerings)}")

        # #commented out detailed structure checks for now to speed up testing.
        # #view structure of capabilities response. firt 10 offerings.
        # # print("\n" + "-"*80)
        # # print("First 10 offerings structure:")
        # # for i, offering in enumerate(offerings[:10]):
        # #     print(f"\nOffering {i+1}:")
        # #     print(json.dumps(offering, indent=2))
        # #     print(f"   ID: {offering.get('identifier', 'N/A')}")
        # #     print(f"   Procedure: {offering.get('procedure', ['N/A'])[0] if offering.get('procedure') else 'N/A'}")
        # #     print(f"   Pollutant: {offering.get('observableProperty', ['N/A'])[0] if offering.get('observableProperty') else 'N/A'}")
        # #     print(f"   Time range: {offering.get('phenomenonTime', ['N/A', 'N/A'])[0]} to {offering.get('phenomenonTime', ['N/A', 'N/A'])[1]}")

        # """commented out detailed structure checks for now to speed up testing.
        #  Uncomment if needed to debug structure of capabilities response."""
    
        # # Comment out file checks for initial testing.
        # # Check if CSV was created and is readable.
        # # csv_file = Path('data/defra/capabilities/capabilities.csv')
        # # self.assertTrue(csv_file.exists(), "CSV file should exist.")
        
        # # if csv_file.exists():
        # #     df = pd.read_csv(csv_file)
        
        # # #     print(f"\nCSV created successfully.")
        # #     print(f"CSV shape: {df.shape}")
        # #     print(f"CSV columns: {df.columns.tolist()}")
        # #     print("\nFirst 5 rows of CSV:")
        # #     print(df.head(5).to_string())
        
        # # # # Check if JSON was created.
        # # json_file = Path('data/defra/capabilities/capabilities.json')
        # # self.assertTrue(json_file.exists(), "JSON file should exist.")
        # # print(f"\nJSON file created at: {json_file}")

        # #parser without saving files.
        # print("\n" + "-"*80)
        # print("TESTING CSV PARSER:")
        # print("-"*80)
        # rows = self.defra_getter._capabilities_to_rows(capabilities)
        # df = pd.DataFrame(rows)
        # print(f"Parser created DataFrame: {df.shape}")
        # print(f" Columns: {df.columns.tolist()}")
        # print(f"\n  First 5 rows:")
        # print(df.head(5).to_string(index=False))
        
        # print("\n" + "="*80)
        # print("TEST COMPLETED: post_capabilities()")
        # print("="*80)

        pass ##added pass to avoid indentation error.

    """3. test for describe sensor function."""
    def test_describe_sensor(self):
        # """Test the describe_sensor function."""
        # print("\n" + "="*80)
        # print("TEST: Get Station metadata describe_sensor()")
        # print("="*80)

        # # Test with one known procedure from capabilities
        # test_procedure = "http://environment.data.gov.uk/air-quality/so/GB_StationProcess_1003"
    
        # print(f"\nRequesting metadata for: {test_procedure}")
    
        # # Call the method
        # data = self.defra_getter.describe_sensor(test_procedure)
        
        # # Validate response
        # self.assertIsInstance(data, dict, "Should return dict.")
        # self.assertNotEqual(data, {}, "Response should not be empty.")
        
        # # Save full response to file for inspection
        # output_path = Path("data/defra/test/describe_sensor.json")
        # output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # with open(output_path, "w") as f:
        #     json.dump(data, f, indent=2)
        
        # print(f"\nResponse saved to: {output_path}")
        # print(f"\nResponse keys: {list(data.keys())}")
        # print(f"\nFirst 1000 characters of response:")
        # print(json.dumps(data, indent=2)[:1000])
        
        # print("\n" + "="*80)
        # print("test complited check the json file to see station metadata structure")
        # print("="*80)
        pass

    """ 4. step, the describe_sensor outputs showes that structure contains XML embedded as a string. Thats points that I need to parse XML and see that if the coordinations are there.
    so need ro run tests to check xml complete."""
    def test_describe_sensor_xml(self):
    #     """Test parsing XML from describe_sensor response."""
    #     print("\n" + "="*80)
    #     print("TEST: Parse XML from describe_sensor()")
    #     print("="*80)

    #     test_procedure = "http://environment.data.gov.uk/air-quality/so/GB_StationProcess_1003"
    #     data = self.defra_getter.describe_sensor(test_procedure)
    
    # # Extract and pretty-print the XML
    #     if 'procedureDescription' in data:
    #         xml_string = data['procedureDescription']
        
    #         # Save full XML to file
    #         output_path = Path("data/defra/test/describe_sensor_full.xml")
    #         output_path.parent.mkdir(parents=True, exist_ok=True)
            
    #         with open(output_path, "w") as f:
    #             f.write(xml_string)
            
    #         print(f"\nFull XML saved to: {output_path}")
    #         print(f"\nXML length: {len(xml_string)} characters")
    #         print("\nSearching for coordinates...")
            
    #         # Look for common coordinate patterns
    #         if 'gml:pos' in xml_string:
    #             print("Found gml:pos in XML")
    #         if 'latitude' in xml_string.lower():
    #             print("Found 'latitude' in XML")
    #         if 'longitude' in xml_string.lower():
    #             print("✓ Found 'longitude' in XML")
            
    #         # Show the full XML (first 2000 chars)
    #         print("\nFirst 2000 characters of XML:")
    #         print(xml_string[:2000])
        pass

    

    def test_get_london_stations(self):
        """Test REST API Get London stations with bounding box filter."""
        print("\n" + "="*80)
        print("Test Get London Stations (REST API with bbox)")
        print("="*80)
        
        # Call the new method
        df = self.defra_getter.get_london_stations(save_csv=False)
        
        # Assertions
        self.assertIsInstance(df, pd.DataFrame, "Should return DataFrame")
        self.assertFalse(df.empty, "DataFrame should not be empty")
        
        # Check expected columns
        expected_cols = ['station_id', 'station_name', 'latitude', 'longitude', 
                        'timeseries_id', 'pollutant']
        for col in expected_cols:
            self.assertIn(col, df.columns, f"Should have {col} column")
        
        # Print summary
        print(f"\nFound {df['station_id'].nunique()} unique stations")
        print(f"Total station-pollutant combinations: {len(df)}")
        print(f"\nColumns: {df.columns.tolist()}")
        print(f"\nFirst 5 rows:")
        print(df.head().to_string(index=False))
        
        # Show pollutant distribution
        print(f"\nPollutant distribution:")
        print(df['pollutant'].value_counts())
        
        # Save for manual inspection
        output_path = Path("data/defra/test/london_stations_test.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"\nSaved test output to: {output_path}")

    def test_get_timeseries_data(self):
        """Test fetching actual measurement data for a timeseries."""
        print("\n" + "="*80)
        print("TEST: Get Timeseries Data")
        print("="*80)
        
        # First get a valid timeseries_id
        df = self.defra_getter.get_london_stations(save_csv=False)
        
        # Filter for rows with valid timeseries_id
        valid = df[df['timeseries_id'].notna()]
        
        if valid.empty:
            self.skipTest("No valid timeseries found")
        
        # Test with first available timeseries
        test_row = valid.iloc[0]
        timeseries_id = test_row['timeseries_id']
        station_name = test_row['station_name']
        pollutant = test_row['pollutant']
        
        print(f"\nTesting with:")
        print(f"  Station: {station_name}")
        print(f"  Pollutant: {pollutant}")
        print(f"  Timeseries ID: {timeseries_id}")
        
        # Fetch data for a short period
        timespan = "2023-01-01T00:00:00Z/2023-01-07T23:59:59Z"
        print(f"\nFetching data for: {timespan}")
        
        measurements = self.defra_getter.get_timeseries_data(timeseries_id, timespan)
        
        # Assertions
        self.assertIsInstance(measurements, pd.DataFrame, "Should return DataFrame")
        
        if not measurements.empty:
            print(f"\nRetrieved {len(measurements)} measurements")
            print(f"\nColumns: {measurements.columns.tolist()}")
            print(f"\nFirst 5 measurements:")
            print(measurements.head().to_string(index=False))
            
            # Save sample
            output_path = Path("data/defra/test/sample_measurements.csv")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            measurements.to_csv(output_path, index=False)
            print(f"\Saved to: {output_path}")
        else:
            print("\n No measurements found for this period")    
        


class TestEUAirPollutantVocab(unittest.TestCase):
    """Class to test fetching and parsing EU pollutant vocabulary CSV."""

    """commented out full test to speed up routine testing.
        Uncomment to run full pipeline test.
    """
    # def test_fetch_eu_pollutant_vocab(self):
    #     """Test fetching and parsing the EU pollutant vocabulary CSV."""
    #     print("\n" + "="*80)
    #     print("TEST: Fetch EU Pollutant Vocabulary CSV")
    #     print("="*80)

    #     csv_url = Config.eu_pollutant_vocab_url
    #     print(f"Fetching CSV from URL: {csv_url}")

    #     try:
            
    #         response = requests.get(csv_url, timeout=30)
    #         print(f"\nResponse Status: {response.status_code}")
            
    #         if response.status_code == 200:
    #             print(f"Request code 200 that's good.")
    #             print(f"\nResponse length: {len(response.text)} characters")
    #             print(f"\nFirst 500 characters:")
    #             print(response.text[:500])
                
    #             df = pd.read_csv(StringIO(response.text))
    #             print(f"\nDataFrame created.")
    #             print(f"Shape: {df.shape}")
    #             print(f"Columns: {df.columns.tolist()}")
    #             print(f"\nFirst 5 rows:")
    #             print(df.head())
    #         else:
    #             print(f"Request failed: {response.status_code}")
    #             print(f"Response: {response.text[:500]}")
                
    #     except Exception as e:
    #         self.fail(f"Error occurred while fetching/parsing CSV: {e}")

    #     print("\n" + "="*80)
    #     print("TEST COMPLETED: Fetch EU Pollutant Vocabulary CSV")
    #     print("="*80)

    def test_fetch_and_process_pollutant_vocab(self):

        """commented out full test to speed up routine testing.
         Uncomment to run full pipeline test."""
        # """Test full pollutant vocabulary fetch, process, and save pipeline."""
        # print("\n" + "="*80)
        # print("TEST: Fetch, Process, and Save EU Pollutant Vocabulary")
        # print("="*80)
        
        # vocab_fetcher = euAirPollutantVocab()
        # df_raw = vocab_fetcher.fetch_vocab()
        # print(f"\nRaw data fetched: {len(df_raw)} rows, {len(df_raw.columns)} columns.")

        # # Process the vocabulary
        # df_clean = vocab_fetcher.process_vocab(df_raw)
        # print(f"\nProcessed data: {len(df_clean)} rows, {len(df_clean.columns)} columns.")
        # print(f"\nFirst 5 rows of processed data:")
        # print(df_clean.head().to_string(index=False))

        # #validation of processed data
        # self.assertIsNotNone(df_clean, "Processed DataFrame should not be None")
        # required_cols = ['uri_code', 'pollutant_code', 'pollutant_name', 'status']
        # for col in required_cols:
        #     self.assertIn(col, df_clean.columns, f"Should have {col} column")
        # #show first 10 rows/pollutants
        # print(f"\nFirst 10 pollutants:")
        # print(df_clean[['uri_code', 'pollutant_code', 'pollutant_name']].head(10).to_string(index=False))
        # print(f"\nTotal pollutants processed: {len(df_clean)}")


        
        # # Check for major pollutants
        # major_codes = ['SO2', 'NO2', 'O3', 'CO', 'PM10', 'PM25']
        # display_cols = ['uri_code', 'pollutant_code', 'pollutant_name', 'definition', 'status']
        # major = df_clean[df_clean['pollutant_code'].isin(major_codes)][display_cols]

        # if not major.empty:
        #     print(major.to_string(index=False))
        #     print(f"\nFound {len(major)} major pollutants")
        # else:
        #     print("No exact matches - showing first 20 pollutants instead:")
        #     print(df_clean[display_cols].head(20).to_string(index=False))

        # #save to file (disabled for testing speed)
        # vocab_fetcher.save_vocab(df_clean)
        # print(f"\nSaved to data/defra/pollutant_mapping.csv")    


        # print(f"\n{'='*80}")
        # print("SUMMARY:")
        # print(f"{'='*80}")
        # print(f"Total pollutants: {len(df_clean)}")
        # print(f"Unique codes: {df_clean['pollutant_code'].nunique()}")
        # print(f"Status counts:")
        # print(df_clean['status'].value_counts())
    pass ##added pass to avoid indentation error.  

if __name__ == '__main__':
    unittest.main()
    print("Testing for DEFRA post_capabilities function completed.")
    unittest.TestCase()
    print("Testing for EU Air Pollutant Vocabulary CSV fetch completed.")