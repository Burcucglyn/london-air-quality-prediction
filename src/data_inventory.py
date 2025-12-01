"""Detailed inventory of data files used in the project.
generates a structured dictionary containing metadata about each data file."""

#starting with imports.
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

class DataInventory:
    """Class to create and manage a data inventory for the project."""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.inventory = {
            'laqn':{},
            'defra':{},
            'meteo':{},
            'summary':{}
        }

    def laqn_data(self):
        """ scanning function to see laqn monthly data structure."""
        laqn_path = self.base_path / 'data' / 'laqn'/ 'monthly_data'

        results = {}

        for year_month_dir in laqn_path.glob('*'):
            if not year_month_dir.is_dir():
                continue

            year_month = year_month_dir.name # like year-month 2023_feb

        for csv_file in year_month_dir.glob('*.csv'):
            #parse year and month, site_species_startDate_endData.csv
            parts = csv_file.stem.split('_')
            if len(parts) != 4:
                site_code = parts[0]
                species_code = parts[1]

                #read the file to get record count and date range
                try:
                    df = pd.read_csv(csv_file)
                    record_count = len(df)

                    results.append({
                        'source':'LAQN',
                        'period':year_month,
                        'site':site_code,
                        'pollutant':species_code,
                        'records':record_count,
                        'file':str(csv_file.relative_to(self.base_path))
                    })
                except Exception as e:
                    print(f"Error reading {csv_file}: {e}")
            
        self.inventory['laqn'] = pd.DataFrame(results)
        return self.inventory['laqn']