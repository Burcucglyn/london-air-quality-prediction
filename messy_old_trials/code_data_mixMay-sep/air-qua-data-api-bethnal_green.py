import requests #used to make a request to the API 
import json
import os
import pandas as pd

# Define parameters
site_code = "BG1"  # Bethnal Green
start_date = "2025-01-01"
end_date = "2025-05-01"

# Construct the API URL
url = (
    f"https://api.erg.ic.ac.uk/AirQuality/Data/Site/"
    f"SiteCode={site_code}/StartDate={start_date}/EndDate={end_date}/Json"
)

# Output setup
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)
filename = f"air_quality_{site_code}_{start_date}_to_{end_date}.json"
filepath = os.path.join(output_dir, filename)

# Download data - that's mean bring the data from the API so ican use it. (json format at big data why?) - json format is used for dictorory stracture for vscode
response = requests.get(url)

if response.status_code == 200:
    with open(filepath, "w") as f:
        json.dump(response.json(), f, indent=2)
    print(f"Data saved to {filepath}")
else:
    print(f"Request failed with status code: {response.status_code}")
    exit(1)

# Load data into Python show as json format
with open(filepath) as f:
    data = json.load(f)

# Show available top-level keys
print("Top-level keys:", list(data.keys()))

# Optional: Inspect one record (adjust depending on structure)
records = data.get("AirQualityData", None)

if isinstance(records, dict) and "Data" in records:
    observations = records["Data"]
    if observations:
        print(f"Loaded {len(observations)} records.")
        print("First record:")
        print(json.dumps(observations[0], indent=2))
    else:
        print("Data list is empty.")
else:
    print("Unexpected structure in AirQualityData.")

# Convert the observation records into a DataFrame
df = pd.DataFrame(observations)

# Rename columns for clarity
df = df.rename(columns={
    "@SpeciesCode": "pollutant",
    "@MeasurementDateGMT": "timestamp",
    "@Value": "value"
})

# Convert timestamp column to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Convert value to numeric
df["value"] = pd.to_numeric(df["value"], errors="coerce")

# Preview the DataFrame
print("\nDataFrame preview:")
print(df.head())

# Print all pollutants measured in this time frame
all_pollutants = sorted(df["pollutant"].unique())
print("\nAll pollutants recorded between", start_date, "and", end_date, ":")
for p in all_pollutants:
    print("-", p)
    
# Save the full dataset including all pollutants to CSV
csv_filename = f"all_pollutants_air_qua_{site_code}_{start_date}_to_{end_date}_bethnalgreen.csv"
csv_filepath = os.path.join(output_dir, csv_filename)

df.to_csv(csv_filepath, index=False)
print(f"\nFull dataset (all pollutants) saved to: {csv_filepath}")


