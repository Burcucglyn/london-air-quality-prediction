"""Testing and data-fetch script for MeteoGet (instance-based)."""

import os
import datetime as dt
import pandas as pd
import unittest



TEST_DIR = os.path.join("data", "meteo", "test")
RAW_DIR = os.path.join("data", "meteo", "raw")

import sys 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.getData.meteo_get import MeteoGet


class MeteoHelper:
    """Instance-based helpers for fetching and saving."""

    def __init__(self):
        os.makedirs(TEST_DIR, exist_ok=True)
        os.makedirs(RAW_DIR, exist_ok=True)
        self.mg = MeteoGet()

    def fetch_and_save_csv(self, start_date: str, end_date: str, out_path: str) -> str:
        """ commented out the code below to not overwrite to fetched data."""
        # os.makedirs(os.path.dirname(out_path), exist_ok=True)
        # df = self.mg.fetch_hourly_dataframe(start_date, end_date)
        # df.to_csv(out_path, index=False)
        # return out_path
        pass

    def save_test(self, start_date: str, end_date: str) -> str:
        """ commented out the code below to not overwrite to fetched data."""
        # """Save to data/meteo/test/meteo_<MMDD>-<MMDDYY>.csv."""
        # sd = dt.date.fromisoformat(start_date)
        # ed = dt.date.fromisoformat(end_date)
        # fname = f"meteo_{sd.strftime('%m%d')}-{ed.strftime('%m%d%y')}.csv"
        # out_path = os.path.join(TEST_DIR, fname)
        # return self.fetch_and_save_csv(start_date, end_date, out_path)
        pass

    def save_monthly_raw(self, year: int, month: int) -> str:
        """ commented out the code below to not overwrite to fetched data."""
        # """Save month to data/meteo/raw/monthlyYYYY/<YYYY-MM>.csv."""
        # first = dt.date(year, month, 1)
        # next_month = dt.date(year + (month == 12), (month % 12) + 1, 1)
        # last = next_month - dt.timedelta(days=1)
        # monthly_dir = os.path.join(RAW_DIR, f"monthly{year}")
        # os.makedirs(monthly_dir, exist_ok=True)
        # out_path = os.path.join(monthly_dir, f"{year}-{month:02d}.csv")
        # return self.fetch_and_save_csv(first.isoformat(), last.isoformat(), out_path)
        pass


    def test_fetch_hourly_df():
        """commented out the code below to not overwrite to fetched data."""
        # """Pytest smoke test: short range and column check."""
        # helper = MeteoHelper()
        # df = helper.mg.fetch_hourly_dataframe("2024-01-01", "2024-01-03")
        # assert isinstance(df, pd.DataFrame)
        # expected_cols = {
        #     "date",
        #     "temperature_2m",
        #     "wind_speed_10m",
        #     "wind_speed_100m",
        #     "wind_direction_10m",
        #     "wind_direction_100m",
        #     "wind_gusts_10m",
        #     "surface_pressure",
        #     "precipitation",
        #     "cloud_cover",
        #     "relative_humidity_2m",
        # }
        # assert expected_cols.issubset(df.columns)
        # assert len(df) > 0
        pass
#outside class to validate csv.
def validate_basic_csv(path: str) -> bool:
    import pandas as pd
    import os

    if not os.path.exists(path):
        print(f"Missing file: {path}")
        return False

    df = pd.read_csv(path)
    required = [
        "date",
        "temperature_2m",
        "wind_speed_10m",
        "wind_speed_100m",
        "wind_direction_10m",
        "wind_direction_100m",
        "wind_gusts_10m",
        "surface_pressure",
        "precipitation",
        "cloud_cover",
        "relative_humidity_2m",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"Missing columns: {missing}")
        return False

    # Parse dates and check order
    try:
        dt_series = pd.to_datetime(df["date"], errors="raise")
    except Exception as e:
        print(f"Date parse failed: {e}")
        return False

    if not dt_series.is_monotonic_increasing:
        print("Dates are not increasing")
        return False

    if len(df) == 0:
        print("No rows")
        return False

    print("Basic validation passed")
    return True
    
class TestMeteoData(unittest.TestCase):
    """Test suite for validating downloaded meteo data."""

    def test_validate_test_file(self):
        """Test the test span file."""
        test_path = os.path.join(TEST_DIR, "meteo_0101-010324.csv")
        self.assertTrue(validate_basic_csv(test_path), f"Validation failed for {test_path}")

    def test_validate_monthly_files(self):
        """Test all monthly files for 2023-2025."""
        for year in (2023, 2024, 2025):
            monthly_dir = os.path.join(RAW_DIR, f"monthly{year}")
            if not os.path.exists(monthly_dir):
                self.skipTest(f"Directory {monthly_dir} does not exist")
                continue
            
            for month in range(1, 13):
                filename = f"{year}-{month:02d}.csv"
                filepath = os.path.join(monthly_dir, filename)
                if os.path.exists(filepath):
                    with self.subTest(file=filepath):
                        self.assertTrue(validate_basic_csv(filepath))



if __name__ == "__main__":
    # helper = MeteoHelper()

    # # Save test span: data/meteo/test/meteo_0101-010324.csv
    # start = "2024-01-01"
    # end = "2024-01-03"
    # path = helper.save_test(start, end)
    # print(f"Saved test span: {path}")

    # # Save monthly files for 2023–2025
    # for year in (2023, 2024, 2025):
    #     for month in range(1, 13):
    #         try:
    #             p = helper.save_monthly_raw(year, month)
    #             print(f"Saved monthly: {p}")
    #         except Exception as e:
    #             print(f"Skip {year}-{month:02d}: {e}")

    # Example: validate your test file
    test_path = os.path.join("data", "meteo", "test", "meteo_0101-010324.csv")
    validate_basic_csv(test_path)

    # Validate all monthly files
    print(f"\n=== Validating monthly files ===")
    for year in (2023, 2024, 2025):
        monthly_dir = os.path.join(RAW_DIR, f"monthly{year}")
        if os.path.exists(monthly_dir):
            files = sorted([f for f in os.listdir(monthly_dir) if f.endswith('.csv')])
            print(f"\nYear {year}: {len(files)} files")
            for filename in files:
                validate_basic_csv(os.path.join(monthly_dir, filename))

    # Run unit tests
    print(f"\n=== Running unit tests ===")
    unittest.main(argv=[''], exit=False, verbosity=2)