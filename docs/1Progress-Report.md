## Progress Report

### Setting Up My Development Environment

**Creating the Virtual Environment** I started by setting up a dedicated Python environment for my thesis project to keep everything organized and avoid any package conflicts. Created the environment using Python's venv module and then customized it to work more efficiently with my workflow.

**What I Did:**

- Set up virtual environment with `python -m venv .venv`
- Created a custom shortcut called `ap venv` so I can quickly activate it from any terminal
- Connected the environment to my project requirements

**Managing Dependencies** I needed to figure out which Python packages would be essential for air pollution analysis and machine learning. Did some research online and with ChatGPT to identify the core libraries I would need throughout the project.

The final requirements file ended up with 87 packages after all dependencies were resolved, including pandas for data handling, scikit-learn for machine learning, geopandas for London geographic data, and requests for API calls.

### Building the Project Structure

**Organising the Code** Since this is going to be a substantial project, I knew I needed proper organisation from the start. Designed a folder structure that separates different types of work and makes it easy to find things later.

```
air-pollution-levels/
├── data/                    # All data storage
│   ├── external/           # Reference data
│   ├── processed/          # Clean data ready for analysis
│   └── raw/               # Original data from APIs
├── docs/                   # Documentation files
│   └── api_guide.md
├── notebooks/              # Jupyter notebooks for exploration
├── results/               # Model outputs and graphs
│   ├── figures/          
│   └── models/
├── src/                   # Main source code
│   ├── __init__.py           
│   └── data_collection.py
├── tests/                 # Testing files
│   ├── __init__.py           
│   └── test_api.py
├── reports/               # progress reports folder
│   └── progress-report.md # first md progress record
├── config.py             # Project settings
├── main.py               # Main execution file
├── README.md             # Project documentation
└── requirements.txt      # Package dependencies
```

**Why This Structure Works** This layout keeps everything separate but logical. Raw data goes in one place, cleaned data in another, and all the actual code stays in the src folder. Makes it much easier to navigate and keeps things professional looking.

### Coding the Data Collection

**Getting Started with APIs** I needed to connect to multiple data sources - the London Air Quality Network for pollution data, Open-Meteo for weather information, and attempted to integrate UK Air DEFRA for additional validation data. Started with the LAQN API since that's the core data for my thesis.

**Building the API Classes** Created classes to handle all interactions with each data source:

python

```python
class LAQN_API:
    def __init__(self):
        # Set up the API connection using config settings
    
    def get_sites(self):
        # Get all monitoring locations in London
    
    def get_site_pollutant(self, site_code, pollutant, start_date, end_date):
        # Collect actual pollution measurements for specific sites
        
class DEFRA_API:
    def __init__(self):
        # Attempted DEFRA API integration
        
    def get_defra_sites(self):
        # Attempted to retrieve DEFRA monitoring sites
        
def test_weather_api():
    # Test Open-Meteo weather API functionality
```

**Technical Implementation**

- Used the config file to manage all API endpoints and settings
- Added proper error handling with try-except blocks so the code doesn't crash if something goes wrong
- Built in delays between API calls to be respectful to their servers and avoid rate limiting
- Set up the responses to automatically convert to pandas DataFrames using json_normalize for easy analysis
- Implemented proper date formatting for the LAQN API requirements
- Added weather API testing with London coordinates and multiple meteorological parameters

### API Integration and Testing

**Comprehensive Testing Framework** Built a thorough testing system that validates all API functionality:

python

```python
def test_api():
    # Test API initialization and configuration
    # Test monitoring sites retrieval
    # Test pollution data collection for multiple sites
    # Validate data structure and content
    
def test_weather_api():
    # Test weather data collection from Open-Meteo
    # Validate meteorological parameter retrieval
    # Check data structure and timestamps
```

**Testing Multiple Sites** Expanded the testing to cover key London monitoring locations:

- MY1 (Marylebone Road) - roadside traffic pollution
- BG1 (Bethnal Green) - urban background pollution
- CT1 (Camden Town) - mixed residential and traffic area

**Weather Data Integration** Successfully implemented weather API testing that retrieves:

- Temperature measurements (2m above ground)
- Wind speed and direction data
- Precipitation and humidity readings
- Proper timezone handling for London (Europe/London)

**Data Validation** The test framework checks:

- API connectivity and response handling for pollution and weather sources
- Site metadata retrieval and formatting
- Pollution data collection across different locations
- Weather parameter collection with proper timestamps
- DataFrame structure and column consistency
- Error handling for missing or unavailable data

### Challenges I Encountered

**Environment Setup Issues** Getting the virtual environment working properly took longer than expected. Initially struggled with activation and making sure all packages installed correctly. Solved this by creating the custom activation command which streamlined the whole process.

**Package Management Problems** Had some issues with package compatibility and figuring out exactly which versions would work together. Spent time testing different combinations and eventually got a stable set of requirements.

**API Integration Difficulties** The LAQN API has specific requirements for date formatting that took a while to figure out. Needed to format dates as "dd MMM yyyy" rather than the standard format I was used to. Also had to work out the JSON response structure to extract the actual pollution measurements properly.

**Weather API Coordinate Issues** Initially used incorrect London coordinates for the Open-Meteo API testing, which caused location-specific weather data retrieval problems. Fixed this by using the proper London coordinates (51.5085°N, -0.1257°W) and validating the geographic accuracy.

**Import Statement Errors** Encountered import errors in the testing file where I accidentally imported from wrong modules (turtle instead of pandas). Fixed by ensuring proper pandas import statements and cleaning up the import section.

**Method Parameter Handling** Initially had issues with the pollution data collection method where I was overwriting the original date parameters. Fixed this by using separate variable names for the formatted date strings.

**Class Structure Alignment Problems** Encountered a significant debugging challenge with the DEFRA API implementation where I had an indentation mistake in the `__init__` method within the data_collection.py file. This caused alignment problems between the `__init__` method and the `get_defra_sites` method, leading to syntax and structural issues. Took considerable time to identify this issue as the misalignment wasn't immediately obvious and caused the class methods to not function properly.

**DEFRA API Integration Failures** Attempted to integrate the UK Air DEFRA API as a third data source but encountered multiple serious issues:

- 404 Client Error: Not Found for the attempted endpoint URLs
- 30+ HTTP redirects causing connection failures
- Service unavailable errors suggesting server-side problems
- Inconsistent API documentation making endpoint discovery difficult

The DEFRA API proved to be unreliable with frequent service interruptions, outdated endpoint URLs, and poor documentation. After multiple attempts with different endpoints and connection strategies, decided to skip DEFRA integration due to its instability and focus on the two working APIs instead.

**Import and Path Issues** Getting the imports to work correctly between different folders was more complex than expected. Had to set up proper Python path management to make sure the config file could be imported from the source code directory.

### Testing and Results

**What I Tested** Built a comprehensive test function that checks:

- Can I connect to the working APIs successfully
- Does the site data retrieval work for all London monitoring locations
- Can I get actual pollution measurements from multiple sites
- Does weather data collection work with proper parameters and timestamps
- Are the responses being converted to usable DataFrames properly
- Does error handling work when data is unavailable or APIs fail

**Current Results** Successfully retrieving:

- 98 London monitoring sites with their coordinates and details
- Historical NO2 pollution data for multiple test sites including Marylebone Road, Bethnal Green, and Camden Town
- Weather data including temperature, wind speed, precipitation, and humidity for London
- Proper data structure with measurement timestamps, pollution values, and site metadata
- Meteorological data with hourly resolution and proper timezone handling
- Consistent DataFrame format ready for analysis and feature engineering

**API Reliability Assessment** Through testing discovered that:

- LAQN API is highly reliable with consistent uptime and data availability
- Open-Meteo weather API provides stable, well-formatted responses
- DEFRA API is unreliable with frequent service issues and should not be used as a primary data source

### Code Quality and Structure

**Professional Standards** Implemented proper coding practices:

- Clear method documentation and comments
- Comprehensive error handling across all API calls
- Modular class design for easy extension
- Separation of concerns between configuration, data collection, and testing
- Proper coordinate validation and parameter handling
- Graceful degradation when APIs fail

**Debugging and Validation** Added comprehensive print statements and data validation to track:

- API response status and data availability
- Record counts and sample data preview
- Success and failure rates across different sites and data sources
- Geographic coordinate accuracy for weather data
- Clear feedback on what data is being collected and what failed

### Where I Stand Now

**What's Working**

- Development environment fully set up and customized
- Project structure implemented and organised
- API connections to LAQN and Open-Meteo established and thoroughly tested
- Data collection functionality operational across multiple London sites
- Weather data integration working with proper London coordinates
- Testing framework confirms core APIs work reliably
- Code quality meets professional standards with robust error handling

**Technical Achievements**

- Successfully collecting data from 98 London monitoring sites
- Validated pollution data collection for NO2 across different site types
- Weather API integration providing meteorological context for pollution analysis
- Proper DataFrame structure established for downstream analysis
- Error handling prevents crashes when data sources are unavailable
- Rate limiting respects API constraints for working data sources
- Learned valuable lessons about API reliability and the importance of having backup data sources

**API Integration Status**

- LAQN API: Fully operational and reliable.
- Open-Meteo Weather API: Working successfully with comprehensive meteorological data.
- DEFRA API: Attempted integration failed due to service reliability issues - skipped for project stability

**Next Steps**

- Expand collection to additional pollutants (PM2.5, PM10) using proven LAQN API
- Implement larger date ranges for comprehensive historical data collection
- Integrate pollution and weather data into combined datasets for analysis
- Build data quality checks and cleaning procedures
- Set up automated data storage and preprocessing pipelines
- Consider TfL traffic data as next reliable data source instead of DEFRA

**Lessons Learned** The DEFRA integration failure taught important lessons about API reliability in real-world projects. Not all data sources are suitable for production use, and it's better to have two highly reliable sources than three unreliable ones. The experience also reinforced the importance of proper error handling and fallback strategies when working with external APIs.

The foundation with LAQN and weather data is solid and provides comprehensive coverage for air quality prediction modeling. The modular code structure means additional data sources can be integrated later if reliable alternatives to DEFRA are found, without affecting the main analysis pipeline.

