import pandas as pd
import os 
from src.laqn_get import laqnGet
df = pd.read_csv("data/laqn/sites_species_london.csv", parse_dates=['@DateMeasurementStarted','@DateMeasurementFinished'])
print(df['@DateMeasurementStarted'].min(), df['@DateMeasurementStarted'].max())
print(df['@DateMeasurementFinished'].min(), df['@DateMeasurementFinished'].max())

g = laqnGet()
print(g.get_hourly_data("TD0", "NO2", "2023-01-01", "2023-01-07").head())