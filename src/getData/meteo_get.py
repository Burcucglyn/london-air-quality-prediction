"""This file for meteo open air weather forecast fetching functions.
I will be create the functions here and foor testing I'll use meteo_test.py.
Installl requests for meteoo api fetching.
pip install openmeteo-requests
pip install requests-cache retry-requests numpy pandas


Regards to documentation of meteo api endpoints:
https://open-meteo.com/en/docs
meteo_url = "https://api.open-meteo.com/v1
London coordinates:
    Latitude: 51.5085
    Longitude: -0.1257
temprature: Celcius
wind speed: km/h
precipitation: mm
humidity: %
cloudcover: %
pressure: hPa
timeformat: ISO 8601
timezone: GMT
I will use variables for hourly data:
"temperature_2m",           # Air temperature (°C)
    "relative_humidity_2m",     # Relative humidity (%)
    "wind_speed_10m",          # Wind speed (km/h)
    "wind_direction_10m",      # Wind direction (°)
    "surface_pressure",        # Atmospheric pressure (hPa)
    "precipitation",           # Precipitation (mm)
    "cloud_cover",            # Cloud cover (%)
    """

import pandas as pd
import requests_cache
from retry_requests import retry
import openmeteo_requests

from config import MeteoConfig


class MeteoGet:
    """Fetch weather data from Open-Meteo APIs."""

    def __init__(self):
        self.base_url = MeteoConfig.open_meteo
        self.archive_url = MeteoConfig.open_meteo_archive
        # added parameters from config file.
        self.params = dict(MeteoConfig.meteo_param)

        """ commented out the code below to not overwrite to fetched data."""
        # # Prepare client with cache + retries. Take this from openmeteo_requests python code document.
        # self._cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
        # self._retry_session = retry(self._cache_session, retries=5, backoff_factor=0.2)
        # self._client = openmeteo_requests.Client(session=self._retry_session)
        pass

    def get_weather(self, start_date: str, end_date: str) -> object:
        """Fetch raw Open-Meteo response object for given date range."""
        """ commented out the code below to not overwrite to fetched data."""
        # params = dict(self.params)
        # params["start_date"] = start_date
        # params["end_date"] = end_date

        # responses = self._client.weather_api(self.archive_url, params=params)
        # return responses[0]
        pass

    def process_hourly_data(self, response) -> pd.DataFrame:

        """ commented out the code below to not overwrite to fetched data."""
        # """Convert the hourly section of a response to a DataFrame."""
        # hourly = response.Hourly()

        # # Order must match the requested 'hourly' variables in Config.meteo_param
        # temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        # wind_speed_10m = hourly.Variables(1).ValuesAsNumpy()
        # wind_speed_100m = hourly.Variables(2).ValuesAsNumpy()
        # wind_direction_10m = hourly.Variables(3).ValuesAsNumpy()
        # wind_direction_100m = hourly.Variables(4).ValuesAsNumpy()
        # wind_gusts_10m = hourly.Variables(5).ValuesAsNumpy()
        # surface_pressure = hourly.Variables(6).ValuesAsNumpy()
        # precipitation = hourly.Variables(7).ValuesAsNumpy()
        # cloud_cover = hourly.Variables(8).ValuesAsNumpy()
        # relative_humidity_2m = hourly.Variables(9).ValuesAsNumpy()

        # time_index = pd.date_range(
        #     start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        #     end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        #     freq=pd.Timedelta(seconds=hourly.Interval()),
        #     inclusive="left",
        # )

        # df = pd.DataFrame(
        #     {
        #         "date": time_index,
        #         "temperature_2m": temperature_2m,
        #         "wind_speed_10m": wind_speed_10m,
        #         "wind_speed_100m": wind_speed_100m,
        #         "wind_direction_10m": wind_direction_10m,
        #         "wind_direction_100m": wind_direction_100m,
        #         "wind_gusts_10m": wind_gusts_10m,
        #         "surface_pressure": surface_pressure,
        #         "precipitation": precipitation,
        #         "cloud_cover": cloud_cover,
        #         "relative_humidity_2m": relative_humidity_2m,
        #     }
        # )

        # return df
        pass

    def fetch_hourly_dataframe(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Convenience method: fetch response and return hourly DataFrame."""
        """commented out the code below to not overwrite to fetched data."""
        # response = self.get_weather(start_date, end_date)
        # # Optional metadata logging:
        # # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        # # print(f"Elevation: {response.Elevation()} m")
        # # print(f"UTC offset: {response.UtcOffsetSeconds()}s")
        # return self.process_hourly_data(response)
        pass
    