import os
import pandas as pd
from pathlib import Path
#sys path modification to allow imports from
import sys

"""Since the test file is located in tests/ directory, and functions to be tested are in src/ directory commented."""
#to make the paths portable across different OS, I used os.path.join to create proj_root
# proj_root = os.path.join(os.path.dirname(__file__), '..')
# project root path below
# sys.path.insert(0, os.path.abspath(proj_root))

# project root as a Path 
proj_root = Path(__file__).resolve().parent.parent
# add project root to sys.path for imports
sys.path.insert(0, str(proj_root))



from src.laqn_analyse import SiteSpeciesAnalysis

def test_site_species_analysis():
    # Define the path to the dataset
    data_path = Path(proj_root) / 'data' / 'laqn' / 'sites_species_london.csv'
    
    # Check if the file exists
    if not os.path.exists(data_path):
        print(f"Test failed: File not found at {data_path}")
        return

    # Initialize the analyzer
    analyzer = SiteSpeciesAnalysis(data_path)

    # Test loading the data
    try:
        analyzer.load_data()
        print("Test passed: Data loaded successfully")
    except Exception as e:
        print(f"Test failed: Error loading data - {e}")
        return

    """Below tests are commented out to avoid redundant file creation during routine testing.
    Uncomment them when you want to specifically test the filtering and saving functionality."""
    # Test getting active sites and species
    try:
        active_sites = analyzer.get_actv_sites_species(save_to_csv=False)
        print("Test passed: Active sites and species filtered successfully")
        print(f"Active sites DataFrame:\n{active_sites.head()}")
    except Exception as e:
        print(f"Test failed: Error filtering active sites and species - {e}")
        return

    # Save the active sites to a CSV file and checks if file saved and created successfully.
    output_path = proj_root / "data" / "laqn" / "actv_sites_species.csv"
    try:
        analyzer.get_actv_sites_species(save_to_csv=True, output_path=str(output_path))
        print(f"Saved canonical file to {output_path}")
    except Exception as e:
        print(f"Error saving canonical file - {e}")

if __name__ == "__main__":
    test_site_species_analysis()