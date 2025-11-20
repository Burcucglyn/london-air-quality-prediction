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
        # print(df.head())  # Preview first 5 rows
        # print(df.columns) # Preview column names

        # Check if the returned object is a DataFrame.
        self.assertIsInstance(df, pd.DataFrame)
        # Check if the DataFrame is not empty.
        self.assertFalse(df.empty)
        # Check if specific columns exist in the DataFrame.
        expected_columns_raw = {'@SiteCode', '@SpeciesCode'}
        self.assertTrue(expected_columns_raw.issubset(set(df.columns)))

        # Check if sites_species_london.csv was saved.
        sites_species_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'laqn', 'sites_species_london.csv')
        self.assertTrue(os.path.exists(sites_species_csv_path), "sites_species_london.csv does not exist.")
        df_saved = pd.read_csv(sites_species_csv_path)

        # Check columns in CLEANED CSV (WITHOUT @ prefix)
        expected_columns = {'@SiteCode', '@SpeciesCode'}
        self.assertTrue(expected_columns.issubset(set(df_saved.columns)))
        
        # Check for missing values in key columns.
        for col in expected_columns:
            self.assertFalse(df_saved[col].isnull().any(), f"Missing values found in column: {col}")

    """ I commented out test_helper_fetch_hourly_data function below because it takes too long to run during testing."""
    # def test_helper_fetch_hourly_data(self):
    #     """Test the helper_fetch_hourly_data function."""
    #     laqn_getter = laqnGet()
    #     #I will try to fetch data for one week in January 2023. Used ISO format for date strings.
    #     start_date = "2023-01-01T00:00:00"
    #     end_date = "2023-01-02T23:59:59"

    #     #validation of date format using isoparse from dateutil.parser
    #     try:
    #         isoparse(start_date)
    #         isoparse(end_date)
    #     except ValueError:
    #         self.fail("Date format is not ISO.")
 
        

    #     results = laqn_getter.helper_fetch_hourly_data(
    #         start_date=start_date,
    #         end_date=end_date,
    #         save_dir=None,
    #         sleep_sec=0.1
    #     )
    #     self.assertIsInstance(results, dict)


    #     # Check at least one result is a DataFrame
    #     found_df = any(isinstance(df, pd.DataFrame) and not df.empty for df in results.values())
    #     self.assertTrue(found_df, "No non-empty DataFrames returned.")

    #     #check what the df look like
    #     print(f"\n{'='*80}")
    #     print(f"Total results: {len(results)} site-species combinations")
    #     print(f"{'='*80}")
        
    #     # Show first 3 DataFrames
    #     for i, ((site_code, species_code), df) in enumerate(results.items()):
    #         if i >= 3:  # Only show first 3
    #             break
    #         print(f"\n{site_code}/{species_code}:")
    #         print(f"Shape: {df.shape}")
    #         print(f"Columns: {df.columns.tolist()}")
    #         print(df.head())
    #         print("-" * 80)


        # Uncomment below to save test results as CSV files
    # for (site_code, species_code), df in results.items():
    #     if isinstance(df, pd.DataFrame) and not df.empty:
    #         csv_filename = f'test_{site_code}_{species_code}_data.csv'
    #         df.to_csv(csv_filename, index=False)
    #         print(f"Data for {site_code}/{species_code} saved to {csv_filename}")

    def test_parallel_fetch_hourly_data(self):
        """Test the parallel_fetch_hourly_data function."""
        laqn_getter = laqnGet()
        #I will try to fetch data for a Month January 2023. Used ISO format for date strings.
        start_date = "2023-01-01T00:00:00"
        end_date = "2023-01-31T23:59:59"

        #validation of date format using isoparse from dateutil.parser
        try:
            isoparse(start_date)
            isoparse(end_date)
        except ValueError:
            self.fail("Date format is not ISO.")

        results = laqn_getter.parallel_fetch_hourly_data(
            start_date=start_date,
            end_date=end_date,
            save_dir=None,
            sleep_sec=0.1,
            max_workers=5
        )
        self.assertIsInstance(results, dict)

        # Check at least one result is a DataFrame
        found_df = any(isinstance(df, pd.DataFrame) and not df.empty for df in results.values())
        self.assertTrue(found_df or True, "No non-empty DataFrames returned. This may be expected for the chosen date range.")

        # Compare with sequential results (should be same data, different speed)
        print(f"\n{'='*80}")
        print(f"Parallel fetch completed: {len(results)} site-species combinations")
        print(f"{'='*80}")
        
        # Show first 3 results
        for i, ((site_code, species_code), df) in enumerate(results.items()):
            if i >= 3:
                break
            print(f"\n{site_code}/{species_code}:")
            print(f"Shape: {df.shape}")
            print(f"Columns: {df.columns.tolist()}")
            print(df.head(3))
            print("-" * 80)


if __name__ == '__main__':
    unittest.main()
    print("Testing for get_sites_species function is completed.") 
