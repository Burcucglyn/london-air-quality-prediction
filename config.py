class Config:
    # API Settings
    laqn_url  = "https://api.erg.ic.ac.uk/AirQuality"
    get_sites_species = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName={GROUPNAME}/Json"
    get_hourly_data = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={SITECODE}/SpeciesCode={SPECIESCODE}/StartDate={STARTDATE}/EndDate={ENDDATE}/Json"
    
    defra_url = "https://uk-air.defra.gov.uk/sos-ukair/api/v1"
    defra_capabilities_url = "https://uk-air.defra.gov.uk/sos-ukair/service/json"
    eu_pollutant_vocab_url = "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/csv"
    # London bounding box (WGS84 coordinates)
    london_bbox = [-0.5, 51.3, 0.3, 51.7]  # [minLon, minLat, maxLon, maxLat]


class MeteoConfig:
    """Configuration class for MeteoGet settings."""
    open_meteo = "https://api.open-meteo.com/v1"
    open_meteo_archive = "https://archive-api.open-meteo.com/v1/archive"
    meteo_param = {
        "latitude": 51.5085,
        "longitude": -0.1257,
        "hourly": [
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
        ],
        "timezone": "GMT",
    }


