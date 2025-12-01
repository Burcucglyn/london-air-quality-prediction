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

        results = [] #list to hold each record as a dict.

        for year_month_dir in laqn_path.glob('*'):
            if not year_month_dir.is_dir():
                continue

            year_month = year_month_dir.name # like year-month 2023_feb

            for csv_file in year_month_dir.glob('*.csv'):
                #parse year and month, site_species_startDate_endData.csv
                parts = csv_file.stem.split('_')
                if len(parts) >= 4:
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
    
    # Additional methods for defra_data, meteo_data, summary_data can be added similarly.
    def defra_data(self):
        """scanning func to see defra data structure."""

        #defra data path description
        defra_base = self.base_path / 'data' / 'defra'


        results = []
        for year_dir in defra_base.glob('*measurements'):
            year = year_dir.name.replace('measurements', '')
            
            for station_dir in year_dir.glob('*'):
                if not station_dir.is_dir():
                    continue
                    
                station_name = station_dir.name
                
                for csv_file in station_dir.glob('*.csv'):
                    # Parse filename: POLLUTANT__YYYY_MM.csv
                    parts = csv_file.stem.split('__')
                    if len(parts) == 2:
                        pollutant = parts[0]
                        period = parts[1]  # e.g., "2023_01"
                        
                        try:
                            df = pd.read_csv(csv_file)
                            record_count = len(df)
                            
                            results.append({
                                'source': 'DEFRA',
                                'period': period,
                                'station': station_name,
                                'pollutant': pollutant,
                                'records': record_count,
                                'file': str(csv_file.relative_to(self.base_path))
                            })
                        except Exception as e:
                            print(f"Error reading {csv_file}: {e}")
        
        self.inventory['defra'] = pd.DataFrame(results)
        return self.inventory['defra']
    
    def meteo_data(self):
        """Scan meteorological data structure."""
        meteo_base = self.base_path / 'data' / 'meteo' / 'raw'
        
        results = []
        for year_dir in meteo_base.glob('monthly*'):
            year = year_dir.name.replace('monthly', '')
            
            for csv_file in year_dir.glob('*.csv'):
                #Filename format YYYY-MM.csv
                try:
                    df = pd.read_csv(csv_file)
                    record_count = len(df)
                    
                    # Check for required columns
                    required_cols = ['date', 'temperature_2m', 'wind_speed_10m', 
                                   'surface_pressure', 'precipitation', 'relative_humidity_2m']
                    has_all_cols = all(col in df.columns for col in required_cols)
                    
                    results.append({
                        'source': 'METEO',
                        'period': csv_file.stem, 
                        'records': record_count,
                        'complete': has_all_cols,
                        'file': str(csv_file.relative_to(self.base_path))
                    })
                except Exception as e:
                    print(f"Error reading {csv_file}: {e}")
        
        self.inventory['meteo'] = pd.DataFrame(results)
        return self.inventory['meteo']
    
    def generate_summary(self):
        """Generate cross-source summary statistics."""
        summary = {
            'laqn': {
                'total_files': len(self.inventory['laqn']),
                'sites': self.inventory['laqn']['site'].nunique() if not self.inventory['laqn'].empty else 0,
                'pollutants': self.inventory['laqn']['pollutant'].unique().tolist() if not self.inventory['laqn'].empty else [],
                'periods': sorted(self.inventory['laqn']['period'].unique().tolist()) if not self.inventory['laqn'].empty else [],
                'total_records': int(self.inventory['laqn']['records'].sum()) if not self.inventory['laqn'].empty else 0
            },
            'defra': {
                'total_files': len(self.inventory['defra']),
                'stations': self.inventory['defra']['station'].nunique() if not self.inventory['defra'].empty else 0,
                'pollutants': self.inventory['defra']['pollutant'].unique().tolist() if not self.inventory['defra'].empty else [],
                'periods': sorted(self.inventory['defra']['period'].unique().tolist()) if not self.inventory['defra'].empty else [],
                'total_records': int(self.inventory['defra']['records'].sum()) if not self.inventory['defra'].empty else 0
            },
            'meteo': {
                'total_files': len(self.inventory['meteo']),
                'periods': sorted(self.inventory['meteo']['period'].unique().tolist()) if not self.inventory['meteo'].empty else [],
                'total_records': int(self.inventory['meteo']['records'].sum()) if not self.inventory['meteo'].empty else 0,
                'complete_months': int(self.inventory['meteo']['complete'].sum()) if not self.inventory['meteo'].empty else 0
            }
        }
        
        self.inventory['summary'] = summary
        return summary
    
    def save_inventory(self, output_dir='data/processed'):
        """Save inventory reports to disk."""
        output_path = self.base_path / output_dir
        output_path.mkdir(parents=True, exist_ok=True)
        
        if not self.inventory['laqn'].empty:
            self.inventory['laqn'].to_csv(output_path / 'laqn_inventory.csv', index=False)
        
        if not self.inventory['defra'].empty:
            self.inventory['defra'].to_csv(output_path / 'defra_inventory.csv', index=False)
        
        if not self.inventory['meteo'].empty:
            self.inventory['meteo'].to_csv(output_path / 'meteo_inventory.csv', index=False)
        
        with open(output_path / 'inventory_summary.json', 'w') as f:
            json.dump(self.inventory['summary'], f, indent=2)

        print(f"Inventory saved to {output_path}.")