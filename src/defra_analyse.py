"""Analyse and organise DEFRA CSV data for London stations."""

import pandas as pd
from pathlib import Path
import re

def clean_london_stations_csv(
    input_path: Path = Path("data/defra/test/london_stations_test.csv"),
    output_path: Path = Path("data/defra/test/london_stations_clean.csv")
) -> pd.DataFrame:
    """
    Clean and restructure the raw London stations CSV to the desired shape.

    Steps:
    1) Ensure output folder exists
    2) Load the raw CSV
    3) Filter rows where 'pollutant' has values
    4) Parse station_name into:
       - station_name (text before '-')
       - pollutant_available (text before '(' in the right side)
       - pollutant_air (text inside parentheses)
    5) Parse 'pollutant' label (e.g., '6875 - Station-Pollutant (air)') for the same fields
    6) Prefer values from the label parse; fallback to station_name parse
    7) Build the final DataFrame with requested columns
    8) Save cleaned CSV and return the DataFrame
    """

    # 1) Ensure output folder exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 2) Load the raw CSV
    df = pd.read_csv(input_path)

    # 3) Filter rows where 'pollutant' column is present and non-empty
    df = df[df['pollutant'].notna() & (df['pollutant'].astype(str).str.strip() != "")].copy()

    # 4) Helper to split "Station-Pollutant (air)" into parts
    def split_station_and_pollutant(station_name: str):
        # Return three parts: base station name, pollutant_available, pollutant_air
        if not isinstance(station_name, str):
            return None, None, None
        # Split only on the first '-' into "Station" and "Pollutant (air)"
        parts = station_name.split('-', 1)
        base = parts[0].strip()                           # Station name before '-'
        rest = parts[1].strip() if len(parts) > 1 else "" # The part after '-'
        # Extract text before '(' as pollutant_available and inside '(...)' as pollutant_air
        m = re.match(r"^(.*?)\s*\((.*?)\)\s*$", rest)
        if m:
            pollutant_available = m.group(1).strip()
            pollutant_air = m.group(2).strip()
        else:
            pollutant_available = rest.strip()
            pollutant_air = None
        return base, pollutant_available, pollutant_air

    # 5) Helper to parse from the 'pollutant' label (e.g., "6875 - Station-Pollutant (air)")
    def extract_from_label(label: str):
        if not isinstance(label, str):
            return None, None, None
        # Remove the leading ID prefix "6875 - "
        right = label.split(" - ", 1)[-1]
        # Reuse split logic to extract fields
        base, pollutant_available, pollutant_air = split_station_and_pollutant(right)
        return base, pollutant_available, pollutant_air

    # 6) Parse from 'station_name'
    station_parsed = df['station_name'].apply(split_station_and_pollutant)
    df[['station_name_clean', 'pollutant_available_from_station', 'pollutant_air_from_station']] = (
        pd.DataFrame(station_parsed.tolist(), index=df.index)
    )

    # Parse from 'pollutant' label (usually more reliable)
    label_parsed = df['pollutant'].apply(extract_from_label)
    df[['station_name_from_label', 'pollutant_available', 'pollutant_air']] = (
        pd.DataFrame(label_parsed.tolist(), index=df.index)
    )

    # 7) Prefer label-derived values; fallback to station-derived
    df['station_name_final'] = df['station_name_from_label'].fillna(df['station_name_clean'])
    df['pollutant_available'] = df['pollutant_available'].fillna(df['pollutant_available_from_station'])
    df['pollutant_air'] = df['pollutant_air'].fillna(df['pollutant_air_from_station'])

    # 8) Build final DataFrame with requested columns and names
    final_cols = [
        'station_id',
        'station_name_final',   # clean station name (before '-')
        'pollutant_available',  # text before '('
        'pollutant_air',        # text inside '(...)'
        'latitude',
        'longitude',
        'timeseries_id',
        'pollutant'             # original label for traceability
    ]
    final_df = df[final_cols].rename(columns={
        'station_name_final': 'station_name'
    })

    # Save cleaned CSV
    final_df.to_csv(output_path, index=False)
    print(f"Saved cleaned CSV to: {output_path}")
    print(final_df.head().to_string(index=False))

    return final_df


if __name__ == "__main__":
    # Run cleaning with default paths
    clean_london_stations_csv()

