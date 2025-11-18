class Config:
    # API Settings
    laqn_url  = "https://api.erg.ic.ac.uk/AirQuality"
    get_sites_species = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName={GROUPNAME}/Json"
    get_hourly_data = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={SITECODE}/SpeciesCode={SPECIESCODE}/StartDate={STARTDATE}/EndDate={ENDDATE}/Period={PERIOD}/Units={UNITS}/Step={STEP}/Json"
    OPENMETEO_BASE_URL = "https://api.open-meteo.com/v1"

    