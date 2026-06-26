"""
Shared core fetch logic for the year-partitioned weather data layer.
Used by BOTH backfill_by_year.py (initial pull) and add_new_city.py
(append a city into existing year-files) - so the column list and
fetch mechanics live in exactly ONE place.

Column -> module mapping (documented here so future changes are
deliberate, not accidental):

  dni, dhi, ghi              -> Solar (core radiation components)
  temperature_2m             -> Solar, Crop, Construction, Cold Chain,
                                 Tourism, Disaster, Urban Heat Island,
                                 Retail Footfall
  relative_humidity_2m       -> Solar, Crop, Construction
  rain                       -> Solar, Crop, Construction, Retail Footfall
  precipitation              -> Disaster (broader hazard signal incl. snow)
  wind_speed_10m             -> Solar, Construction, Disaster, Wind Energy
  wind_direction_10m         -> Solar (soiling), Wind Energy
  wind_gusts_10m             -> Construction, Disaster, Wind Energy
  wind_speed_100m            -> Wind Energy (turbine hub height)
  cloud_cover                -> Solar, Construction, Tourism, Retail Footfall
  sunshine_duration          -> Solar, Tourism
  weather_code               -> Solar, Construction, Tourism, Disaster,
                                 Retail Footfall (dashboard labels)
  snowfall, snow_depth       -> Solar/Construction/Disaster/Wind Energy
                                 (future non-India cities; ~0 for India now)
  et0_fao_evapotranspiration -> Crop (core)
  pressure_msl                -> Disaster (storm pressure-drop signal)
  surface_pressure            -> Disaster (kept alongside pressure_msl;
                                 the two are highly correlated at a
                                 single location, but both are cheap to
                                 carry and harmless if one ends up unused)
  vapour_pressure_deficit    -> Crop (plant stress), Construction
                                 (heat-stress signal for outdoor workers,
                                 combined with high temperature)
  apparent_temperature       -> Construction, Cold Chain, Tourism, Disaster,
                                 Retail Footfall
  wind_direction_100m        -> Wind Energy (turbine layout/wake effects
                                 depend on prevailing direction at hub
                                 height, not just speed - low priority,
                                 included for future completeness)

  dew_point_2m is DELIBERATELY EXCLUDED - derive it from temperature_2m
  + relative_humidity_2m via the Magnus formula instead of fetching it.
"""

import requests
import pandas as pd
import time

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

HOURLY_VARS = ",".join([
    "direct_normal_irradiance",
    "diffuse_radiation",
    "shortwave_radiation",
    "temperature_2m",
    "relative_humidity_2m",
    "rain",
    "precipitation",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_direction_100m",
    "wind_gusts_10m",
    "wind_speed_100m",
    "cloud_cover",
    "sunshine_duration",
    "weather_code",
    "snowfall",
    "snow_depth",
    "et0_fao_evapotranspiration",
    "pressure_msl",
    "surface_pressure",
    "vapour_pressure_deficit",
    "apparent_temperature",
])

# Friendly rename so columns are unambiguous in the saved files
COLUMN_RENAME = {
    "direct_normal_irradiance": "dni",
    "diffuse_radiation": "dhi",
    "shortwave_radiation": "ghi",
}


def fetch_city_year(lat, lon, year, max_retries=5, base_delay=5):
    """
    Fetch ONE city's full hourly data for ONE calendar year.
    Returns a DataFrame with a clean 'time' column plus all variables.

    Handles the current/incomplete year case (e.g. 2026) by capping
    end_date at 2 days ago, since the archive endpoint needs a
    finalized past date.

    Retries on HTTP 429 (rate limit) with exponential backoff:
    5s, 10s, 20s, 40s, 80s. With 22 columns x a full year, each
    response is much larger than our earlier tests used, which is
    why bursts of calls can trip a rate limit even with a short
    sleep between requests - this retries instead of giving up.
    """
    import datetime

    start_date = f"{year}-01-01"
    today = datetime.date.today()
    year_end = datetime.date(year, 12, 31)
    safe_today = today - datetime.timedelta(days=2)
    end_date = str(min(year_end, safe_today))

    if pd.Timestamp(end_date) < pd.Timestamp(start_date):
        # requested year is entirely in the future - nothing to fetch yet
        return None

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": HOURLY_VARS,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
    }

    for attempt in range(max_retries):
        resp = requests.get(ARCHIVE_URL, params=params, timeout=60)

        if resp.status_code == 429:
            if attempt == max_retries - 1:
                resp.raise_for_status()  # give up after final attempt, raise normally
            delay = base_delay * (2 ** attempt)
            print(f"    [rate limited - waiting {delay}s before retry "
                  f"{attempt + 1}/{max_retries}]")
            time.sleep(delay)
            continue

        resp.raise_for_status()  # raises for any other non-2xx (404, 500, etc.)
        data = resp.json()
        break

    h = data["hourly"]
    df = pd.DataFrame(h)
    df = df.rename(columns=COLUMN_RENAME)
    df["time"] = pd.to_datetime(df["time"])

    # derive dew point from temperature + humidity (Magnus formula)
    # rather than fetching it separately - see module docstring above
    df["dew_point_2m"] = derive_dew_point(df["temperature_2m"], df["relative_humidity_2m"])

    return df


def derive_dew_point(temp_c, rh_pct):
    """
    Magnus-Tetens approximation. Accurate to ~+/-0.1C for typical
    atmospheric conditions - standard, widely used formula.
    """
    import numpy as np
    b, c = 17.62, 243.12
    gamma = np.log(rh_pct / 100.0) + (b * temp_c) / (c + temp_c)
    return (c * gamma) / (b - gamma)


def attach_city_metadata(df, rank, name, state, tier, lat, lon):
    df = df.copy()
    df["city"] = name
    df["state"] = state
    df["rank"] = rank
    df["tier"] = tier
    df["latitude"] = lat
    df["longitude"] = lon
    return df
