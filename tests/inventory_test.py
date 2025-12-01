"""Testing module for data_inventory.py file."""

import unittest
import pandas as pd
import numpy as np
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
        print("\n" + "="*80)
        print("Running test_laqn_data:")
        print("="*80)
        laqn_df = self.data_inventory.laqn_data()
        
        # Check if the returned object is a df.
        self.assertIsInstance(laqn_df, pd.DataFrame)
        
        
        # Check if the df is not empty.
        self.assertFalse(laqn_df.empty)
        print(f"Total records: {len(laqn_df)}")

        # Check for expected columns in the df.
        expected_columns = {'source', 'period', 'site', 'pollutant', 'records', 'file'}
        self.assertTrue(expected_columns.issubset(set(laqn_df.columns)))
        print(f" All expected col: {expected_columns} are present.")

        print(f"\nLAQN Data Summary:")
        print(f"Unique sites: {laqn_df['site'].nunique()}")
        print(f"Unique pollutants: {laqn_df['pollutant'].nunique()}")
        print(f"Unique periods: {laqn_df['period'].nunique()}")
        print(f"Total data records: {laqn_df['records'].sum():,}")
        print(f"Average records per file: {laqn_df['records'].mean():.0f}")
        
        # Check if file paths are relative to base path.
        for file_path in laqn_df['file']:
            full_path = self.base_path / file_path
            self.assertTrue(full_path.exists(), f"File does not exist: {full_path}")
    
    def test_laqn_col(self):
        """Test LAQN data column types and values."""
        print("\n" + "="*80)
        print("Test LAQN data column:")
        print("="*80)
        laqn_df = self.data_inventory.laqn_data()
        
        # Verify source column values.
        self.assertTrue(all(laqn_df['source'] == 'LAQN'), "All source values should be 'LAQN'.")
        
        # Verify period format.
        self.assertTrue(all(laqn_df['period'].str.contains('_')), "Period should contain underscore.")
        print(f"Sample periods: {laqn_df['period'].unique()[:3].tolist()}")

        # Verify site is not empty.
        self.assertTrue(all(laqn_df['site'].notna()), "Site codes should not be null.")
        self.assertTrue(all(laqn_df['site'].str.len() > 0), "Site codes should not be empty.")
        print(f"Unique pollutants: {sorted(laqn_df['pollutant'].unique().tolist())}")
        
        # Verify pollutant is not empty.
        self.assertTrue(all(laqn_df['pollutant'].notna()), "Pollutant codes should not be null.")
        self.assertTrue(all(laqn_df['pollutant'].str.len() > 0), "Pollutant codes should not be empty.")
        
        # Verify records is positive intg.
        self.assertTrue(all(laqn_df['records'] > 0), "Record counts should be positive.")
        self.assertTrue(pd.api.types.is_integer_dtype(laqn_df['records']), "Records should be integer type.")
        print(f"Records column: All positive integers.")
        print(f"Min records: {laqn_df['records'].min()}")
        print(f"Max records: {laqn_df['records'].max()}")
        print(f"Median records: {laqn_df['records'].median():.0f}")


        # Verify file paths start with expected directory.
        self.assertTrue(all(laqn_df['file'].str.startswith('data/laqn/monthly_data')), 
                       "File paths should start with 'data/laqn/monthly_data'")
            
    def test_defra_data(self):
        """Test the defra_data method."""
        print("\n" + "="*80)
        print("Testing DEFRA data")
        print("="*80)
        
        defra_df = self.data_inventory.defra_data()
        
        # Check if the returned object is a df.
        self.assertIsInstance(defra_df, pd.DataFrame)

        # Check if the df is not empty.
        self.assertFalse(defra_df.empty, "DEFRA DataFrame should not be empty.")
        print(f"Total records: {len(defra_df)}")
        
        # Check for expected columns.
        expected_columns = {'source', 'period', 'station', 'pollutant', 'records', 'file'}
        self.assertTrue(expected_columns.issubset(set(defra_df.columns)))
        print(f"All expected columns present: {expected_columns}")
        
        # Print summ statistics.
        print(f"\nDEFRA Data Summary:")
        print(f"Unique stations: {defra_df['station'].nunique()}")
        print(f"Unique pollutants: {defra_df['pollutant'].nunique()}")
        print(f"Unique periods: {defra_df['period'].nunique()}")
        print(f"Total data records: {defra_df['records'].sum():,}")
        print(f"Average records per file: {defra_df['records'].mean():.0f}")
        
        # Verify all sources are labeled as DEFRA.
        self.assertTrue(all(defra_df['source'] == 'DEFRA'))
        
        # Check if file paths exist.
        file_check_count = 0
        for file_path in defra_df['file']:
            full_path = self.base_path / file_path
            self.assertTrue(full_path.exists(), f"File does not exist: {full_path}")
            file_check_count += 1

    
    def test_defra_col(self):
        """Test DEFRA data column types and values."""
        print("\n" + "="*80)
        print("testing DEFRA data column tests.")
        print("="*80)
        
        defra_df = self.data_inventory.defra_data()
        
        # Verify source column values.
        self.assertTrue(all(defra_df['source'] == 'DEFRA'), "All source values should be 'DEFRA'")

        
        # Verify period format.
        self.assertTrue(all(defra_df['period'].str.contains('_')), "Period should contain underscore")
        self.assertTrue(all(defra_df['period'].str.match(r'\d{4}_\d{2}')), 
                       "Period should match YYYY_MM format")
        print(f"Sample periods: {defra_df['period'].unique()[:3].tolist()}")
        
        # Verify station is not empty.
        self.assertTrue(all(defra_df['station'].notna()), "Station names should not be null.")
        self.assertTrue(all(defra_df['station'].str.len() > 0), "Station names should not be empty.")
        print(f"Sample stations: {defra_df['station'].unique()[:3].tolist()}")
        
        # Verify pollutant is not empty.
        self.assertTrue(all(defra_df['pollutant'].notna()), "Pollutant names should not be null.")
        self.assertTrue(all(defra_df['pollutant'].str.len() > 0), "Pollutant names should not be empty.")
        print(f"Unique pollutants: {sorted(defra_df['pollutant'].unique().tolist())}")
        
        # Verify records is positive intg.
        self.assertTrue(all(defra_df['records'] > 0), "Record counts should be positive.")
        self.assertTrue(pd.api.types.is_integer_dtype(defra_df['records']), "Records should be integer type.")
        print(f"Min records: {defra_df['records'].min()}")
        print(f"Max records: {defra_df['records'].max()}")
        print(f"Median records: {defra_df['records'].median():.0f}")
        
        # Verify file paths start with expected directory.
        self.assertTrue(all(defra_df['file'].str.startswith('data/defra')), 
                       "File paths should start with 'data/defra'")
        self.assertTrue(all(defra_df['file'].str.contains('measurements')), 
                       "File paths should contain 'measurements'")


    def test_meteo_data(self):
        """Test the meteo_data method."""
        print("\n" + "="*80)
        print("Testing weather forecast data-METEO")
        print("="*80)
        
        meteo_df = self.data_inventory.meteo_data()
        
        # Check if the returned object is a df.
        self.assertIsInstance(meteo_df, pd.DataFrame)
        
        # Check if the DataFrame is not empty.
        self.assertFalse(meteo_df.empty, "Meteo DataFrame should not be empty")
        print(f"Total records: {len(meteo_df)}")
        
        # Check for expected columns.
        expected_columns = {'source', 'period', 'records', 'complete', 'file'}
        self.assertTrue(expected_columns.issubset(set(meteo_df.columns)))
        print(f"All expected columns present: {expected_columns}")
        
        # Print summary statistics.
        print(f"\nMeteo Data Summary:")
        print(f"Unique periods: {meteo_df['period'].nunique()}")
        print(f"Total data records: {meteo_df['records'].sum():,}")
        print(f"Average records per file: {meteo_df['records'].mean():.0f}")
        print(f"Complete files: {meteo_df['complete'].sum()}/{len(meteo_df)}")
        print(f"Incomplete files: {(~meteo_df['complete']).sum()}")
        
        # Verify all sources are labeled as 'METEO'.
        self.assertTrue(all(meteo_df['source'] == 'METEO'))

        
        # Check that 'complete' column is boolean.
        self.assertTrue(meteo_df['complete'].dtype == bool)
        print(f"Complete column: Boolean type")
        
        # Check if file paths exist.
        file_check_count = 0
        for file_path in meteo_df['file']:
            full_path = self.base_path / file_path
            self.assertTrue(full_path.exists(), f"File does not exist: {full_path}")
            file_check_count += 1
        print(f"All {file_check_count} file paths validated")
    
    def test_meteo_col(self):
        """Test meteorological data column types and values."""
        print("\n" + "="*80)
        print("Testing METEO data column tests.")
        print("="*80)
        
        meteo_df = self.data_inventory.meteo_data()
        
        # Verify source column values.
        self.assertTrue(all(meteo_df['source'] == 'METEO'), "All source values should be 'METEO'")
        print(f"Source column: All values = 'METEO'")
        
        # Verify period format.
        self.assertTrue(all(meteo_df['period'].str.match(r'\d{4}-\d{2}')), 
                       "Period should match YYYY-MM format")
        print(f"Sample periods: {meteo_df['period'].unique()[:3].tolist()}")
        print(f"Date range: {meteo_df['period'].min()} to {meteo_df['period'].max()}")
        
        # Verify records is positive intg.
        self.assertTrue(all(meteo_df['records'] > 0), "Record counts should be positive")
        self.assertTrue(pd.api.types.is_integer_dtype(meteo_df['records']), "Records should be integer type")
        print(f"Records column: All positive integers")
        print(f"Min records: {meteo_df['records'].min()}")
        print(f"Max records: {meteo_df['records'].max()}")
        print(f"Median records: {meteo_df['records'].median():.0f}")
        
        # Verify complete is boolean.
        self.assertTrue(meteo_df['complete'].dtype == bool, "Complete flag should be boolean")
        print(f"Complete flag: Boolean type")
        
        # Verify file paths start with expected directory.
        self.assertTrue(all(meteo_df['file'].str.startswith('data/meteo/raw')), 
                       "File paths should start with 'data/meteo/raw'")
        self.assertTrue(all(meteo_df['file'].str.contains('monthly')), 
                       "File paths should contain 'monthly'")
        
        #if any incomplete records exist.
        if not all(meteo_df['complete']):
            incomplete_files = meteo_df[~meteo_df['complete']]['file'].tolist()
            print(f"\n Incomplete meteo files found:")
            for file in incomplete_files:
                print(f"    - {file}")
        else:
            print(f"All meteorological files are complete.")
    
    def test_inventory_structure(self):
        """Test the overall inventory structure."""
        print("\n" + "="*80)
        print("testing inventory structure.")
        print("="*80)
        
        # Run all data collection methods.
        self.data_inventory.laqn_data()
        self.data_inventory.defra_data()
        self.data_inventory.meteo_data()
        
        # Check inventory has all expected keys.
        expected_keys = {'laqn', 'defra', 'meteo', 'summary'}
        self.assertTrue(expected_keys.issubset(set(self.data_inventory.inventory.keys())))
        print(f"Inventory has all expected keys: {expected_keys}")
        
        # Check each data source has df.
        self.assertIsInstance(self.data_inventory.inventory['laqn'], pd.DataFrame)
        self.assertIsInstance(self.data_inventory.inventory['defra'], pd.DataFrame)
        self.assertIsInstance(self.data_inventory.inventory['meteo'], pd.DataFrame)
        print(f"All data sources are DataFrames")
        
        # Print overall inventory summary.
        print(f"\nOverall Inventory Summary:")
        print(f"LAQN files: {len(self.data_inventory.inventory['laqn'])}")
        print(f"DEFRA files: {len(self.data_inventory.inventory['defra'])}")
        print(f"Meteo files: {len(self.data_inventory.inventory['meteo'])}")
        print(f"Total files: {len(self.data_inventory.inventory['laqn']) + len(self.data_inventory.inventory['defra']) + len(self.data_inventory.inventory['meteo'])}")
    
    def test_duplicates(self):
        """Test for duplicate records in each dataset."""
        print("\n" + "="*80)
        print("Testing for duplicate records in datasets.")
        print("="*80)
        
        laqn_df = self.data_inventory.laqn_data()
        defra_df = self.data_inventory.defra_data()
        meteo_df = self.data_inventory.meteo_data()
        
        # Check LAQN duplicates.
        laqn_duplicates = laqn_df.duplicated(subset=['period', 'site', 'pollutant'])
        self.assertFalse(laqn_duplicates.any(), "Found duplicate LAQN records.")
        print(f"LAQN No duplicates found (checked {len(laqn_df)} records.)")
        
        # Check DEFRA duplicates
        defra_duplicates = defra_df.duplicated(subset=['period', 'station', 'pollutant'])
        self.assertFalse(defra_duplicates.any(), "Found duplicate DEFRA records.")
        print(f"DEFRA No duplicates found (checked {len(defra_df)} records.)")
        
        # Check METEO duplicates
        meteo_duplicates = meteo_df.duplicated(subset=['period'])
        self.assertFalse(meteo_duplicates.any(), "Found duplicate METEO records.")
        print(f"METEO No duplicates found (checked {len(meteo_df)} records)")
        
        print(f"\nAll datasets passed duplicate validation.")

if __name__ == '__main__':
    unittest.main()
    # Run tests in definition order
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None
    suite = loader.loadTestsFromTestCase(TestDataInventory)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

