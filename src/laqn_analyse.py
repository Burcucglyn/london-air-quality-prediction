"""Analyse the LAQN data to identify active measurement sites and species."""

import pandas as pd
from pathlib import Path


class SiteSpeciesAnalysis:
    """Class to analyse and export a new table from data/laqn/sites_species_london.csv."""

    def __init__(self, data_path):
        """Initialize the analyzer with the dataset path.
        
        Args:
            data_path (str): Path to the sites_species CSV file
        """
        self.data_path = data_path
        self.df = None

    def load_data(self):
        """Load data from the CSV file."""
        try:
            self.df = pd.read_csv(self.data_path, encoding="utf-8")
            print(f"Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        except FileNotFoundError:
            print(f"Error: File not found at {self.data_path}")
            raise
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def get_actv_sites_species(self, save_to_csv=True, output_path="data/laqn/active_sites_species.csv"):
        """Filter for currently active sites (DateClosed is empty/null).
        Returns site code, site name, site type, species code, and species name.
        
        Args:
            save_to_csv (bool): Whether to save the result to CSV
            output_path (str): Path where to save the CSV file
            
        Returns:
            pd.DataFrame: Filtered dataframe with active sites and species
        """
        if self.df is None:
            print("Data not loaded. Loading data...")
            self.load_data()

        # Filter for sites where DateClosed is null (still active)
        actv_sites = self.df[self.df['@DateClosed'].isnull()].copy()

        # Select only the required columns
        actv_sites_filtered = actv_sites[[
            '@SiteCode',
            '@SiteName', 
            '@SiteType',
            '@SpeciesCode',
            '@SpeciesDescription',
            '@Latitude',
            '@Longitude'
        ]].copy()

        # Rename columns for cleaner output
        actv_sites_filtered = actv_sites_filtered.rename(columns={
            '@SiteCode': 'SiteCode',
            '@SiteName': 'SiteName',
            '@SiteType': 'SiteType',
            '@SpeciesCode': 'SpeciesCode',
            '@SpeciesDescription': 'SpeciesName',
            '@Latitude': 'Latitude',
            '@Longitude': 'Longitude'
        })

        print(f"Active sites found: {actv_sites_filtered['SiteCode'].nunique()} unique sites")
        print(f"Total site-species combinations: {len(actv_sites_filtered)}")

        if save_to_csv:
            try:
                # Create datasets directory if it doesn't exist
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                actv_sites_filtered.to_csv(output_path, index=False)
                print(f"\nSaved to: {output_path}")
            except Exception as e:
                print(f"Error saving to CSV: {e}")
                raise

        return actv_sites_filtered