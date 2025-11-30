import requests
import pandas as pd
import json
import os
from datetime import datetime


def create_structured_dataframe(raw_data):
    """Create a structured DataFrame from the nested LAQN data"""
    if 'SiteObjectives.Site' not in raw_data.columns:
        print("No SiteObjectives.Site data found")
        return None
    
    sites_data = raw_data['SiteObjectives.Site'].iloc[0]
    structured_data = []
    
    for site in sites_data:
        site_code = site.get('@SiteCode', 'N/A')
        site_name = site.get('@SiteName', 'N/A')
        
        # Extract objectives/species data
        if 'Objective' in site:
            objectives = site['Objective']
            if isinstance(objectives, list):
                # Multiple objectives for this site
                for obj in objectives:
                    row = {
                        'SiteCode': site_code,
                        'SiteName': site_name,
                        'SpeciesCode': obj.get('@SpeciesCode', obj.get('@Species', 'Unknown')),
                        'SpeciesDescription': obj.get('@SpeciesDescription', 'N/A'),
                        'ObjectiveType': obj.get('@ObjectiveType', 'N/A'),
                        'Value': obj.get('@Value', 'N/A'),
                        'Unit': obj.get('@Unit', 'N/A'),
                        'Guideline': obj.get('@Guideline', 'N/A'),
                        'Period': obj.get('@Period', 'N/A')
                    }
                    structured_data.append(row)
            else:
                # Single objective for this site
                row = {
                    'SiteCode': site_code,
                    'SiteName': site_name,
                    'SpeciesCode': objectives.get('@SpeciesCode', objectives.get('@Species', 'Unknown')),
                    'SpeciesDescription': objectives.get('@SpeciesDescription', 'N/A'),
                    'ObjectiveType': objectives.get('@ObjectiveType', 'N/A'),
                    'Value': objectives.get('@Value', 'N/A'),
                    'Unit': objectives.get('@Unit', 'N/A'),
                    'Guideline': objectives.get('@Guideline', 'N/A'),
                    'Period': objectives.get('@Period', 'N/A')
                }
                structured_data.append(row)
        else:
            # Site with no objectives data
            row = {
                'SiteCode': site_code,
                'SiteName': site_name,
                'SpeciesCode': 'No data',
                'SpeciesDescription': 'N/A',
                'ObjectiveType': 'N/A',
                'Value': 'N/A',
                'Unit': 'N/A',
                'Guideline': 'N/A',
                'Period': 'N/A'
            }
            structured_data.append(row)
    
    df = pd.DataFrame(structured_data)
    return df

def fetch_laqn_data():
    """ Test function to fetch data from LAQN API to have better understanding
    of available data structure and formats."""
    url = "https://api.erg.ic.ac.uk/AirQuality/Annual/MonitoringObjective/GroupName={GROUPNAME}/Json"
    groupname = "London"
    url = url.replace("{GROUPNAME}", groupname)
    print(f"Fetching data from URL: {url}")

    try:
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Handle UTF-8 BOM issue by decoding the content properly
            try:
                json_data = response.json()
            except ValueError as json_error:
                print(f"JSON parsing failed, trying to handle BOM: {json_error}")
                # Remove BOM and parse JSON manually
                import json
                content = response.content.decode('utf-8-sig')
                json_data = json.loads(content)
            
            print(f"Success. JSON keys: {list(json_data.keys()) if isinstance(json_data, dict) else 'Not a dict'}")
            df = pd.json_normalize(json_data)
            print(f"DataFrame shape: {df.shape}")
            return df
        else:
            print(f" HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f" Request failed with exception: {e}")
        return None

if __name__ == "__main__":
    # Fetch raw data
    raw_data = fetch_laqn_data()
    
    if raw_data is not None:
        print("\n=== RAW DATA INFO ===")
        print(f"Raw DataFrame shape: {raw_data.shape}")
        print(f"Raw DataFrame columns: {list(raw_data.columns)}")
        
        # Create structured DataFrame
        print("\n=== CREATING STRUCTURED DATAFRAME ===")
        structured_df = create_structured_dataframe(raw_data)
        
        if structured_df is not None:
            print(f"\nStructured DataFrame created successfully!")
            print(f"Total sites: {structured_df['SiteCode'].nunique()}")
            print(f"Total species: {structured_df['SpeciesCode'].nunique()}")
            
            print("\n=== AVAILABLE SPECIES AT EACH SITE ===")
            print("="*80)
            
            # Create data structure for JSON
            sites_species_data = {
                "metadata": {
                    "total_sites": int(structured_df['SiteCode'].nunique()),
                    "total_species": int(structured_df['SpeciesCode'].nunique()),
                    "extraction_date": datetime.now().isoformat(),
                    "data_source": "London Air Quality Network (LAQN)"
                },
                "sites": [],
                "species_summary": {}
            }
            
            # Group by site and collect species data
            site_groups = structured_df.groupby(['SiteCode', 'SiteName'])['SpeciesCode'].apply(list).reset_index()
            
            for idx, row in site_groups.iterrows():
                site_code = row['SiteCode']
                site_name = row['SiteName']
                species_list = [s for s in row['SpeciesCode'] if s != 'No data']
                
                print(f"\nSite: {site_code} - {site_name}")
                if species_list:
                    unique_species = sorted(set(species_list))
                    print(f"   Species: {', '.join(unique_species)}")
                    
                    sites_species_data["sites"].append({
                        "site_code": site_code,
                        "site_name": site_name,
                        "species": unique_species,
                        "species_count": len(unique_species)
                    })
                else:
                    print("   Species: No monitoring data available")
                    sites_species_data["sites"].append({
                        "site_code": site_code,
                        "site_name": site_name,
                        "species": [],
                        "species_count": 0
                    })
            
            # Create species summary
            all_species = structured_df[structured_df['SpeciesCode'] != 'No data']['SpeciesCode'].unique()
            species_counts = structured_df[structured_df['SpeciesCode'] != 'No data']['SpeciesCode'].value_counts()
            
            print("\n" + "="*80)
            print(f"\n=== SPECIES SUMMARY ===")
            print(f"All monitored species: {sorted(all_species)}")
            
            print(f"\n=== SPECIES FREQUENCY ===")
            for species, count in species_counts.items():
                print(f"{species}: {count} site(s)")
                sites_species_data["species_summary"][species] = int(count)
            
            # Save to JSON file in data directory
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            json_file_path = os.path.join(data_dir, "sites_species_data.json")
            
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(sites_species_data, f, indent=2, ensure_ascii=False)
            
            print(f"\nJSON data saved to: {json_file_path}")
            print(f"JSON file contains {len(sites_species_data['sites'])} sites and {len(sites_species_data['species_summary'])} species")
            
            # Save only one comprehensive CSV file with enhanced structure
            csv_file_path = os.path.join(data_dir, "sites_species_data.csv")
            
            # Enhance the structured DataFrame with additional summary columns
            enhanced_df = structured_df.copy()
            
            # Add site summary information
            site_species_counts = structured_df.groupby('SiteCode')['SpeciesCode'].nunique().to_dict()
            enhanced_df['SiteSpeciesCount'] = enhanced_df['SiteCode'].map(site_species_counts)
            
            # Add species frequency information
            species_frequency = structured_df['SpeciesCode'].value_counts().to_dict()
            enhanced_df['SpeciesFrequency'] = enhanced_df['SpeciesCode'].map(species_frequency)
            
            # Sort by SiteCode and SpeciesCode for better organization
            enhanced_df = enhanced_df.sort_values(['SiteCode', 'SpeciesCode']).reset_index(drop=True)
            
            # Save the enhanced CSV
            enhanced_df.to_csv(csv_file_path, index=False)
            
            print(f"Enhanced CSV data saved to: {csv_file_path}")
            print(f"CSV file contains {len(enhanced_df)} rows with detailed site-species relationships")
            print("Enhanced features: SiteSpeciesCount, SpeciesFrequency columns added")
  
        
        else:
            print(" Failed to create structured DataFrame")
    else:
        print(" Failed to fetch data from LAQN API")
