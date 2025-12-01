"""Testing module for data_inventory.py file."""

import unittest
import pandas as pd
import os
import sys
from pathlib import Path 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_inventory import DataInventory

class TestDataInventory(unittest.TestCase):
    """Unit tests for DataInventory class."""

    def setUp(self):
        """Set up the DataInventory instance for testing."""
        self.data_inventory = DataInventory()
        self.base_path = Path(__file__).parent.parent

    def test_laqn_data(self):
        """Test the laqn_data method."""
        laqn_df = self.data_inventory.laqn_data()
        
        # Check if the returned object is a DataFrame.
        self.assertIsInstance(laqn_df, pd.DataFrame)
        
        # Check if the DataFrame is not empty.
        self.assertFalse(laqn_df.empty)
        
        # Check for expected columns in the DataFrame.
        expected_columns = {'source', 'period', 'site', 'pollutant', 'records', 'file'}
        self.assertTrue(expected_columns.issubset(set(laqn_df.columns)))
        
        # Check if file paths are relative to base path.
        for file_path in laqn_df['file']:
            full_path = self.base_path / file_path
            self.assertTrue(full_path.exists(), f"File does not exist: {full_path}")

if __name__ == '__main__':
    unittest.main()

