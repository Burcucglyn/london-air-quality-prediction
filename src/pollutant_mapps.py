"""This file contains functions to standardise pollutant names across data sources.
LAQN and DEFRA will have the same pollutant names."""

import pandas as pd
from pathlib import Path


class PollutantMapper:
    """Class to map and standardise pollutant names across LAQN and DEFRA data sources."""

    def __init__(self):
        """Initialise the PollutantMapper with paths and mappings."""
        self.data_dir = Path('data')
        self.laqn_dir = self.data_dir / 'laqn'
        self.defra_dir = self.data_dir / 'defra'

        #Definition common pollutant mapping dictionary.
        self.std_pollutants = {
            #LAQN mappings.
            'NO2': 'NO2',
            'NO': 'NO',
            'PM25': 'PM2.5',
            'PM10': 'PM10',
            'O3': 'O3',
            'SO2': 'SO2',
            'CO': 'CO',

            #DEFRA mappings common ones in both datasets first.
            'Nitrogen dioxide': 'NO2',
            'Nitrogen Dioxide': 'NO2',
            'Nitrogen_dioxide': 'NO2',
            'Nitric oxide': 'NO',
            'Nitrogen_monoxide': 'NO',
            'Nitrogen oxides': 'NOx',
            'Nitrogen_oxides': 'NOx',
            'PM2.5 Particulate': 'PM2.5',
            'Particulate_matter_less_than_2.5_micro_m': 'PM2.5',
            'PM10 Particulate': 'PM10',
            'Particulate_matter_less_than_10_micro_m': 'PM10',
            'Sulphur Dioxide': 'SO2',
            'Sulphur dioxide': 'SO2',
            'Sulphur_dioxide': 'SO2',
            'Ozone': 'O3',
            'Carbon Monoxide': 'CO',
            'Carbon monoxide': 'CO',
            'Carbon_monoxide': 'CO',
            
            # VOCs used simplified standard codes instead of their chemical names.
            'Benzene': 'Benzene',
            'Toluene': 'Toluene',
            'Ethylbenzene': 'Ethylbenzene',
            'Ethyl_benzene': 'Ethylbenzene',
            'o-Xylene': 'o-Xylene',
            'm,p-Xylene': 'm,p-Xylene',
            
            #Trimethylbenzenes.
            '1,2,3-Trimethylbenzene': '1,2,3-TMB',
            '1,2,4-Trimethylbenzene': '1,2,4-TMB',
            '1,3,5-Trimethylbenzene': '1,3,5-TMB',
            
            #Alkanes.
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
            
            #Alkenes
            'Ethene': 'Ethene',
            'Propene': 'Propene',
            '1-Butene': '1-Butene',
            'cis-2-Butene': 'cis-2-Butene',
            'trans-2-Butene': 'trans-2-Butene',
            '1-Pentene': '1-Pentene',
            'trans-2-Pentene': 'trans-2-Pentene',
            
            #Other VOCs
            '1,3-Butadiene': '1,3-Butadiene',
            '1.3_Butadiene': '1,3-Butadiene',
            'Isoprene': 'Isoprene',
            'Ethyne': 'Ethyne',
        }

    def std_pollutant(self, pollutant_name: str) -> str:
        """Standardise pollutant name to common format.
        
        Args:
            pollutant_name: Original pollutant name from dataset.
            
        Returns:
            Standardised pollutant name.
        """
        return self.std_pollutants.get(pollutant_name, pollutant_name)
    
    def get_common_pollutants(self, laqn_pollutants: set, defra_pollutants: set) -> set:
        """Get common pollutants between LAQN and DEFRA datasets.
        
        Args:
            laqn_pollutants: Set of LAQN pollutant names.
            defra_pollutants: Set of DEFRA pollutant names.
            
        Returns:
            Set of standardised common pollutants.
        """
        std_laqn = {self.std_pollutant(p) for p in laqn_pollutants}
        std_defra = {self.std_pollutant(p) for p in defra_pollutants}
        return std_laqn.intersection(std_defra)
    
    def mapping_report(self, laqn_pollutants: set, defra_pollutants: set) -> pd.DataFrame:
        """Generate a mapping report comparing pollutants across sources.
        
        Args:
            laqn_pollutants: Set of LAQN pollutant names.
            defra_pollutants: Set of DEFRA pollutant names.
            
        Returns:
            DataFrame with pollutant comparison.
        """
        common_pollutants = self.get_common_pollutants(laqn_pollutants, defra_pollutants)
        report_data = {
            'Pollutant': list(common_pollutants),
            'In_LAQN': [p in laqn_pollutants for p in common_pollutants],
            'In_DEFRA': [p in defra_pollutants for p in common_pollutants]
        }
        return pd.DataFrame(report_data)
    
    """Commented out LAQN func for now because i will be working on DEFRA."""
    
    # def std_laqn_pollutants(self, output_dir=Path('data/laqn/processed')):
    #     """Standardise LAQN pollutant names across all monthly files.
        
    #     Args:
    #         output_dir: Directory to save standardised files.
            
    #     Returns:
    #         Number of files processed.
    #     """
    #     laqn_monthly_dir = self.laqn_dir / 'monthly_data'
    #     output_path = Path(output_dir)
    #     output_path.mkdir(parents=True, exist_ok=True)

    #     processed_count = 0

    #     print(f"Standardising LAQN pollutants from {laqn_monthly_dir}")
    #     print(f"Output directory: {output_path}")

    #     #Iterate through all monthly folders.
    #     for year_month_dir in laqn_monthly_dir.glob('*'):
    #         if not year_month_dir.is_dir():
    #             continue
        
    #         year_month = year_month_dir.name
    #         print(f"\nProcessing {year_month}...")
            
    #         #Create output directory for each month.
    #         month_output_dir = output_path / year_month
    #         month_output_dir.mkdir(parents=True, exist_ok=True)

    #         #Process each csv file.
    #         for csv_file in year_month_dir.glob('*.csv'):
    #             try:
    #                 #Parse filename as site_species_start_end.csv
    #                 parts = csv_file.stem.split('_')
    #                 if len(parts) >= 2:
    #                     site_code = parts[0]
    #                     species_code = parts[1]
                        
    #                     #Standardise the species code
    #                     std_species = self.std_pollutant(species_code)
                        
    #                     #Read the file.
    #                     df = pd.read_csv(csv_file, encoding='utf-8')
                        
    #                     #Add standardised pollutant column.
    #                     df['pollutant_std'] = std_species
                        
    #                     # Create new filename with standardised species
    #                     new_filename = f"{site_code}_{std_species}_{'_'.join(parts[2:])}.csv"
    #                     output_file = month_output_dir / new_filename
                        
    #                     # Saving standardised file
    #                     df.to_csv(output_file, index=False)
    #                     processed_count += 1
                        
    #                     if processed_count % 100 == 0:
    #                         print(f"  Processed {processed_count} files...")
                
    #             except Exception as e:
    #                 print(f"  Error processing {csv_file.name}: {e}")
        
    #     print(f"\nCompleted. Standardised {processed_count} LAQN files.")
    #     print(f"Output saved to: {output_path}")

    #     return processed_count
    
    # """LAQN funmtion works I will be mirroring it for DEFRA dataset next."""



    def std_defra_pollutants(self, output_dir=Path('data/defra/processed')):
            """Standardise DEFRA pollutant names across all measurement files.
            
            Args:
                output_dir: Directory to save standardised files.
                
            Returns:
                Number of files processed.
            """
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            processed_count = 0

            print(f"Standardising DEFRA pollutants from {self.defra_dir}")
            print(f"Output directory: {output_path}")

            #Iterate through year measurement folders 2023measurements, 2024measurements, 2025measurements.
            for year_dir in self.defra_dir.glob('*measurements'):
                if not year_dir.is_dir():
                    continue
                
                year = year_dir.name.replace('measurements', '')
                print(f"\nProcessing {year}...")
                
                #Create output directory for each year.
                year_output_dir = output_path / f"{year}measurements"
                year_output_dir.mkdir(parents=True, exist_ok=True)
                
                #Iterate through station folders.
                for station_dir in year_dir.glob('*'):
                    if not station_dir.is_dir():
                        continue
                    
                    station_name = station_dir.name
                    
                    #Create output directory for each station.
                    station_output_dir = year_output_dir / station_name
                    station_output_dir.mkdir(parents=True, exist_ok=True)
                    
                    #Process each csv file.
                    for csv_file in station_dir.glob('*.csv'):
                        try:
                            #Parse filename as pollutant__yyyy_mm.csv.
                            parts = csv_file.stem.split('__')
                            if len(parts) == 2:
                                pollutant_name = parts[0]
                                date_part = parts[1]
                                
                                #Standardise the pollutant name.
                                std_pollutant_name = self.std_pollutant(pollutant_name)
                                
                                #Read the file.
                                df = pd.read_csv(csv_file, encoding='utf-8')
                                
                                #Add standardised pollutant column.
                                df['pollutant_std'] = std_pollutant_name
                                
                                #Create new filename with standardised pollutant.
                                new_filename = f"{std_pollutant_name}__{date_part}.csv"
                                output_file = station_output_dir / new_filename
                                
                                #Saving standardised file.
                                df.to_csv(output_file, index=False)
                                processed_count += 1
                                
                                if processed_count % 100 == 0:
                                    print(f"  Processed {processed_count} files...")
                        
                        except Exception as e:
                            print(f"  Error processing {csv_file.name}: {e}")
            
            print(f"\nCompleted. Standardised {processed_count} DEFRA files.")
            print(f"Output saved to: {output_path}")

            return processed_count


if __name__ == "__main__":
    mapper = PollutantMapper()
    
    # # Standardise LAQN files (commented out to prevent overwriting)
    # print("="*80)
    # print("STANDARDISING LAQN POLLUTANTS")
    # print("="*80)
    # laqn_count = mapper.std_laqn_pollutants()
    # print(f"\nTotal LAQN files processed: {laqn_count}")
    
    # Standardise DEFRA files
    print("="*80)
    print("STANDARDISING DEFRA POLLUTANTS")
    print("="*80)
    defra_count = mapper.std_defra_pollutants()
    print(f"\nTotal DEFRA files processed: {defra_count}")
    
    print("\n" + "="*80)
    print(f"TOTAL FILES PROCESSED: {defra_count}")
    print("="*80)
