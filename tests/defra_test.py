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

from src.defra_get import DefraGet
from config import Config
from pathlib import Path


class TestDefraGet(unittest.TestCase):
    """Class to test DefraGet class functions."""

    def setUp(self):
        """Set up the DefraGet instance for testing."""
        self.defra_getter = DefraGet()

    def test_post_capabilities(self):
        """Test the post_capabilities function."""
        print("\n" + "="*80)
        print("TEST: post_capabilities()")
        print("="*80)
        
        capabilities = self.defra_getter.post_capabilities(save_json=False, save_csv=False)
        
        # Check if response is valid.
        self.assertIsInstance(capabilities, dict, "Expected dict response.")
        self.assertGreater(len(capabilities), 0, "Capabilities should not be empty.")

        # Check structure - contents might be dict or the offerings might be at top level
        contents = capabilities.get('contents', {})
    
        # Handle if contents is a dict
        if isinstance(contents, dict):
            offerings = contents.get('observationOfferings', [])
        # Handle if contents is already a list (the offerings)
        elif isinstance(contents, list):
            offerings = contents
        # Fallback - try to get offerings directly from capabilities
        else:
            offerings = capabilities.get('observationOfferings', [])

        print(f"\nNumber of offerings found: {len(offerings)}")

        #view structure of capabilities response. firt 10 offerings.
        print("\n" + "-"*80)
        print("First 10 offerings structure:")
        for i, offering in enumerate(offerings[:10]):
            print(f"\nOffering {i+1}:")
            print(json.dumps(offering, indent=2))
            print(f"   ID: {offering.get('identifier', 'N/A')}")
            print(f"   Procedure: {offering.get('procedure', ['N/A'])[0] if offering.get('procedure') else 'N/A'}")
            print(f"   Pollutant: {offering.get('observableProperty', ['N/A'])[0] if offering.get('observableProperty') else 'N/A'}")
            print(f"   Time range: {offering.get('phenomenonTime', ['N/A', 'N/A'])[0]} to {offering.get('phenomenonTime', ['N/A', 'N/A'])[1]}")

        """commented out detailed structure checks for now to speed up testing.
         Uncomment if needed to debug structure of capabilities response."""
        
        # print("\nCapabilities keys:", list(capabilities.keys()))
        
        # # Check for standard SOS structure.
        # if 'contents' in capabilities:
        #     print("Found 'contents' key.")
        #     contents = capabilities['contents']
        #     print("\nContents type:", type(contents))
        #     print("Contents keys:", list(contents.keys()) if isinstance(contents, dict) else "Not a dict")
        #     print("\nFull contents structure:")

        #     #json print statement to see everything inside contents.
        #     #print(json.dumps(contents, indent=2)) 

        #     if 'offerings' in contents:
        #         offerings = contents['offerings']
        #         print(f"Found {len(offerings)} offerings.")
                
        #         if offerings:
        #             print("\nFirst offering structure:")
        #             print(json.dumps(offerings[0], indent=2))

        # else:
        #     print("No 'contents' key found in capabilities.")
        #     print("Trying alternatives:")

        #     for key in ['observationOfferings', 'Offerings', 'offering']:
        #         if key in contents:
        #             print(f"Found '{key}' instead!")
        #             print(json.dumps(contents[key], indent=2)[:500])


        # Comment out file checks for initial testing.
        # # Check if CSV was created and is readable.
        # csv_file = Path('data/defra/capabilities/capabilities.csv')
        # self.assertTrue(csv_file.exists(), "CSV file should exist.")
        
        # if csv_file.exists():
        #     df = pd.read_csv(csv_file)
        #     print(f"\nCSV created successfully.")
        #     print(f"CSV shape: {df.shape}")
        #     print(f"CSV columns: {df.columns.tolist()}")
        #     print("\nFirst 10 rows of CSV:")
        #     print(df.head(10).to_string())
        
        # # Check if JSON was created.
        # json_file = Path('data/defra/capabilities/capabilities.json')
        # self.assertTrue(json_file.exists(), "JSON file should exist.")
        # print(f"\nJSON file created at: {json_file}")
        
        print("\n" + "="*80)
        print("TEST COMPLETED: post_capabilities()")
        print("="*80)


if __name__ == '__main__':
    unittest.main()
    print("Testing for DEFRA post_capabilities function completed.")




        