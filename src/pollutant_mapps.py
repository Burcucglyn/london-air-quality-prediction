"""This file will be contain functions for change the poollutant names in each source to a common standard.
LAQN, DEFRA will be have the same pollutant names."""

import pandas as pd
from pathlib import Path


class PollutantMapper:
    """class to mapping and standertise pollutant names accros laqn and defra data sources."""
    def __init__(self):
        """Initialize the PollutantMapper with paths and mappings."""
        self.data_dir = Path('data')
        self.laqn_dir = self.data_dir / 'LAQN'
        self.defra_dir = self.data_dir / 'DEFRA'

    #defining a common pollutant mapping dictionary.

    std_pollutants ={
        #laqn mappings
        'NO2':'NO2',
        'NO':'NO',
        'PM25':'PM2.5',
        'PM10':'PM10',
        'O3':'O3',
        'SO2':'SO2',
        'CO':'CO',

        #defra mappings below: first the common ones in both datasets.
        'Nitrogen dioxide': 'NO2',
        'Nitrogen Dioxide': 'NO2',
        'Nitric oxide': 'NO',
        'Nitrogen oxides': 'NOx',
        'PM2.5 Particulate': 'PM2.5',
        'PM10 Particulate': 'PM10',
        'Sulphur Dioxide': 'SO2',
        'Sulphur dioxide': 'SO2',
        'Ozone': 'O3',
        'Carbon Monoxide': 'CO',
        'Carbon monoxide': 'CO',
        
        #VOCs used simplified standard codes isntead of chemical symbols.
        'Benzene': 'Benzene',
        'Toluene': 'Toluene',
        'Ethylbenzene': 'Ethylbenzene',
        'Ethyl_benzene': 'Ethylbenzene',
        'o-Xylene': 'o-Xylene',
        'm,p-Xylene': 'm,p-Xylene',
        
        #Trimethylbenzenes
        '1,2,3-Trimethylbenzene': '1,2,3-TMB',
        '1,2,4-Trimethylbenzene': '1,2,4-TMB',
        '1,3,5-Trimethylbenzene': '1,3,5-TMB',
        
        #Alkanes
        'Ethane': 'Ethane',
        'Propane': 'Propane',
        'n-Butane': 'n-Butane',
        'i-Butane': 'i-Butane',
        'n-Pentane': 'n-Pentane',
        'i-Pentane': 'i-Pentane',
        'n-Hexane': 'n-Hexane',
        'i-Hexane': 'i-Hexane',
        'n-Heptane': 'n-Heptane',
        'n-Octane': 'n-Octane',
        'i-Octane': 'i-Octane',
        'Ethene': 'Ethene',
        'Propene': 'Propene',
        '1-Butene': '1-Butene',
        'cis-2-Butene': 'cis-2-Butene',
        '1-Pentene': '1-Pentene',
        
        #Other VOCs
        '1,3-Butadiene': '1,3-Butadiene',
        'Isoprene': 'Isoprene',
        'Ethyne': 'Ethyne',
    }

    def standardize_pollutant(self, pollutant_name: str) -> str:
        """Method to standardize pollutant names."""
        return self.std_pollutants.get(pollutant_name, pollutant_name)
    
    def get_common_pollutants(self, laqn_pollutants: set, defra_pollutants: set) -> set:
        """Method to get common pollutants between LAQN and DEFRA datasets."""
        standardized_laqn = {self.standardize_pollutant(p) for p in laqn_pollutants}
        standardized_defra = {self.standardize_pollutant(p) for p in defra_pollutants}
        return standardized_laqn.intersection(standardized_defra)
    
    def mapping_report(self, laqn_pollutants: set, defra_pollutants: set) -> pd.DataFrame:
        """Method to generate a mapping report."""
        common_pollutants = self.get_common_pollutants(laqn_pollutants, defra_pollutants)
        report_data = {
            'Pollutant': list(common_pollutants),
            'In_LAQN': [p in laqn_pollutants for p in common_pollutants],
            'In_DEFRA': [p in defra_pollutants for p in common_pollutants]
        }
        return pd.DataFrame(report_data)