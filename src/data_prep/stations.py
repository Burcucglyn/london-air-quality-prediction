"""" In this module, I will be optimasing LAQN and DEFRA processed datasets for further analysis.
1. I will be organising both datasets to have same column names, formats and structure before merging them.
    - Example structure: Location_ID, Location_Name, Timestamp, Pollutant, Value, Latitude, Longiture, Source
    - LAQN monthly fetched datasets missing Location_ID, Location_Name, Latitude, Longitude columns.
       - to optimase LAQN datasets first general cathegory yearly datasets/monthly datasets and then each monthly data sets
       needs to be have each months pollutants, values and timestamps and the location details.
    - DEFRA datasets named under station_name and stored on dataset as according to pollutant name and timestamp
       - Optimase DEFRA datasets: first general cathegory yearly datasets/monthly datasets and then each monthly data sets
       needs to be have each months pollutants, values and timestamps and the location details."""