"""
Add ONE new city into every existing year_YYYY.parquet file, without
re-fetching or rewriting any existing city's data.

Usage:
    python add_new_city.py "City Name" "State" <rank> <tier> <lat> <lon>

Example:
    python add_new_city.py "Shimla" "Himachal Pradesh" 101 3 31.1048 77.1734

This also appends the new city to city_list_with_coords_fixed.csv so
future runs (and add_new_city.py re-runs for ANOTHER new city) see it
as part of the master list.
"""

import sys
import pandas as pd
from pathlib import Path

from fetch_core import fetch_city_year, attach_city_metadata

OUTPUT_DIR = Path("data/raw/weather")
CITIES_CSV = "data/metadata/city_list_with_coords_fixed.csv"


def main():
    if len(sys.argv) != 7:
        print(__doc__)
        sys.exit(1)

    name, state, rank, tier, lat, lon = sys.argv[1:7]
    rank, tier, lat, lon = int(rank), int(tier), float(lat), float(lon)

    year_files = sorted(OUTPUT_DIR.glob("year_*.parquet"))
    if not year_files:
        print(f"ERROR: no existing year files found in {OUTPUT_DIR}. "
              f"Run backfill_by_year.py first.")
        sys.exit(1)

    print(f"Adding '{name}' ({state}, tier {tier}) at ({lat}, {lon})")
    print(f"Found {len(year_files)} existing year-files to update.\n")

    for year_file in year_files:
        year = int(year_file.stem.split("_")[1])

        existing_df = pd.read_parquet(year_file)
        if name in existing_df["city"].unique():
            print(f"  {year_file.name}: '{name}' already present - skipping fetch.")
            continue

        print(f"  {year_file.name}: fetching {year} data for '{name}'...")
        new_df = fetch_city_year(lat, lon, year)
        if new_df is None:
            print(f"    -> SKIPPED (year {year} not yet available)")
            continue

        new_df = attach_city_metadata(new_df, rank, name, state, tier, lat, lon)

        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_parquet(year_file, index=False)
        print(f"    -> appended {len(new_df)} rows "
              f"(file now has {updated_df['city'].nunique()} cities, "
              f"{len(updated_df):,} total rows)")

    # update the master city list CSV too
    cities_df = pd.read_csv(CITIES_CSV)
    if name not in cities_df["name"].values:
        new_row = pd.DataFrame([{
            "rank": rank, "name": name, "state": state, "tier": tier,
            "latitude": lat, "longitude": lon,
            "matched_name": name, "geocode_status": "OK_MANUAL_ADD",
        }])
        cities_df = pd.concat([cities_df, new_row], ignore_index=True)
        cities_df.to_csv(CITIES_CSV, index=False)
        print(f"\nAdded '{name}' to {CITIES_CSV} (master city list).")
    else:
        print(f"\n'{name}' already in {CITIES_CSV} - not duplicated.")

    print("\nDone.")


if __name__ == "__main__":
    main()
