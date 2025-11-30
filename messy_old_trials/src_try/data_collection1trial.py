''' I will collect data from LAQN (London Air Quality Network)
Open-Meteo API weather data'''
# standard imports
import sys
from pathlib import Path

# ensure project root is on sys.path so local modules (like config) can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# third-party imports
import requests
import pandas as pd  # to handle data in DataFrame
from datetime import datetime, timedelta  # to handle date and time
import time  # to add delays between API requests
from urllib.parse import urljoin
#import time as time_module to measure total time taken for data collection (collect_air_quality_full_year_2023 func)
import time as time_module


# local config (Config class you just added)
from config import Config  # import configuration settings

class LAQN_API:
    '''class to interact with LAQN API
    website: https://api.erg.ic.ac.uk/AirQuality'''
    BASE_URL = "https://api.erg.ic.ac.uk/AirQuality"

    def __init__(self):
        # prefer Config.LAQN_BASE_URL but fall back to class constant
        self.base_url = getattr(Config, "LAQN_BASE_URL", self.BASE_URL).rstrip('/')
        # adding print statement to confirm it's working
        print(f"Created condition for LAQN collector with URL: {self.base_url}")

#               ----GET  London SITES data ----

    def get_sites(self):
        """Get all London monitoring sites data (defensive parsing)."""
        # print statement to confirm method call.
        print("Fetching all monitoring sites data.")

        url = f"{self.base_url}/Information/MonitoringSites/GroupName=London/Json"
        
        try:
            response = requests.get(url, timeout=15)  # increased timeout
            response.raise_for_status()

            data = response.json()

            # defensive extraction to handle different response shapes
            sites = None
            if isinstance(data, dict):
                sites = data.get('Sites', {}).get('Site') \
                        or data.get('sites') \
                        or data.get('MonitoringSites') \
                        or data.get('Site')
            if sites is None:
                # fallback: try to find a list in the top-level values
                for v in data.values() if isinstance(data, dict) else []:
                    if isinstance(v, list):
                        sites = v
                        break

            if not sites:
                print("No site list found in response.")
                return pd.DataFrame()

            # convert to dataframe call sites_df
            sites_df = pd.DataFrame(sites)
            print(f"Found {len(sites_df)} monitoring sites.")
            return sites_df  # return dataframe of sites
        
        except requests.RequestException as e:  # catch request exceptions.
            print(f"Error getting sites: {e}")
            return pd.DataFrame()  # return empty dataframe on error
        except ValueError as e:
            print(f"Error parsing sites JSON: {e}")
            return pd.DataFrame()
        
#               ----GET  London SITE, POLLUTANT data ----
    def get_site_pollutant(self, site_code, pollutant, start_date, end_date):
        """ Get specific site's pollutant data within time range.
        returns dataframe with standardized columns:
        SiteCode, SpeciesCode, measurement_date, value (plus any extra cols)
        """
        print(f"Getting {pollutant} data for site {site_code}.")

        # normalize date inputs to datetime
        def to_dt(d):
            if isinstance(d, datetime):
                return d
            try:
                return datetime.fromisoformat(str(d))
            except Exception:
                return pd.to_datetime(d, errors='coerce')

        start_dt = to_dt(start_date)
        end_dt = to_dt(end_date)

        # chunk safety (30-day)
        max_chunk_days = 30
        chunks = []
        cur = start_dt
        while cur <= end_dt:
            chunk_end = min(cur + timedelta(days=max_chunk_days - 1), end_dt)
            chunks.append((cur, chunk_end))
            cur = chunk_end + timedelta(days=1)

        all_records = []

        # helper to find first list inside nested json
        def find_list(obj):
            if isinstance(obj, list):
                return obj
            if isinstance(obj, dict):
                for v in obj.values():
                    res = find_list(v)
                    if res:
                        return res
            return None

        # helper to normalize record list to desired fields
        def normalize_records(records, site, species):
            if not records:
                return []
            df = pd.json_normalize(records)

            # detect date column
            date_candidates = [c for c in df.columns if c.lower() in (
                '@measurementdategmt', 'measurementdategmt', '@measurementdate', 'measurementdate', 'date', 'datetime', 'time')]
            value_candidates = [c for c in df.columns if c.lower() in ('@value', 'value', 'measurementvalue', 'reading')]

            date_col = date_candidates[0] if date_candidates else None
            value_col = value_candidates[0] if value_candidates else None

            # create standardized columns
            if date_col:
                df['measurement_date'] = pd.to_datetime(df[date_col], errors='coerce')
            else:
                df['measurement_date'] = pd.NaT

            if value_col:
                df['value'] = pd.to_numeric(df[value_col], errors='coerce')
            else:
                # try to infer numeric column
                numeric_col = None
                for c in df.columns:
                    if pd.api.types.is_numeric_dtype(df[c]):
                        numeric_col = c
                        break
                if numeric_col:
                    df['value'] = pd.to_numeric(df[numeric_col], errors='coerce')
                else:
                    df['value'] = pd.NA

            # ensure site/species columns present
            df['SiteCode'] = site
            df['SpeciesCode'] = species

            # desired order: SiteCode, SpeciesCode, measurement_date, value, ...
            cols = ['SiteCode', 'SpeciesCode', 'measurement_date', 'value'] + \
                   [c for c in df.columns if c not in ('SiteCode', 'SpeciesCode', 'measurement_date', 'value')]

            return df[cols].to_dict(orient='records')

        for s, e in chunks:
            s_str = s.strftime("%Y-%m-%d")
            e_str = e.strftime("%Y-%m-%d")

            url = f"{self.base_url}/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={pollutant}/StartDate={s_str}/EndDate={e_str}/Json"
            # try documented endpoint as well (if available)
            candidate_urls = [
                f"{self.base_url}/RawData/SitesSpeciesOriginal/Json?SiteCode={site_code}&SpeciesCode={pollutant}&StartDate={s_str}&EndDate={e_str}",
                url,
                f"{self.base_url}/Data/SiteSpecies/Json?SiteCode={site_code}&SpeciesCode={pollutant}&StartDate={s_str}&EndDate={e_str}"
            ]

            chunk_found = False
            for candidate in candidate_urls:
                try:
                    response = requests.get(candidate, timeout=20)
                    if response.status_code == 404:
                        continue
                    response.raise_for_status()
                    data = response.json()

                    # find measurements list robustly
                    measurements = None
                    if isinstance(data, dict):
                        measurements = (data.get('RawAQData') or {}).get('Data') \
                                       or data.get('Data') \
                                       or data.get('RawData') \
                                       or find_list(data)
                    else:
                        measurements = find_list(data)

                    if measurements:
                        normalized = normalize_records(measurements, site_code, pollutant)
                        if normalized:
                            all_records.extend(normalized)
                            chunk_found = True
                            break
                except Exception:
                    # try next candidate url
                    continue

            time.sleep(1)  # polite pause between chunk requests

        if not all_records:
            # return empty df with standard columns
            return pd.DataFrame(columns=['SiteCode', 'SpeciesCode', 'measurement_date', 'value'])

        result_df = pd.DataFrame(all_records)

        # ensure types
        if 'measurement_date' in result_df.columns:
            result_df['measurement_date'] = pd.to_datetime(result_df['measurement_date'], errors='coerce')
        if 'value' in result_df.columns:
            result_df['value'] = pd.to_numeric(result_df['value'], errors='coerce')

        # reorder to preferred final schema: SiteCode, SpeciesCode, measurement_date, value
        preferred = [c for c in ['SiteCode', 'SpeciesCode', 'measurement_date', 'value'] if c in result_df.columns]
        rest = [c for c in result_df.columns if c not in preferred]
        result_df = result_df[preferred + rest]

        return result_df

# helper: standardize any pollution dataframe and save only requested columns
def save_standard_pollution(df: pd.DataFrame, out_name: str = 'pollution_standard.csv'):
    """Keep only SiteCode, SpeciesCode, measurement_date, value and save csv."""
    out_dir = Path('data/raw')
    out_dir.mkdir(parents=True, exist_ok=True)
    cols = [c for c in ['SiteCode', 'SpeciesCode', 'measurement_date', 'value'] if c in df.columns]
    if not cols:
        # nothing to save
        return None
    std_df = df[cols].copy()
    # ensure proper ordering: sitecode, speciescode, date, value
    ordered = ['SiteCode', 'SpeciesCode', 'measurement_date', 'value']
    ordered = [c for c in ordered if c in std_df.columns]
    std_df = std_df[ordered]
    out_path = out_dir / out_name
    std_df.to_csv(out_path, index=False)
    return out_path
# ...existing code...
""" test jan 2023 data collection saved and function works. I'll collect 2023 all year data."""

# def collect_air_quality_full_year_2023():
#     """ Collect LAQN 2023 data in monthly chunks. """
#     start_time = time_module.time()  # start timing
    
#     api = LAQN_API()

#     # use priority sites instead of all sites to not hit api rate limits as usual.
#     priority_sites = ['MY1', 'BG1', 'CT1', 'RB1', 'TD1']  # 5 sites only.
    
#     # main two pollutants for analysis.
#     pollutants = ['NO2', 'PM10'] 
    
#     # monthly date ranges [1,13] to not hit api rate limits.
#     import calendar # to get month ranges.
#     year = 2023
#     monthly_ranges = []
#     for month in range(1, 13):
#         start_date = datetime(year, month, 1)
#         last_day = calendar.monthrange(year, month)[1]
#         end_date = datetime(year, month, last_day)
#         monthly_ranges.append((start_date, end_date))

#     # created loop for each site, pollutant and month with empty list to store df as usual.
#     all_data = []
    
#     for site_code in priority_sites:
#         for pollutant in pollutants:
#             for month_start, month_end in monthly_ranges:
#                 pollutant_data = api.get_site_pollutant(site_code, pollutant, month_start, month_end)
                
#                 if not pollutant_data.empty:
#                     all_data.append(pollutant_data)
                
#                 time.sleep(1)  # delay between monthly requests to avoid rate limits.

#     # combine all data and save.
#     if all_data:
#         full_data_df = pd.concat(all_data, ignore_index=True)
        
#         # save to file as pollution_data_2023year.csv
#         out_dir = Path('data/raw')
#         out_dir.mkdir(parents=True, exist_ok=True)
#         out_path = out_dir / 'pollution_data_2023year.csv'
#         full_data_df.to_csv(out_path, index=False)
        
#         # calculate total time taken and divide by 60 for min.
#         end_time = time_module.time()
#         total_minutes = (end_time - start_time) / 60
        
#         print(f"2023 year data collection completed in {total_minutes:.2f} minutes.")
#         return full_data_df, total_minutes
#     else:
#         end_time = time_module.time()
#         total_minutes = (end_time - start_time) / 60
#         return pd.DataFrame(), total_minutes
    






"""Building test function for Open-Meteo weather API"""
# ------TEST Open-Meteo WEATHER API function ----
class WeatherAPI:
    '''class to interact with Open-Meteo weather API
    website: https://open-meteo.com/'''
    
    def __init__(self):
        self.base_url = Config.OPENMETEO_BASE_URL  # use config URL
        self.forecast_url = f"{self.base_url}/forecast"
        self.archive_url = f"{self.base_url.replace('/v1', '')}/archive-api/v1/archive"  # for historical data
        self.london_lat = 51.5085  # london coordinates 
        self.london_lon = -0.1257
        print(f"Created weather collector with base URL: {self.base_url}")
    
    def get_recent_weather(self, days_back=7):
        """ Get recent weather data for testing - based on your original function """
        print(f"Getting recent {days_back} days weather data for testing")
        
        # london coordinates and parameters needs to be set
        params = {
            'latitude': self.london_lat,
            'longitude': self.london_lon,
            # API expects a comma-separated string for hourly variables
            'hourly': 'temperature_2m,wind_speed_10m,precipitation,relative_humidity_2m',
            # dynamic recent dates by default
            'start_date': (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d"),
            'end_date': datetime.now().strftime("%Y-%m-%d"),
            'timezone': 'Europe/London'
        }
        
        try:
            response = requests.get(self.forecast_url, params=params, timeout=15)
            response.raise_for_status()  # raise error for bad responses
            data = response.json()

            if 'hourly' in data:
                weather_df = pd.DataFrame(data['hourly'])
                print(f"Got {len(weather_df)} hourly records.")
                return weather_df
            else:
                print("No 'hourly' data in response.")
                return pd.DataFrame()
                
        except requests.RequestException as e:
            print(f"Weather API Error: {e}")
            return pd.DataFrame()
    



     
#------ January 2023 Weather data collection function ----
 

# def collect_weather_data_jan2023():
#     """ Collect weather data for January 2023 only """
#     start_time = time_module.time()  # start timing
    
#     weather_api = WeatherAPI()
    
#     # fixed date range for January 2023 only
#     start_date = datetime(2023, 1, 1)   # january 1st 2023
#     end_date = datetime(2023, 1, 31)    # january 31st 2023
    
#     print(f"Collecting weather data for London coordinates")
#     print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
#     # weather parameters for 2023 january data collection.
#     weather_params = ['temperature_2m', 'relative_humidity_2m', 'precipitation', 
#                      'wind_speed_10m', 'wind_direction_10m', 'pressure_msl']
    
#     # use archive API for 2023 jan data collection.
#     archive_url = "https://archive-api.open-meteo.com/v1/archive"
    
#     params = {
#         'latitude': weather_api.london_lat,  # london coordinates
#         'longitude': weather_api.london_lon,
#         'start_date': start_date.strftime('%Y-%m-%d'),
#         'end_date': end_date.strftime('%Y-%m-%d'),
#         'hourly': weather_params,
#         'timezone': 'Europe/London'
#     }
    
#     # make API request to collect january weather data
#     try:
#         print("Requesting weather data from Open-Meteo Archive API...")
#         response = requests.get(archive_url, params=params, timeout=60)
#         response.raise_for_status()  # raise error for bad responses
#         data = response.json()
        
#         # Hourly process and save weather data.
#         if 'hourly' in data:
#             weather_df = pd.DataFrame(data['hourly'])
            
#             # save to file
#             out_dir = Path('data/raw')
#             out_dir.mkdir(parents=True, exist_ok=True)
#             out_path = out_dir / 'weather_data_jan2023.csv'
#             weather_df.to_csv(out_path, index=False)
            
#             # calculate total time taken
#             end_time = time_module.time()
#             total_minutes = (end_time - start_time) / 60
            
#             print(f"Weather collection completed in {total_minutes:.2f} minutes")
#             return weather_df, total_minutes
#         else:
#             print("No hourly weather data received from API")
#             end_time = time_module.time()
#             total_minutes = (end_time - start_time) / 60
#             return pd.DataFrame(), total_minutes
            
#     except requests.RequestException as e:
#         print(f"Weather collection failed: {e}")
#         end_time = time_module.time()
#         total_minutes = (end_time - start_time) / 60
#         return pd.DataFrame(), total_minutes


#----- weather data collection function implementation for 2023 year.----

def weather_data_2023year():
    """ Collect weather data for full year 2023 in monthly chunks """
    start_time = time_module.time()  # start timing
    
    weather_api = WeatherAPI()
    
    # weather parameters for historical data collection
    weather_params = ['temperature_2m', 'relative_humidity_2m', 'precipitation', 
                     'wind_speed_10m', 'wind_direction_10m', 'pressure_msl']
    
    # create monthly date ranges for 2023
    import calendar  # to get month ranges
    year = 2023
    monthly_ranges = []
    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day)
        monthly_ranges.append((start_date, end_date))
    
    # created loop for each month with empty list to store df
    all_data = []
    
    # use archive API for historical data collection
    archive_url = "https://archive-api.open-meteo.com/v1/archive"
    
    for month_start, month_end in monthly_ranges:
        month_name = month_start.strftime('%B')
        
        params = {
            'latitude': weather_api.london_lat,  # london coordinates
            'longitude': weather_api.london_lon,
            'start_date': month_start.strftime('%Y-%m-%d'),
            'end_date': month_end.strftime('%Y-%m-%d'),
            'hourly': weather_params,
            'timezone': 'Europe/London'
        }
        
        # make API request for this monthly chunk
        try:
            response = requests.get(archive_url, params=params, timeout=60)
            response.raise_for_status()  # raise error for bad responses
            data = response.json()
            
            if 'hourly' in data:
                month_weather_df = pd.DataFrame(data['hourly'])
                all_data.append(month_weather_df)
                
        except requests.RequestException as e:
            print(f"Error collecting {month_name}: {e}")
        
        time.sleep(1)  # delay between monthly requests to avoid rate limits

    # combine all monthly weather data and save
    if all_data:
        full_weather_df = pd.concat(all_data, ignore_index=True)
        
        # save to file
        out_dir = Path('data/raw')
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / 'weather_data_2023year.csv'
        full_weather_df.to_csv(out_path, index=False)
        
        # calculate total time taken
        end_time = time_module.time()
        total_minutes = (end_time - start_time) / 60
        
        return full_weather_df, total_minutes
    else:
        end_time = time_module.time()
        total_minutes = (end_time - start_time) / 60
        return pd.DataFrame(), total_minutes



    










    

# main block to collect and save 
if __name__ == "__main__":
    # LAQN Data colletion code blocks under this comment.
    #LAQN january 2023 data collection with timing
    # print("=== Starting LAQN data collection for January 2023. ===")
    # data = collect_air_quality_jan2023()
    # if not data.empty:
    #     print(f"Collected and saved {len(data)} records.")
    # print('=== LAQN January 2023 data collection completed. ===')
    # print("=== Starting LAQN data collection for full year 2023. ===")
    # data, duration = collect_air_quality_full_year_2023()
    # if not data.empty:
    #     print(f"Collected and saved {len(data)} records.")
    #     print(f"Total process time: {duration:.2f} minutes.")
    # print('=== LAQN full year 2023 data collection completed. ===')

    # Open-Meteo Data collection code blocks under this comment.


    # main block to collect and save january weather data with timing
    # print("=== Starting weather data collection for January 2023 ===")
    # data, duration = collect_weather_data_jan2023()
    # if not data.empty:
    #     print(f"SUCCESS! Collected and saved {len(data)} weather records.")
    #     print(f"Total process time: {duration:.2f} minutes.")
    # print('=== Weather Jan 2023 data collection completed. ===')

    # main block to collect and save full year 2023 weather data with timing
    print("=== Starting weather data collection for full year 2023 ===")
    data, duration = weather_data_2023year()
    if not data.empty:
        print(f"SUCCESS! Collected and saved {len(data)} weather records")
        print(f"Total process time: {duration:.2f} minutes")
    print('=== Weather full year 2023 data collection completed ===')

