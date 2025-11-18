"""Datta analysis functions for air pollution and weather data.
I have both pollution and weather datasets collected from APIs.
This file will be  used for analysing the dataset."""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime



# ------- LAQN Pollution Data Analysis Class below: -------
# ---------------------------------------------------------

class LAQNDataAnalyse:
    """Class for analyzing LAQN pollution data."""
    
    def __init__(self, pollution_data: pd.DataFrame):
        self.pollution_data = pollution_data

    def basic_summary(self) -> pd.DataFrame:
        """Generate basic summary statistics of the pollution data."""
        return self.pollution_data.describe()

    def LAQN_data_analysis(self) -> dict: 
        """Perform comprehensive analysis on LAQN pollution data.
        Returns:
            dict: Analyse results including summary stats and insights.
        """
        analysis_results = {}
        
        # basic summary statistics 
        analysis_results['basic_summary'] = self.pollution_data.describe()
        
        # pollution-specific analysis
        analysis_results['data_shape'] = self.pollution_data.shape
        analysis_results['sites'] = self.pollution_data['SiteCode'].unique()
        analysis_results['pollutants'] = self.pollution_data['SpeciesCode'].unique()
        
        # missing data analysis
        analysis_results['missing_values'] = self.pollution_data['@Value'].isnull().sum()
        analysis_results['missing_percentage'] = (self.pollution_data['@Value'].isnull().sum() / len(self.pollution_data)) * 100
        
        # date range analysis
        self.pollution_data['datetime'] = pd.to_datetime(self.pollution_data['@MeasurementDateGMT'])
        analysis_results['date_range'] = {
            'start': self.pollution_data['datetime'].min(),
            'end': self.pollution_data['datetime'].max()
        }
        
        # pollutant-specific statistics
        pollutant_stats = {}
        for pollutant in self.pollution_data['SpeciesCode'].unique():
            subset = self.pollution_data[self.pollution_data['SpeciesCode'] == pollutant]['@Value']
            pollutant_stats[pollutant] = {
                'mean': subset.mean(),
                'std': subset.std(),
                'min': subset.min(),
                'max': subset.max(),
                'count': subset.count()
            }
        analysis_results['pollutant_statistics'] = pollutant_stats
        
        return analysis_results

    def display_analysis_results(self, analysis_results: dict):  # Fixed: added self
        """Display analysis results in readable format"""
        print("=== LAQN POLLUTION DATA ANALYSIS ===")
        print(f"Dataset shape: {analysis_results['data_shape']}")
        print(f"Sites: {analysis_results['sites']}")
        print(f"Pollutants: {analysis_results['pollutants']}")
        print(f"Missing values: {analysis_results['missing_values']} ({analysis_results['missing_percentage']:.1f}%)")
        print(f"Date range: {analysis_results['date_range']['start']} to {analysis_results['date_range']['end']}")
        
        print("\nPollutant Statistics:")
        for pollutant, stats in analysis_results['pollutant_statistics'].items():
            print(f"  {pollutant}: Mean={stats['mean']:.1f}, Min={stats['min']:.1f}, Max={stats['max']:.1f} µg/m³")

if __name__ == "__main__":
    # load your data
    pollution_df = pd.read_csv('data/raw/pollution_data_2023year.csv')
    
    # create analyzer instance and run analysis
    analyzer = LAQNDataAnalyse(pollution_df)
    results = analyzer.LAQN_data_analysis()
    analyzer.display_analysis_results(results)
