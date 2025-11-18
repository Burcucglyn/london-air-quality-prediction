"""Testing file for laqn_get.py. This file will be contain test cases for each function defined in laqn_get.py to ensure they work as expected.
To run the tests, laqn_get.py and config.py files should be in the src/ folder. and import here.
"""
#importing necessary libraries for testing.
import unittest
import pandas as pd
import os, sys #os to check file existence. sys to modify the system path for imports.
#importing laqn_test.py file below.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importing the laqnGet class from laqn_get.py file.
from src.laqn_get import laqnGet
from config import Config

# creating a class to test laqnGet class function below.
class TestLaqnGet(unittest.TestCase):
    """Class to test laqnGet class functions."""

    def setUp(self):
        """Set up the laqnGet instance for testing."""
        self.laqn_getter = laqnGet()
         # used os.path.join to create the path to groups.csv file for path consistency across different OS.
        self.groups_csv_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'laqn', 'groups.csv'
        )


    def test_get_sites_species(self):
        """Test the get_sites_species function."""
        df = self.laqn_getter.get_sites_species()
        print(df.head())  # Preview first 5 rows
        print(df.columns) # Preview column names

        # Check if the returned object is a DataFrame.
        self.assertIsInstance(df, pd.DataFrame)
        # Check if the DataFrame is not empty.
        self.assertFalse(df.empty)
        # Check if specific columns exist in the DataFrame.
        expected_columns = {'SiteCode', 'SiteName', 'SpeciesCode', 'SpeciesName'}
        self.assertTrue(expected_columns.issubset(set(df.columns)))

        # Check if sites_species_london.csv was saved.
        self.assertTrue(os.path.exists(self.sites_species_csv_path), "sites_species_london.csv does not exist.")
        df_saved = pd.read_csv(self.sites_species_csv_path)
        # Check for missing values in key columns.
        for col in expected_columns:
            self.assertFalse(df_saved[col].isnull().any(), f"Missing values found in column: {col}")

if __name__ == '__main__':
    unittest.main()
    print("Testing for get_sites_species function is completed.")
