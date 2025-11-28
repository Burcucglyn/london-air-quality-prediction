import requests
from config import Config
import pandas as pd
import datetime
from pathlib import Path
import time
import json
#parsing html
from bs4 import BeautifulSoup

class DefraGet:
    """ Class to DEFRA UK-AIR sensor obervation services API fetching data.
    base defra_url: https://uk-air.defra.gov.uk/sos-ukair/api/v1
    Pollutant Codes Reference:
    -------------------------
    Source: European Environment Agency (EEA) Air Quality Vocabulary
    URL: http://dd.eionet.europa.eu/vocabulary/aq/pollutant/
    
    
    """

    def __init__(self):
        """ Initialize DefraGet with base URL with config instance."""
        self.config = Config()
        self.pollutant_codes = None

    def defra_eea_pollutant_vocabulary():
        """ fetch the official EEA pollutant codes from data dictinionery.
        Returns:
            dict:{code: notation} e.g., {'8':NO2, '5': 'PM10'}"""
        url = Config.defra_pollutant

        
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        #parse html beatifulsoup
        soup = BeautifulSoup(response.content, 'html.parser')

        #find table with pollutant codes on eea.
        table = soup.find('table', {'class': 'datatable'})
        if not table:
            raise Exception("Could not find pollutant table on EEA page")
        
        pollutant_vocab = {}
        
        # Parse table rows (skip header)
        rows = table.find_all('tr')[1:]
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                # First column usually has the URI with code
                uri_link = cols[0].find('a')
                if uri_link:
                    uri = uri_link.get('href', '')
                    code = uri.split('/')[-1]  # Extract code from URI
                    
                    # Second column has the notation (NO2, PM10, etc.)
                    notation = cols[1].get_text(strip=True)
                    
                    pollutant_vocab[code] = notation
        
        if not pollutant_vocab:
            raise Exception("No pollutant codes.")
        self.pollutant_codes = pollutant_vocab
        return pollutant_vocab



