"""
Delete ONE city from every existing year_YYYY.parquet file and remove it
from the master city list.

Usage:
    python delete_city.py "City Name"

Example:
    python delete_city.py "Shimla"
"""

import sys
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("data/raw/weather")
CITIES_CSV = "data/metadata/city_list_with_coords_fixed.csv"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    city_name = sys.argv[1]

    year_files = sorted(OUTPUT_DIR.glob("year_*.parquet"))

    if not year_files:
        print(f"ERROR: No parquet files found in {OUTPUT_DIR}")
        sys.exit(1)

    print(f"Deleting '{city_name}' from {len(year_files)} year files.\n")

    total_removed = 0

    for year_file in year_files:
        df = pd.read_parquet(year_file)

        if "city" not in df.columns:
            print(f"{year_file.name}: No 'city' column found. Skipping.")
            continue

        before = len(df)
        df = df[df["city"] != city_name]
        removed = before - len(df)

        if removed == 0:
            print(f"{year_file.name}: City not found.")
            continue

        df.to_parquet(year_file, index=False)

        total_removed += removed

        print(
            f"{year_file.name}: Removed {removed:,} rows "
            f"(remaining cities: {df['city'].nunique()}, "
            f"rows: {len(df):,})"
        )

    # Remove from master city list
    cities_df = pd.read_csv(CITIES_CSV)

    before = len(cities_df)
    cities_df = cities_df[cities_df["name"] != city_name]
    removed = before - len(cities_df)

    if removed:
        cities_df.to_csv(CITIES_CSV, index=False)
        print(f"\nRemoved '{city_name}' from {CITIES_CSV}.")
    else:
        print(f"\n'{city_name}' not found in {CITIES_CSV}.")

    print(f"\nDone. Total weather rows removed: {total_removed:,}")


if __name__ == "__main__":
    main()