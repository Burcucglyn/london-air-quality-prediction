""" I will be cleaning and preparing datasets of LAQN and DEFRA for analysis."""

import pandas as pd
from pathlib import Path    
import os
from typing import Dict, List, Tuple, Optional
import logging
from tqdm import tqdm
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LAQNCleaner:
    """ Class for cleaning LAQN datasets.
     Processes hourly pollutant measurements from monitoring stations across London.
    Input: data/laqn/monthly_data/{year}_{month}/
    Output: data/laqn/clean/{year}_{month}/ """

    def __init__(self, base_dir: Path = None):
        """Initialize LAQN cleaner with directory paths."""
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        self.base_dir = base_dir
        self.raw_dir = base_dir / 'data' / 'laqn' / 'monthly_data'
        self.processed_dir = base_dir / 'data' / 'laqn' / 'processed'
        self.clean_dir = base_dir / 'data' / 'laqn' / 'clean'
        
        #new folder creation.
        self.clean_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"LAQN Cleaner initialized")
        logger.info(f"Raw data: {self.raw_dir}")
        logger.info(f"Output: {self.clean_dir}")

    def load_data(self, filename: str) -> pd.DataFrame:
        """ Load LAQN data from a CSV file. """
        file_path = self.data_dir / filename
        return pd.read_csv(file_path)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Clean the LAQN data. """
        # Example cleaning steps
        df = df.dropna()  # Remove missing values
        df['date'] = pd.to_datetime(df['date'])  # Convert date column to datetime
        return df

    def save_cleaned_data(self, df: pd.DataFrame, output_filename: str):
        """ Save the cleaned data to a CSV file. """
        output_path = self.data_dir / output_filename
        df.to_csv(output_path, index=False, encoding="utf-8")

class DEFARACleaner:
    """ Class for cleaning DEFRA datasets. """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def load_data(self, filename: str) -> pd.DataFrame:
        """ Load DEFRA data from a CSV file. """
        file_path = self.data_dir / filename
        return pd.read_csv(file_path)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Clean the DEFRA data. """
        # Example cleaning steps
        df = df.drop_duplicates()  # Remove duplicate rows
        df['measurement_date'] = pd.to_datetime(df['measurement_date'])  # Convert date column to datetime
        return df

    def save_cleaned_data(self, df: pd.DataFrame, output_filename: str):
        """ Save the cleaned data to a CSV file. """
        output_path = self.data_dir / output_filename
        df.to_csv(output_path, index=False, encoding="utf-8")


class MeteoCleaner:
    """ Class for cleaning Meteorological datasets. """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def load_data(self, filename: str) -> pd.DataFrame:
        """ Load Meteorological data from a CSV file. """
        file_path = self.data_dir / filename
        return pd.read_csv(file_path)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Clean the Meteorological data. """
        # Example cleaning steps
        df = df.dropna()  # Remove missing values
        df['obs_date'] = pd.to_datetime(df['obs_date'])  # Convert date column to datetime
        df = df[df['temperature'] >= -50]  # Remove unrealistic temperature values
        return df

    def save_cleaned_data(self, df: pd.DataFrame, output_filename: str):
        """ Save the cleaned data to a CSV file. """
        output_path = self.data_dir / output_filename
        df.to_csv(output_path, index=False, encoding="utf-8")