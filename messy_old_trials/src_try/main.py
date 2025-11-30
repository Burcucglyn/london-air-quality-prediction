"""
Enhanced LAQN API Collector with Parallel Processing
Collects full year 2023 London air quality data efficiently
"""

from pathlib import Path
import logging

import asyncio
from datetime import datetime, timedelta
from threading import Thread
import threading
import time
import concurrent.futures
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, urljoin
import csv
import pandas as pd
import requests
import aiohttp
from tqdm import tqdm
from time import perf_counter
import random
import math


logger = logging.getLogger(__name__)

class LAQN_API:
    """class to interact with the laqn air quality api"""
    base_url = "https://api.erg.ic.ac.uk/AirQuality/"

    #setting up the session with retries
    def __init__(self):
        # create session with retries
        sess = requests.Session()
        try:
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429,500,502,503,504], allowed_methods=["GET","POST"])
            adapter = HTTPAdapter(max_retries=retry)
            sess.mount("https://", adapter)
            sess.mount("http://", adapter)
        except Exception:
            pass
        self.session = sess
        self.lock = threading.Lock()

    #fethching all monitoring sites in csv format
    def get_sites(self) -> pd.DataFrame:
        """fetch all monitoring sites"""
       
        url = urljoin(self.base_url, "Information/MonitoringSites/GroupName=London/csv")
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        sites = pd.json_normalize(data.get("Sites", {}).get("Site", []))
        return sites
    
    #fetching all pollutants/species
    def get_pollutants(self) -> pd.DataFrame:
        """Fetch pollutant/species list, returnd  as df with species info."""
        url = f"{self.base_url}/Information/Species/csv"
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # try expected path first
            species_list = None
            if isinstance(data, dict):
                # common explicit structure
                if 'Species' in data and isinstance(data['Species'], dict) and 'Species' in data['Species']:
                    species_list = data['Species']['Species']

            # fallback: try several common wrapper keys
            if species_list is None and isinstance(data, dict):
                for key in ('Species', 'Data', 'RawData', 'RawAQData', 'Items', 'ItemList', 'SpeciesList'):
                    v = data.get(key)
                    if isinstance(v, list):
                        species_list = v
                        break
                    if isinstance(v, dict) and 'Species' in v and isinstance(v['Species'], list):
                        species_list = v['Species']
                        break

            # last-resort: find first nested list anywhere in the structure
            def _find_first_list(obj):
                if isinstance(obj, list):
                    return obj
                if isinstance(obj, dict):
                    for val in obj.values():
                        res = _find_first_list(val)
                        if res:
                            return res
                return None

            if species_list is None:
                species_list = _find_first_list(data)

            if not species_list:
                logger.warning("could not parse species list from API response: %s", url)
                return pd.DataFrame()

            df = pd.json_normalize(species_list)
            return df
        except requests.exceptions.HTTPError as e:
            logger.warning("could not fetch pollutant list from API (%s): %s", url, e)
            return pd.DataFrame()
        except Exception as e:
            logger.error("unexpected error fetching pollutants: %s", e)
            return pd.DataFrame()

    #to see which species are monitored at which sites.
    def get_site_species(self) -> pd.DataFrame:
        """fetch site-species combinations"""
        url = urljoin(self.base_url, "Information/MonitoringSiteSpecies/GroupName=London/csv")
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        if 'Sites' in data and 'Site' in data['Sites']:
            return pd.json_normalize(data['Sites']['Site'])
        return pd.DataFrame()


    """
    Fetching measurements for 2023-01-01- 2023-01-08 7 days to see if it works.

    @MeasurementDateGMT,@LocalAuthorityName,@SiteCode,@SiteName,@SiteType,
    @SpeciesCode,@Value,@DateClosed,@DateOpened,@Latitude,@Longitude

    By default searches only these species:NO2, O3, PM10, PM25, SO2

    start/end date strings "YYYY-MM-DD".
    """
def get_hourly_7days_fixed(site_codes=None, start_date="2023-01-01", end_date="2023-01-08", 
                          species=None, output_file="weekly_data.csv", max_sites=None):
    """
    collect hourly data for specified date range
    
    args:
        site_codes: list of site codes or None to get all sites
        start_date: start date in iso format "2023-01-01" 
        end_date: end date in iso format "2023-01-08"
        species: list of species codes or None for default
        output_file: output csv filename
        max_sites: limit number of sites
    
    returns:
        dict with results
    """
    
    species = species or ["NO2", "O3", "PM10", "PM25", "SO2"]
    
    # get sites.
    if not site_codes:
        print("fetching london sites...")
        api = LAQN_API()
        sites_df = api.get_sites()
        if sites_df.empty:
            return {"error": "no sites found", "out_file": None, "rows": 0}
        #list of all monitoring site codes in london 
        site_codes = sites_df['@SiteCode'].tolist()
        if max_sites:
            site_codes = site_codes[:max_sites]
            print(f"limited to {max_sites} sites")
    
    print(f"processing {len(site_codes)} sites")
    
    # converting dates to api format
    start_api = datetime.fromisoformat(start_date).strftime("%d %b %Y")
    end_api = datetime.fromisoformat(end_date).strftime("%d %b %Y")
    
    print(f"api date range: {start_api} to {end_api}")
    
    records = []
    successful_requests = 0
    failed_requests = 0
    
    for site_code in site_codes:
        print(f"processing site {site_code}...")
        
        for species_code in species:
            url = f"{LAQN_API.base_url}Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_api}/EndDate={end_api}/Json"
            
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    
                    # navigate json structure
                    if 'RawAQData' in data and 'Data' in data['RawAQData']:
                        measurements = data['RawAQData']['Data']
                        if not isinstance(measurements, list):
                            measurements = [measurements]
                        
                        site_info = data['RawAQData']
                        
                        for m in measurements:
                            record = {
                                '@MeasurementDateGMT': m.get('@MeasurementDateGMT'),
                                '@LocalAuthorityName': site_info.get('@LocalAuthorityName', ''),
                                '@SiteCode': site_info.get('@SiteCode', site_code),
                                '@SiteName': site_info.get('@SiteName', ''),
                                '@SiteType': site_info.get('@SiteType', ''),
                                '@SpeciesCode': species_code,
                                '@Value': m.get('@Value'),
                                '@DateClosed': site_info.get('@DateClosed', ''),
                                '@DateOpened': site_info.get('@DateOpened', ''),
                                '@Latitude': site_info.get('@Latitude', ''),
                                '@Longitude': site_info.get('@Longitude', '')
                            }
                            records.append(record)
                        
                        successful_requests += 1
                        print(f"  {species_code}: {len(measurements)} measurements")
                    else:
                        print(f"  {species_code}: no data structure")
                        failed_requests += 1
                else:
                    print(f"  {species_code}: http {response.status_code}")
                    failed_requests += 1
                    
            except Exception as e:
                print(f"  {species_code}: error {e}")
                failed_requests += 1
            
            time.sleep(0.3)
    
    # save to csv
    if records:
        df = pd.DataFrame(records)
        df.to_csv(output_file, index=False)
        
        
        return {"out_file": output_file, "rows": len(records), "successful": successful_requests, "failed": failed_requests}
    else:
        print("no data collected")
        return {"out_file": None, "rows": 0, "successful": 0, "failed": failed_requests}

def collect_working_combinations(output_file="london_jan2023_data.csv"):
    """collect data for proven working site-species combinations from test_api.py"""
    
    # proven working combinations
    working_sites = {
        'BL0': ['NO2', 'O3', 'PM10', 'PM25', 'SO2'],
        'LW2': ['NO2', 'O3', 'PM10'], 
        'CT2': ['CO', 'NO2', 'PM10'],
        'MY1': ['CO', 'NO2', 'PM10', 'PM25'],
        'CD1': ['CO', 'NO2', 'PM10']
    }
    
    
    # collect using your proven combinations
    site_codes = list(working_sites.keys())
    all_species = []
    for species_list in working_sites.values():
        all_species.extend(species_list)
    unique_species = list(set(all_species))
    
    result = get_hourly_7days_fixed(
        site_codes=site_codes,
        start_date="2023-01-01", 
        end_date="2023-01-31",  # full january
        species=unique_species,
        output_file=output_file
    )
    
    return result

def collect_weekly_sample(output_file="london_weekly_sample.csv"):
    """collect small weekly sample for testing"""
    
    # use proven working sites
    working_sites = ['BL0', 'MY1', 'CT2']
    working_species = ['NO2', 'PM10', 'CO']
    
    print("collecting weekly sample for testing")
    
    result = get_hourly_7days_fixed(
        site_codes=working_sites,
        start_date="2023-01-01",
        end_date="2023-01-08", 
        species=working_species,
        output_file=output_file
    )
    
    return result


def collect_year_parallel(
    year: int,
    output_file: str = None,
    species: Optional[List[str]] = None,
    max_workers: int = 24,
    pause_s: float = 0.05,
    max_sites: Optional[int] = None,
) -> Dict:
    """
    Collect full year of data from LAQN API using parallel processing.
    
    Args:
        year: Year to collect (e.g., 2023, 2024)
        output_file: Output CSV filename (auto-generated if None)
        species: List of pollutant codes (default: ["CO", "NO2", "O3", "PM10", "PM25", "SO2"])
        max_workers: Number of parallel threads
        pause_s: Pause between API calls per thread
        max_sites: Limit number of sites (for testing)
    
    Returns:
        Dict with collection statistics
    """
    
    # Default species to collect
    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]
    
    # Auto-generate output filename if not provided
    if output_file is None:
        output_file = f"data/raw/tests/LAQN_2023_parallel.csv"
    
    # Set date strings (ISO) then format to LAQN API form per request
    start_iso = f"{year}-01-01"
    end_iso = f"{year}-12-31"

    # use LAQN_API instance and session
    api = LAQN_API()
    sites_df = api.get_sites()
    base = api.base_url
    
    if sites_df is None or sites_df.empty:
        return {
            "error": "No sites available",
            "out_file": None,
            "rows": 0,
            "year": year
        }
    
    # Extract site codes
    site_col = next(
        (c for c in ("@SiteCode", "SiteCode", "siteCode") 
         if c in sites_df.columns), 
        sites_df.columns[0]
    )
    
    site_codes = sites_df[site_col].astype(str).unique().tolist()
    print(f"Found {len(site_codes)} sites")
    
    if max_sites:
        site_codes = site_codes[:int(max_sites)]
        print(f"Limited to {max_sites} sites for testing")
    
    # Build metadata map once
    meta = {}
    for _, r in sites_df.iterrows():
        code = r.get(site_col)
        if pd.isna(code) or code is None:
            continue
        meta[str(code)] = r.to_dict()
    
    # Helper to find nested list in JSON
    def _find_list(obj):
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            for v in obj.values():
                res = _find_list(v)
                if res:
                    return res
        return None
    
    # Per-site worker: fetch all species for one site
    def _worker_fetch(site_code: str):
        """Fetch all species data for a single site"""
        records = []
        
        for sp in species:
            # format dates to LAQN expected "01 Jan 2023"
            start_api = datetime.fromisoformat(start_iso).strftime("%d %b %Y")
            end_api = datetime.fromisoformat(end_iso).strftime("%d %b %Y")
            # Build API URL using base and quoting values
            url = (
                f"{base}Data/SiteSpecies/"
                f"SiteCode={quote(str(site_code))}/"
                f"SpeciesCode={quote(str(sp))}/"
                f"StartDate={quote(start_api)}/"
                f"EndDate={quote(end_api)}/"
                f"Json"
            )
            
            try:
                # use api.session for pooling and retries
                response = api.session.get(url, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    
                    # navigate json structure
                    if 'RawAQData' in data and 'Data' in data['RawAQData']:
                        measurements = data['RawAQData']['Data']
                        if not isinstance(measurements, list):
                            measurements = [measurements]
                        
                        site_info = data['RawAQData']
                        
                        for m in measurements:
                            record = {
                                '@MeasurementDateGMT': m.get('@MeasurementDateGMT'),
                                '@LocalAuthorityName': site_info.get('@LocalAuthorityName', ''),
                                '@SiteCode': site_info.get('@SiteCode', site_code),
                                '@SiteName': site_info.get('@SiteName', ''),
                                '@SiteType': site_info.get('@SiteType', ''),
                                '@SpeciesCode': sp,
                                '@Value': m.get('@Value'),
                                '@DateClosed': site_info.get('@DateClosed', ''),
                                '@DateOpened': site_info.get('@DateOpened', ''),
                                '@Latitude': site_info.get('@Latitude', ''),
                                '@Longitude': site_info.get('@Longitude', '')
                            }
                            records.append(record)
                else:
                    logger.warning("HTTP error %s for site %s, species %s", response.status_code, site_code, sp)
            except Exception as e:
                logger.error("Error fetching data for site %s, species %s: %s", site_code, sp, e)
        
        return records if records else None
    
    # Global collect results
    all_records = []
    success = 0
    fail = 0
    total_sites = len(site_codes)
    start_t = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(_worker_fetch, s): s for s in site_codes}
        with tqdm(total=total_sites, desc="Sites", unit="site") as pbar:
            for fut in concurrent.futures.as_completed(futures):
                s = futures[fut]
                try:
                    r = fut.result()
                    if r:
                        all_records.extend(r)
                        success += 1
                    else:
                        fail += 1
                except Exception:
                    fail += 1
                elapsed = time.time() - start_t
                pbar.update(1)
                pbar.set_postfix({"succ": success, "fail": fail, "elapsed_s": int(elapsed)})
                time.sleep(pause_s)
    
    # Save all records to CSV
    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(output_file, index=False)
        return {
            "error": None,
            "out_file": output_file,
            "rows": len(all_records),
            "successful": success,
            "failed": fail,
            "year": year
        }
    else:
        return {
            "error": "No data collected",
            "out_file": None,
            "rows": 0,
            "year": year
        }
def collect_year_async(
    year: int = 2023,
    sites_csv: str = "data/raw/sites_code_name.csv",
    output_file: str = "data/raw/2023_async_parallel.csv",
    species: Optional[List[str]] = None,
    concurrency: int = 100,
    connector_limit: int = 100,
    retries: int = 2,
    pause_s: float = 0.0,
):
    """
    Async collector (fastest method for many HTTP requests).
    - concurrency: max concurrent in-flight requests (aiohttp semaphore)
    - connector_limit: aiohttp TCPConnector limit
    - species: list of species to probe (defaults to common list)
    Returns dict with stats.
    """
    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]

    # read sites
    p = Path(sites_csv)
    if not p.exists():
        return {"error": "sites csv missing", "out_file": None, "rows": 0}
    sites_df = pd.read_csv(p)
    site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
    site_codes = sites_df[site_col].astype(str).unique().tolist()

    start_api = datetime.fromisoformat(f"{year}-01-01").strftime("%d %b %Y")
    end_api = datetime.fromisoformat(f"{year}-12-31").strftime("%d %b %Y")
    api = LAQN_API()
    base = api.base_url

    total_tasks = len(site_codes) * len(species)
    q = asyncio.Queue(maxsize=1000)

    header = ["@MeasurementDateGMT","@LocalAuthorityName","@SiteCode","@SiteName","@SiteType","@SpeciesCode","@Value","@DateClosed","@DateOpened","@Latitude","@Longitude"]
    stats = {"rows": 0, "success_tasks": 0, "failed_tasks": 0}

    async def writer():
        with open(output_file, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=header)
            w.writeheader()
            while True:
                item = await q.get()
                if item is None:
                    q.task_done()
                    break
                w.writerow(item)
                stats["rows"] += 1
                q.task_done()

    async def _run():
         conn = aiohttp.TCPConnector(limit=connector_limit, force_close=False)
         timeout = aiohttp.ClientTimeout(total=120)
         sem = asyncio.Semaphore(concurrency)
         async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            worker_tasks = []
            writer_task = asyncio.create_task(writer())
            total_success = 0
            total_fail = 0
            for sc in site_codes:
                for sp in species:
                    worker_tasks.append(asyncio.create_task(
                        _fetch_and_enqueue(session, sem, q, base, sc, sp, start_api, end_api,
                                           retries=retries, timeout=timeout.total)
                    ))
                    if pause_s:
                        await asyncio.sleep(pause_s)
            for res_task in asyncio.as_completed(worker_tasks):
                success_count, fail_count = await res_task
                total_success += success_count
                total_fail += fail_count
            await q.put(None)
            await q.join()
            await writer_task
            return total_success, total_fail

    total_success, total_fail = asyncio.run(_run())

    return {"out_file": output_file, "rows": stats["rows"], "successful_tasks": total_success, "failed_tasks": total_fail}

async def _fetch_and_enqueue(session, sem, queue, base, site_code, sp, start_api, end_api, retries=2, timeout=60):
    url = f"{base}Data/SiteSpecies/SiteCode={quote(str(site_code))}/SpeciesCode={quote(str(sp))}/StartDate={quote(start_api)}/EndDate={quote(end_api)}/Json"
    attempt = 0
    while attempt <= retries:
        attempt += 1
        async with sem:
            try:
                async with session.get(url, timeout=timeout) as resp:
                    status = resp.status
                    text = await resp.text()
                    if status != 200:
                        # non-200, retry
                        if attempt <= retries:
                            await asyncio.sleep(0.5 * attempt)
                            continue
                        return 0, 1
                    try:
                        data = await resp.json()
                    except Exception:
                        # bad json
                        return 0, 1
                    raw = data.get("RawAQData", {})
                    measurements = raw.get("Data")
                    if measurements is None:
                        return 0, 1
                    if isinstance(measurements, dict):
                        measurements = [measurements]
                    count = 0
                    for m in measurements:
                        row = {
                            "@MeasurementDateGMT": m.get("@MeasurementDateGMT"),
                            "@LocalAuthorityName": raw.get("@LocalAuthorityName") or "",
                            "@SiteCode": raw.get("@SiteCode") or site_code,
                            "@SiteName": raw.get("@SiteName") or "",
                            "@SiteType": raw.get("@SiteType") or "",
                            "@SpeciesCode": sp,
                            "@Value": m.get("@Value"),
                            "@DateClosed": raw.get("@DateClosed") or "",
                            "@DateOpened": raw.get("@DateOpened") or "",
                            "@Latitude": raw.get("@Latitude") or "",
                            "@Longitude": raw.get("@Longitude") or ""
                        }
                        await queue.put(row)
                        count += 1
                    return count, 0
            except asyncio.TimeoutError:
                if attempt <= retries:
                    await asyncio.sleep(0.5 * attempt)
                    continue
                return 0, 1
            except Exception:
                if attempt <= retries:
                    await asyncio.sleep(0.5 * attempt)
                    continue
                return 0, 1
    return 0, 1

def collect_year_async_chunked(
    year: int = 2023,
    sites_csv: str = "data/raw/sites_code_name.csv",
    output_prefix: str = "data/raw/2023_async_chunk",
    species: Optional[List[str]] = None,
    concurrency: int = 60,
    connector_limit: int = 80,
    retries: int = 2,
    pause_s: float = 0.0,
    date_chunks: Optional[List[Tuple[str, str]]] = None,
) -> dict:
    """
    Fetch full year in chunks (default 4 quarters), each into its own CSV using the async collector.
    Returns summary dict with per-chunk stats and total rows.
    """
    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]
    if date_chunks is None:
        date_chunks = [
            (f"{year}-01-01", f"{year}-03-31"),
            (f"{year}-04-01", f"{year}-06-30"),
            (f"{year}-07-01", f"{year}-09-30"),
            (f"{year}-10-01", f"{year}-12-31"),
        ]

    summary = []
    total_rows = 0
    for idx, (start_iso, end_iso) in enumerate(date_chunks, start=1):
        start_api = datetime.fromisoformat(start_iso).strftime("%d %b %Y")
        end_api = datetime.fromisoformat(end_iso).strftime("%d %b %Y")
        chunk_out = f"{output_prefix}_chunk{idx}.csv"
        print(f"\nChunk {idx}: {start_iso} → {end_iso} -> {chunk_out}")
        res = collect_year_async(
            year=year,
            sites_csv=sites_csv,
            output_file=chunk_out,
            species=species,
            concurrency=concurrency,
            connector_limit=connector_limit,
            retries=retries,
            pause_s=pause_s,
        )
        res.update({"chunk": idx, "start": start_iso, "end": end_iso, "file": chunk_out})
        summary.append(res)
        total_rows += res.get("rows", 0)
        elapsed = perf_counter() - start
        done_chunks = idx
        remaining_chunks = len(date_chunks) - done_chunks
        avg_per_chunk = elapsed / done_chunks if done_chunks else 0
        eta = avg_per_chunk * remaining_chunks
        print(f"Chunk {idx} done. Elapsed: {elapsed:.1f}s, ETA: {eta:.1f}s")
    summary_file = f"{output_prefix}_summary.csv"
    pd.DataFrame(summary).to_csv(summary_file, index=False)
    return {"chunks": summary, "total_rows": total_rows, "summary_file": summary_file}

def combine_chunks_to_hourly_wide(
    chunk_files: List[str],
    output_file: str = "data/raw/2023_async_hourly_wide.csv",
) -> pd.DataFrame:
    """
    Combine chunk CSVs and pivot to one row per hour/site, columns per species.
    Returns the wide DataFrame and writes it to CSV.
    """
    frames = []
    for fpath in chunk_files:
        p = Path(fpath)
        if p.exists():
            frames.append(pd.read_csv(p))
    if not frames:
        raise FileNotFoundError("no chunk files found to combine")

    df = pd.concat(frames, ignore_index=True)
    # ensure timestamp is parsed
    df["@MeasurementDateGMT"] = pd.to_datetime(df["@MeasurementDateGMT"], errors="coerce")
    df = df.dropna(subset=["@MeasurementDateGMT", "@SpeciesCode"])
    # pivot: index = timestamp + site, columns = species, values = measurement
    wide = (
        df.pivot_table(
            index=["@MeasurementDateGMT", "@SiteCode"],
            columns="@SpeciesCode",
            values="@Value",
            aggfunc="first",
        )
        .reset_index()
        .sort_values(["@SiteCode", "@MeasurementDateGMT"])
    )
    wide.columns.name = None
    wide.to_csv(output_file, index=False)
    return wide

def estimate_total_runtime(
    year: int = 2023,
    sites_csv: str = "data/raw/sites_code_name.csv",
    species: Optional[List[str]] = None,
    concurrency: int = 60,
    date_chunks: Optional[List[Tuple[str, str]]] = None,
    sample_sites: int = 5,
    sample_species: int = 2,
    repeats: int = 2,
) -> Dict:
    """
    Probe a few API requests to estimate total runtime.

    Returns dict with:
      - avg_request_s: average seconds per request (measured)
      - total_requests: total requests to perform (sites * species * chunks)
      - concurrency: concurrency used in estimate
      - eta_seconds: estimated wall time in seconds
      - eta_human: human readable ETA
    """

    species = species or ["CO", "NO2", "O3", "PM10", "PM25", "SO2"]
    if date_chunks is None:
        date_chunks = [
            (f"{year}-01-01", f"{year}-03-31"),
            (f"{year}-04-01", f"{year}-06-30"),
            (f"{year}-07-01", f"{year}-09-30"),
            (f"{year}-10-01", f"{year}-12-31"),
        ]
    # load site list from CSV; fallback to API sites
    p = Path(sites_csv)
    if p.exists():
        sites_df = pd.read_csv(p)
        site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
        site_codes = sites_df[site_col].astype(str).unique().tolist()
    else:
        api = LAQN_API()
        sites_df = api.get_sites()
        if sites_df is None or sites_df.empty:
            return {"error": "no sites available to estimate"}
        site_col = next((c for c in ("@SiteCode", "SiteCode", "siteCode") if c in sites_df.columns), sites_df.columns[0])
        site_codes = sites_df[site_col].astype(str).unique().tolist()

    if not site_codes:
        return {"error": "no site codes found"}

    # choose samples
    sample_sites = min(sample_sites, len(site_codes))
    sample_species = min(sample_species, len(species))
    samples_sites = random.sample(site_codes, sample_sites)
    samples_species = random.sample(species, sample_species)

    api = LAQN_API()
    base = api.base_url

    # use first chunk date range for timing probe
    start_iso, end_iso = date_chunks[0]
    start_api = datetime.fromisoformat(start_iso).strftime("%d %b %Y")
    end_api = datetime.fromisoformat(end_iso).strftime("%d %b %Y")

    timings = []
    for sc in samples_sites:
        for sp in samples_species:
            url = (
                f"{base}Data/SiteSpecies/SiteCode={quote(str(sc))}/"
                f"SpeciesCode={quote(str(sp))}/StartDate={quote(start_api)}/EndDate={quote(end_api)}/Json"
            )
            for _ in range(repeats):
                t0 = perf_counter()
                try:
                    r = api.session.get(url, timeout=60)
                    # read small slice to ensure transfer
                    _ = r.text[:1]
                    dt = perf_counter() - t0
                    timings.append(dt)
                except Exception:
                    # if request fails, count as a longer attempt to be conservative
                    timings.append(5.0)
                time.sleep(0.1)

    if not timings:
        return {"error": "no timings collected"}

    avg_request_s = sum(timings) / len(timings)
    n_sites = len(site_codes)
    n_species = len(species)
    n_chunks = len(date_chunks)
    total_requests = n_sites * n_species * n_chunks

    # estimated wall time assuming perfect saturation of concurrency
    eta_seconds = math.ceil(total_requests / max(1, concurrency)) * avg_request_s

    def _fmt(s):
        s = int(round(s))
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        if h:
            return f"{h}h{m:02d}m{sec:02d}s"
        if m:
            return f"{m}m{sec:02d}s"
        return f"{sec}s"

    return {
        "avg_request_s": round(avg_request_s, 3),
        "sampled_requests": len(timings),
        "total_sites": n_sites,
        "total_species": n_species,
        "chunks": n_chunks,
        "total_requests": total_requests,
        "concurrency": concurrency,
        "eta_seconds": int(eta_seconds),
        "eta_human": _fmt(eta_seconds),
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch LAQN data in quarterly chunks and pivot to hourly-wide CSV.")
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument("--sites", default="data/raw/sites_code_name.csv")
    parser.add_argument("--prefix", default="data/raw/2023_async")
    parser.add_argument("--concurrency", type=int, default=60)
    parser.add_argument("--connector-limit", type=int, default=80)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--pause", type=float, default=0.0)
    parser.add_argument("--pivot", action="store_true", help="Combine chunk CSVs into hourly-wide format")
    args = parser.parse_args()

    start = perf_counter()
    summary = collect_year_async_chunked(
        year=args.year,
        sites_csv=args.sites,
        output_prefix=args.prefix,
        concurrency=args.concurrency,
        connector_limit=args.connector_limit,
        retries=args.retries,
        pause_s=args.pause,
    )
    print(summary)
    print(f"elapsed={perf_counter()-start:.1f}s")

    if args.pivot:
        chunk_files = [chunk["file"] for chunk in summary["chunks"]]
        wide = combine_chunks_to_hourly_wide(chunk_files, f"{args.prefix}_hourly_wide.csv")
        print("hourly-wide shape:", wide.shape)