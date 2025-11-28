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

    def test_get_sites_species(self):
        """Test the get_sites_species function."""
        print("\n" + "="*80)
        print("TEST: get_sites_species()")
        print("="*80)
        
        stations = self.defra_getter.get_sites_species()
        
        # Check if the returned object is a list.
        self.assertIsInstance(stations, list, "Expected list, got something else.")
        
        # Check if the list is not empty.
        self.assertGreater(len(stations), 0, "Expected stations, got empty list.")
        
        print(f"\nRetrieved {len(stations)} stations from DEFRA API.")
        
        # Display first 5 stations to understand structure.
        print("\nFirst 5 stations:")
        print("-"*80)
        for i, station in enumerate(stations[:5], 1):
            print(f"\nStation {i}:")
            print(json.dumps(station, indent=2))
        
        # Check structure of first station.
        if stations:
            first_station = stations[0]
            print("\nKeys in first station:")
            print(list(first_station.keys()))
            
            # Check for expected fields.
            expected_fields = ['id', 'name', 'lat', 'lon']
            for field in expected_fields:
                if field in first_station:
                    print(f"  {field}: {first_station[field]}")
                else:
                    print(f"  {field}: missing")
        
        # Save to JSON for inspection.
        output_dir = os.path.join('data', 'defra', 'test')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'stations_sample.json')
        
        with open(output_file, 'w') as f:
            json.dump(stations[:10], f, indent=2)  # Save first 10 stations
        
        print(f"\nSaved first 10 stations to: {output_file}")
        
        print("\n" + "="*80)
        print("TEST COMPLETED: get_sites_species()")
        print("="*80)


if __name__ == '__main__':
    unittest.main()
    print("Testing for get_sites_species function is completed.")
 





        
