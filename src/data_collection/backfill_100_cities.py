"""
Step 2: backfill hourly historical solar/weather data starting
2025-01-01 for all 100 cities (from city_list_with_coords.csv,
produced by geocode_cities.py).

Each city = ONE API call covering the full date range (proven
pattern from earlier tests - the archive endpoint returns a whole
year in a single request).

Variables pulled (raw, no tilt/azimuth - computed offline later
with pvlib as established earlier):
  - direct_normal_irradiance, diffuse_radiation, shortwave_radiation
    (for solar/tilt analysis)
  - temperature_2m, cloud_cover (general weather context)

Output: one combined CSV with a 'tier' and 'city' column, ready for
pandas groupby analysis (e.g. df.groupby('tier').mean()).
"""

import requests
import pandas as pd
import time
import sys
from pathlib import Path

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
START_DATE = "2025-01-01"

HOURLY_VARS = "direct_normal_irradiance,diffuse_radiation,shortwave_radiation,temperature_2m,cloud_cover"


def get_end_date():
    """Archive endpoint needs a finalized past date - use 2 days ago."""
    import datetime
    return str(datetime.date.today() - datetime.timedelta(days=2))


def fetch_city_data(lat, lon, start_date, end_date):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": HOURLY_VARS,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
    }
    resp = requests.get(ARCHIVE_URL, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main():
    cities_path = Path(r"C:\Users\bhush\OneDrive\Desktop\DS Projects\Solar\city_list_with_coords_fixed.csv")
    if not cities_path.exists():
        print("ERROR: city_list_with_coords.csv not found.")
        print("Run geocode_cities.py first to generate it.")
        sys.exit(1)

    cities_df = pd.read_csv(cities_path)
    valid_cities = cities_df.dropna(subset=["latitude", "longitude"])
    skipped = len(cities_df) - len(valid_cities)
    if skipped:
        print(f"WARNING: skipping {skipped} cities with missing coordinates "
              f"(failed geocoding) - check city_list_with_coords.csv\n")

    end_date = get_end_date()
    print(f"Backfilling {START_DATE} to {end_date} for {len(valid_cities)} cities...")
    print(f"(1 API call per city, ~{len(valid_cities)} calls total - well under the "
          f"10,000/day free-tier limit)\n")

    all_frames = []
    failed = []

    for i, row in valid_cities.iterrows():
        rank, name, state, tier = row["rank"], row["name"], row["state"], row["tier"]
        try:
            data = fetch_city_data(row["latitude"], row["longitude"], START_DATE, end_date)
            h = data["hourly"]
            n_hours = len(h["time"])

            df = pd.DataFrame({
                "time": h["time"],
                "dni": h["direct_normal_irradiance"],
                "dhi": h["diffuse_radiation"],
                "ghi": h["shortwave_radiation"],
                "temperature_2m": h["temperature_2m"],
                "cloud_cover": h["cloud_cover"],
            })
            df["city"] = name
            df["state"] = state
            df["rank"] = rank
            df["tier"] = tier
            df["latitude"] = row["latitude"]
            df["longitude"] = row["longitude"]

            all_frames.append(df)
            print(f"  [{int(rank):>3}] Tier {int(tier)}  {name:25} -> {n_hours} hours OK")

        except Exception as e:
            print(f"  [{int(rank):>3}] Tier {int(tier)}  {name:25} -> FAILED: {e}")
            failed.append(name)

        time.sleep(0.2)  # polite pacing, nowhere near the 600/min limit

    if not all_frames:
        print("\nNo data collected - aborting.")
        sys.exit(1)

    combined = pd.concat(all_frames, ignore_index=True)
    out_path = r"C:\Users\bhush\OneDrive\Desktop\DS Projects\Solar\solar_weather_100cities_2025.csv"
    combined.to_csv(out_path, index=False)

    print(f"\n{'='*60}")
    print(f"Done. {len(all_frames)}/{len(valid_cities)} cities succeeded.")
    print(f"Total rows: {len(combined):,}")
    print(f"Saved to: {out_path}")
    if failed:
        print(f"\nFailed cities (re-run individually to debug): {failed}")

    print(f"\nRows per tier:")
    print(combined.groupby("tier")["city"].nunique().rename("n_cities"))


if __name__ == "__main__":
    main()
