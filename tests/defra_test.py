"""Testing file for defra_get.py. This file will contain test cases for each function defined in defra_get.py to ensure they work as expected.
To run the tests, defra_get.py and config.py files should be in the src/ folder and import here.
"""

import unittest
import pandas as pd
import os
import sys
import json

# Add project root to path for imports.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.defra_get import DefraGet
from config import Config


class TestDefraGet(unittest.TestCase):
    """Class to test DefraGet class functions."""

    def setUp(self):
        """Set up the DefraGet instance for testing."""
        self.defra_getter = DefraGet()

    def test_get_capabilities(self):
        """Test the get_capabilities function."""
        print("\n" + "="*80)
        print("TEST: get_capabilities()")
        print("="*80)
        
        capabilities = self.defra_getter.get_capabilities(save_json=True)
        
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
        
        print("\n" + "="*80)
        print("TEST COMPLETED: get_capabilities()")
        print("="*80)


if __name__ == '__main__':
    unittest.main()
    print("Testing for get_sites_species function is completed.")
 





        
