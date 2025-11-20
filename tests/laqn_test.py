"""Testing file for laqn_get.py. This file will be contain test cases for each function defined in laqn_get.py to ensure they work as expected.
To run the tests, laqn_get.py and config.py files should be in the src/ folder. and import here.
"""
#importing necessary libraries for testing.
import unittest
import pandas as pd
# import response
import os, sys #os to check file existence. sys to modify the system path for imports.
#importing laqn_test.py file below.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Df returns jaSON response from laqn API, so i need to parse JSON response as csv DataFrame.
import json
#date formatting imports below for ISO format date parsing.
from dateutil.parser import isoparse

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
        self.sites_species_csv_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'laqn', 'sites_species_london.csv'
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
        expected_columns_raw = {'@SiteCode', '@SpeciesCode'}
        self.assertTrue(expected_columns_raw.issubset(set(df.columns)))

        # Check if sites_species_london.csv was saved.
        actve_sites_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'laqn', 'actv_sites_species.csv')
        self.assertTrue(os.path.exists(actve_sites_csv_path), "actv_sites_species.csv does not exist.")
        df_saved = pd.read_csv(actve_sites_csv_path)

        # Check columns in CLEANED CSV (WITHOUT @ prefix)
        expected_columns_cleaned = {'SiteCode', 'SpeciesCode'}
        self.assertTrue(expected_columns_cleaned.issubset(set(df_saved.columns)))
        
        # Check for missing values in key columns.
        for col in expected_columns_cleaned:
            self.assertFalse(df_saved[col].isnull().any(), f"Missing values found in column: {col}")


    def test_helper_fetch_hourly_data(self):
        """Test the helper_fetch_hourly_data function."""
        laqn_getter = laqnGet()
        #I will try to fetch data for one week in January 2023. Used ISO format for date strings.
        start_date = "2023-01-01T00:00:00"
        end_date = "2023-01-02T23:59:59"

        #validation of date format using isoparse from dateutil.parser
        try:
            isoparse(start_date)
            isoparse(end_date)
        except ValueError:
            self.fail("Date format is not ISO.")
        

        results = laqn_getter.helper_fetch_hourly_data(
            start_date=start_date,
            end_date=end_date,
            save_dir=None,
            sleep_sec=0.1
        )
        self.assertIsInstance(results, dict)
        # Check at least one result is a DataFrame
        found_df = any(isinstance(df, pd.DataFrame) and not df.empty for df in results.values())
        self.assertTrue(found_df, "No non-empty DataFrames returned.")

        # Uncomment below to save test results as CSV files
    # for (site_code, species_code), df in results.items():
    #     if isinstance(df, pd.DataFrame) and not df.empty:
    #         csv_filename = f'test_{site_code}_{species_code}_data.csv'
    #         df.to_csv(csv_filename, index=False)
    #         print(f"Data for {site_code}/{species_code} saved to {csv_filename}")



if __name__ == '__main__':
    unittest.main()
    print("Testing for get_sites_species function is completed.")
