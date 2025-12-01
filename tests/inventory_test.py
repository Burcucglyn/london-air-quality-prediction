"""Testing module for data_inventory.py file."""

import unittest
import pandas as pd
import numpy as np
import os
import sys
import json
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
        
        # Check for expected columns.
        expected_columns = {'source', 'period', 'records', 'complete', 'file'}
        self.assertTrue(expected_columns.issubset(set(meteo_df.columns)))
        print(f"All expected columns present: {expected_columns}")
        
        # Verify all sources are labeled as 'METEO'.
        self.assertTrue(all(meteo_df['source'] == 'METEO'))

        
        # Check that 'complete' column is boolean.
        self.assertTrue(meteo_df['complete'].dtype == bool)
        
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
        
        # Verify period format.
        self.assertTrue(all(meteo_df['period'].str.match(r'\d{4}-\d{2}')), 
                       "Period should match YYYY-MM format")
        print(f"Sample periods: {meteo_df['period'].unique()[:3].tolist()}")
        print(f"Date range: {meteo_df['period'].min()} to {meteo_df['period'].max()}")
        
        # Verify records is positive intg.
        self.assertTrue(all(meteo_df['records'] > 0), "Record counts should be positive")
        self.assertTrue(pd.api.types.is_integer_dtype(meteo_df['records']), "Records should be integer type")
        print(f"Min records: {meteo_df['records'].min()}")
        print(f"Max records: {meteo_df['records'].max()}")
        print(f"Median records: {meteo_df['records'].median():.0f}")
        
        # Verify complete is boolean.
        self.assertTrue(meteo_df['complete'].dtype == bool, "Complete flag should be boolean")

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
    
    def test_summary(self):
        """Test the summary method."""
        print("\n" + "="*80)
        print("Testing summary function.")
        print("="*80)
        
        self.data_inventory.laqn_data()
        self.data_inventory.defra_data()
        self.data_inventory.meteo_data()
        
        summary = self.data_inventory.generate_summary()
        
        self.assertIsInstance(summary, dict)
        print("Summary is a dictionary.")
        
        expected_keys = {'laqn', 'defra', 'meteo'}
        self.assertTrue(expected_keys.issubset(set(summary.keys())))
        print(f"Summary has all expected keys: {expected_keys}.")
        
        laqn_summary = summary['laqn']
        laqn_expected_keys = {'total_files', 'sites', 'pollutants', 'periods', 'total_records'}
        self.assertTrue(laqn_expected_keys.issubset(set(laqn_summary.keys())))
        print("LAQN summary has correct structure.")
        
        self.assertIsInstance(laqn_summary['total_files'], int)
        self.assertIsInstance(laqn_summary['sites'], int)
        self.assertIsInstance(laqn_summary['pollutants'], list)
        self.assertIsInstance(laqn_summary['periods'], list)
        self.assertIsInstance(laqn_summary['total_records'], int)
        print(f"Total LAQN files: {laqn_summary['total_files']}.")
        print(f"Total sites: {laqn_summary['sites']}.")
        print(f"Total records: {laqn_summary['total_records']:,}.")
        
        defra_summary = summary['defra']
        defra_expected_keys = {'total_files', 'stations', 'pollutants', 'periods', 'total_records'}
        self.assertTrue(defra_expected_keys.issubset(set(defra_summary.keys())))
        print("DEFRA summary has correct structure.")
        
        self.assertIsInstance(defra_summary['total_files'], int)
        self.assertIsInstance(defra_summary['stations'], int)
        self.assertIsInstance(defra_summary['pollutants'], list)
        self.assertIsInstance(defra_summary['periods'], list)
        self.assertIsInstance(defra_summary['total_records'], int)
        print(f"Total DEFRA files: {defra_summary['total_files']}.")
        print(f"Total stations: {defra_summary['stations']}.")
        print(f"Total records: {defra_summary['total_records']:,}.")
        
        meteo_summary = summary['meteo']
        meteo_expected_keys = {'total_files', 'periods', 'total_records', 'complete_months'}
        self.assertTrue(meteo_expected_keys.issubset(set(meteo_summary.keys())))
        print("METEO summary has correct structure.")
        
        self.assertIsInstance(meteo_summary['total_files'], int)
        self.assertIsInstance(meteo_summary['periods'], list)
        self.assertIsInstance(meteo_summary['total_records'], int)
        self.assertIsInstance(meteo_summary['complete_months'], int)
        print(f"Total METEO files: {meteo_summary['total_files']}.")
        print(f"Complete months: {meteo_summary['complete_months']}/{meteo_summary['total_files']}.")
        print(f"Total records: {meteo_summary['total_records']:,}.")
        
        self.assertEqual(self.data_inventory.inventory['summary'], summary)
        print("Summary stored in inventory correctly.")
        
        print("\nSummary generation passed all validations.")

    def test_save_inventory(self):
        """Test the save_inventory method."""
        print("\n" + "="*80)
        print("Testing save_inventory function.")
        print("="*80)
        
        self.data_inventory.laqn_data()
        self.data_inventory.defra_data()
        self.data_inventory.meteo_data()
        self.data_inventory.generate_summary()
        
        test_output_dir = 'data/processed/test_output'
        output_path = self.base_path / test_output_dir

        
        if output_path.exists():
            for file in output_path.glob('*'):
                file.unlink()
            output_path.rmdir()
        
        self.data_inventory.save_inventory(output_dir=test_output_dir)
        
        self.assertTrue(output_path.exists())
        print(f"Output directory created: {output_path}.")
        
        laqn_csv = output_path / 'laqn_inventory.csv'
        self.assertTrue(laqn_csv.exists())
        print("LAQN inventory CSV created.")
        
        laqn_loaded = pd.read_csv(laqn_csv)
        self.assertEqual(len(laqn_loaded), len(self.data_inventory.inventory['laqn']))
        expected_cols = {'source', 'period', 'site', 'pollutant', 'records', 'file'}
        self.assertTrue(expected_cols.issubset(set(laqn_loaded.columns)))
        print(f"LAQN CSV has {len(laqn_loaded)} records with correct columns.")
        
        defra_csv = output_path / 'defra_inventory.csv'
        self.assertTrue(defra_csv.exists())
        print("DEFRA inventory CSV created.")
        
        defra_loaded = pd.read_csv(defra_csv)
        self.assertEqual(len(defra_loaded), len(self.data_inventory.inventory['defra']))
        expected_cols = {'source', 'period', 'station', 'pollutant', 'records', 'file'}
        self.assertTrue(expected_cols.issubset(set(defra_loaded.columns)))
        print(f"DEFRA CSV has {len(defra_loaded)} records with correct columns.")
        
        meteo_csv = output_path / 'meteo_inventory.csv'
        self.assertTrue(meteo_csv.exists())
        print("METEO inventory CSV created.")
        
        meteo_loaded = pd.read_csv(meteo_csv)
        self.assertEqual(len(meteo_loaded), len(self.data_inventory.inventory['meteo']))
        expected_cols = {'source', 'period', 'records', 'complete', 'file'}
        self.assertTrue(expected_cols.issubset(set(meteo_loaded.columns)))
        print(f"METEO CSV has {len(meteo_loaded)} records with correct columns.")
        
        summary_json = output_path / 'inventory_summary.json'
        self.assertTrue(summary_json.exists())
        print("Summary JSON created.")
        
        with open(summary_json, 'r') as f:
            summary_loaded = json.load(f)
        
        self.assertEqual(summary_loaded, self.data_inventory.inventory['summary'])
        expected_keys = {'laqn', 'defra', 'meteo'}
        self.assertTrue(expected_keys.issubset(set(summary_loaded.keys())))
        print(f"JSON has correct structure with keys: {expected_keys}.")
        
        self.assertIsInstance(summary_loaded['laqn']['total_files'], int)
        self.assertIsInstance(summary_loaded['defra']['total_files'], int)
        self.assertIsInstance(summary_loaded['meteo']['total_files'], int)
        print("JSON data types are correct. All integers for counts.")
        
        print("\nAll inventory files saved and validated successfully.")
        
        for file in output_path.glob('*'):
            file.unlink()
        output_path.rmdir()
        print("Test output cleaned up.")
    
    def test_duplicates(self):
        """Test for duplicate records in each dataset."""
        print("\n" + "="*80)
        print("Testing for duplicate records in datasets.")
        print("="*80)
        
        laqn_df = self.data_inventory.laqn_data()
        defra_df = self.data_inventory.defra_data()
        meteo_df = self.data_inventory.meteo_data()
        
        laqn_duplicates = laqn_df.duplicated(subset=['period', 'site', 'pollutant'])
        self.assertFalse(laqn_duplicates.any(), "Found duplicate LAQN records.")
        print(f"LAQN No duplicates found (checked {len(laqn_df)} records.)")
        
        defra_duplicates = defra_df.duplicated(subset=['period', 'station', 'pollutant'])
        self.assertFalse(defra_duplicates.any(), "Found duplicate DEFRA records.")
        print(f"DEFRA No duplicates found (checked {len(defra_df)} records.)")
        
        meteo_duplicates = meteo_df.duplicated(subset=['period'])
        self.assertFalse(meteo_duplicates.any(), "Found duplicate METEO records.")
        print(f"METEO No duplicates found (checked {len(meteo_df)} records)")
        
        print(f"\nAll datasets passed duplicate validation.")

if __name__ == '__main__':
    unittest.main(verbosity=2)


    """Terminal output below:
    test_defra_col (__main__.TestDataInventory.test_defra_col)
Test DEFRA data column types and values. ... 
================================================================================
testing DEFRA data column tests.
================================================================================
Sample periods: ['2023_03', '2023_09', '2023_02']
Sample stations: ['London_Marylebone_Road', 'London_Westminster', 'London_N._Kensington']
Unique pollutants: ['1,2,3-Trimethylbenzene', '1,2,4-Trimethylbenzene', '1,3,5-Trimethylbenzene', '1-Butene', '1-Pentene', 
'1.3_Butadiene', 'Benzene', 'Carbon_monoxide', 'Ethane', 'Ethene', 'Ethyl_benzene', 'Ethyne', 'Isoprene', 'Nitrogen_dioxide', 'Nitrogen_monoxide', 'Nitrogen_oxides', 'Ozone', 'Particulate_matter_less_than_10_micro_m', 'Particulate_matter_less_than_2.5_micro_m', 'Propane', 'Propene', 'Sulphur_dioxide', 'Toluene', 'cis-2-Butene', 'i-Butane', 'i-Hexane', 'i-Octane', 'i-Pentane', 'm,p-Xylene', 'n-Butane', 'n-Heptane', 'n-Hexane', 'n-Octane', 'n-Pentane', 'o-Xylene', 'trans-2-Butene', 'trans-2-Pentene']                                                                                                                Min records: 81
Max records: 746
Median records: 726
ok
test_defra_data (__main__.TestDataInventory.test_defra_data)
Test the defra_data method. ... 
================================================================================
Testing DEFRA data
================================================================================
Total records: 3563
All expected columns present: {'pollutant', 'records', 'station', 'file', 'source', 'period'}
ok
test_duplicates (__main__.TestDataInventory.test_duplicates)
Test for duplicate records in each dataset. ... 
================================================================================
Testing for duplicate records in datasets.
================================================================================
LAQN No duplicates found (checked 8709 records.)
DEFRA No duplicates found (checked 3563 records.)
METEO No duplicates found (checked 35 records)

All datasets passed duplicate validation.
ok
test_laqn_col (__main__.TestDataInventory.test_laqn_col)
Test LAQN data column types and values. ... 
================================================================================
Test LAQN data column:
================================================================================
Sample periods: ['2023_mar', '2025_feb', '2024_feb']
Unique pollutants: ['CO', 'NO2', 'O3', 'PM10', 'PM25', 'SO2']
Min records: 432
Max records: 720
Median records: 720
ok
test_laqn_data (__main__.TestDataInventory.test_laqn_data)
Test the laqn_data method. ... 
================================================================================
Running test_laqn_data:
================================================================================
Total records: 8709
 All expected col: {'pollutant', 'records', 'file', 'source', 'site', 'period'} are present.
ok
test_meteo_col (__main__.TestDataInventory.test_meteo_col)
Test meteorological data column types and values. ... 
================================================================================
Testing METEO data column tests.
================================================================================
Sample periods: ['2023-09', '2023-08', '2023-11']
Date range: 2023-01 to 2025-11
Min records: 672
Max records: 744
Median records: 744
All meteorological files are complete.
ok
test_meteo_data (__main__.TestDataInventory.test_meteo_data)
Test the meteo_data method. ... 
================================================================================
Testing weather forecast data-METEO
================================================================================
All expected columns present: {'records', 'file', 'source', 'complete', 'period'}
All 35 file paths validated
ok
test_save_inventory (__main__.TestDataInventory.test_save_inventory)
Test the save_inventory method. ... 
================================================================================
Testing save_inventory function.
================================================================================
Output directory created: /Users/burdzhuchaglayan/Desktop/data science projects/air-pollution-levels/data/processed/test_ou
tput.                                                                                                                      LAQN inventory CSV created.
LAQN CSV has 8709 records with correct columns.
DEFRA inventory CSV created.
DEFRA CSV has 3563 records with correct columns.
METEO inventory CSV created.
METEO CSV has 35 records with correct columns.
Summary JSON created.
JSON has correct structure with keys: {'laqn', 'defra', 'meteo'}.
JSON data types are correct. All integers for counts.

All inventory files saved and validated successfully.
Test output cleaned up.
ok
test_summary (__main__.TestDataInventory.test_summary)
Test the summary method. ... 
================================================================================
Testing summary function.
================================================================================
Summary is a dictionary.
Summary has all expected keys: {'laqn', 'defra', 'meteo'}.
LAQN summary has correct structure.
Total LAQN files: 8709.
Total sites: 84.
Total records: 6,085,344.
DEFRA summary has correct structure.
Total DEFRA files: 3563.
Total stations: 18.
Total records: 2,454,011.
METEO summary has correct structure.
Total METEO files: 35.
Complete months: 35/35.
Total records: 25,560.
Summary stored in inventory correctly.

Summary generation passed all validations.
ok

----------------------------------------------------------------------
Ran 9 tests in 42.681s

OK

    """

