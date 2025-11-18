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


    def test_get_groups(self):
        """Test the get_groups function."""
        df = self.laqn_getter.get_groups()
        # Check if the returned object is a DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        # Check if the DataFrame is not empty
        self.assertFalse(df.empty)
        # Check if specific columns exist in the DataFrame
        expected_columns = {'GroupName', 'Description'}
        self.assertTrue(expected_columns.issubset(set(df.columns)))
        self.assertTrue(os.path.exists(self.groups_csv_path), "groups.csv does not exist.")
        df = pd.read_csv(self.groups_csv_path)
        # Check for missing values in key columns
        key_columns = ['GroupName', 'Description']
        for col in key_columns:
            self.assertFalse(df[col].isnull().any(), f"Missing values found in column: {col}")

if __name__ == '__main__':
    unittest.main() #that will be run the test cases nested in the TestLaqnGet class.
    print("Testing for get_groups function is completed.")
