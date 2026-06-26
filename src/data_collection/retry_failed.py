"""
Retry cities that failed during backfill_by_year.py (saved to
data/raw/weather/failed_YYYY.csv) and append any that now succeed
into the existing year_YYYY.parquet file.

Usage:
    python retry_failed.py 2021
    python retry_failed.py 2021 2022 2023   # multiple years at once
"""

import sys
import time
import pandas as pd
from pathlib import Path

from fetch_core import fetch_city_year, attach_city_metadata

OUTPUT_DIR = Path("data/raw/weather")


def retry_year(year):
    failed_path = OUTPUT_DIR / f"failed_{year}.csv"
    year_path = OUTPUT_DIR / f"year_{year}.parquet"

    if not failed_path.exists():
        print(f"No failed_{year}.csv found - nothing to retry for {year}.")
        return

    failed_df = pd.read_csv(failed_path)
    print(f"\n{'='*60}")
    print(f"YEAR {year}: retrying {len(failed_df)} previously failed cities")
    print(f"{'='*60}")

    existing_df = pd.read_parquet(year_path) if year_path.exists() else None
    new_frames = []
    still_failed = []

    for _, row in failed_df.iterrows():
        rank, name, state, tier = row["rank"], row["name"], row["state"], row["tier"]
        try:
            df = fetch_city_year(row["latitude"], row["longitude"], year)
            if df is None:
                print(f"  [{int(rank):>3}] {name:25} -> SKIPPED (year not available)")
                continue
            df = attach_city_metadata(df, rank, name, state, tier,
                                       row["latitude"], row["longitude"])
            new_frames.append(df)
            print(f"  [{int(rank):>3}] {name:25} -> {len(df)} hours OK (recovered)")
        except Exception as e:
            print(f"  [{int(rank):>3}] {name:25} -> STILL FAILED: {e}")
            still_failed.append(row.to_dict())

        time.sleep(1.5)

    if new_frames:
        new_df = pd.concat(new_frames, ignore_index=True)
        combined = pd.concat([existing_df, new_df], ignore_index=True) if existing_df is not None else new_df
        combined.to_parquet(year_path, index=False)
        print(f"\n  Appended {len(new_frames)} recovered cities into {year_path}")
        print(f"  {year_path.name} now has {combined['city'].nunique()} cities, "
              f"{len(combined):,} rows")

    if still_failed:
        pd.DataFrame(still_failed).to_csv(failed_path, index=False)
        print(f"  {len(still_failed)} cities still failing - kept in {failed_path}")
    else:
        failed_path.unlink()
        print(f"  All cities recovered - removed {failed_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    for year_arg in sys.argv[1:]:
        retry_year(int(year_arg))
