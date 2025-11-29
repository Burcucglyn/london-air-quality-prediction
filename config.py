class Config:
    # API Settings
    laqn_url  = "https://api.erg.ic.ac.uk/AirQuality"
    get_sites_species = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName={GROUPNAME}/Json"
    get_hourly_data = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={SITECODE}/SpeciesCode={SPECIESCODE}/StartDate={STARTDATE}/EndDate={ENDDATE}/Json"
    OPENMETEO_BASE_URL = "https://api.open-meteo.com/v1"
    defra_url = "https://uk-air.defra.gov.uk/sos-ukair/api/v1"
    defra_capabilities_url = "https://uk-air.defra.gov.uk/sos-ukair/service/json"
    eu_pollutant_vocab_url = "http://dd.eionet.europa.eu/vocabulary/aq/pollutant/csv"
    # London bounding box (WGS84 coordinates)
    london_bbox = {
        "ll": {"type": "Point", "coordinates": [-0.5, 51.3]},
        "ur": {"type": "Point", "coordinates": [0.3, 51.7]}
    }
    