"""Testing file for defra_get.py. This file will contain test cases for each function defined in defra_get.py to ensure they work as expected.
To run the tests, defra_get.py and config.py files should be in the src/ folder and import here.
"""

import unittest
import pandas as pd
import os
import sys
import json
import requests
# Add project root to path for imports.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        
        capabilities = self.defra_getter.post_capabilities(save_json=True, save_csv=True)
        
        # Check if response is valid.
        self.assertIsInstance(capabilities, dict, "Expected dict response.")
        self.assertGreater(len(capabilities), 0, "Capabilities should not be empty.")
        
        print("\nCapabilities keys:", list(capabilities.keys()))
        
        # Check for standard SOS structure.
        if 'contents' in capabilities:
            print("Found 'contents' key.")
            contents = capabilities['contents']
            if 'offerings' in contents:
                offerings = contents['offerings']
                print(f"Found {len(offerings)} offerings.")
                
                if offerings:
                    print("\nFirst offering structure:")
                    print(json.dumps(offerings[0], indent=2))
        
        # Check if CSV was created and is readable.
        csv_file = Path('data/defra/capabilities/capabilities.csv')
        self.assertTrue(csv_file.exists(), "CSV file should exist.")
        
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            print(f"\nCSV created successfully.")
            print(f"CSV shape: {df.shape}")
            print(f"CSV columns: {df.columns.tolist()}")
            print("\nFirst 10 rows of CSV:")
            print(df.head(10).to_string())
        
        # Check if JSON was created.
        json_file = Path('data/defra/capabilities/capabilities.json')
        self.assertTrue(json_file.exists(), "JSON file should exist.")
        print(f"\nJSON file created at: {json_file}")
        
        print("\n" + "="*80)
        print("TEST COMPLETED: post_capabilities()")
        print("="*80)


if __name__ == '__main__':
    unittest.main()
    print("Testing for DEFRA post_capabilities function completed.")




        