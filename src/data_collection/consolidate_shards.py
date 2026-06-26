"""
Consolidate per-city-year shards (data/weather_core/shards/cityNNN_yearYYYY.parquet)
into the final year_YYYY.parquet files that the rest of the project
(Solar module, etc.) actually reads from.

Run this after backfill_by_year.py has completed - whether that took
one run or several resumed runs across multiple days due to the daily
quota budget.

Safe to re-run: it always rebuilds each year_YYYY.parquet fresh from
whatever shards currently exist, so partial progress is fine too -
you'll just get a year-file with fewer cities until the rest of the
shards are collected.
"""

import re
import pandas as pd
from pathlib import Path
from collections import defaultdict

OUTPUT_DIR = Path("data/weather_core")
SHARD_DIR = OUTPUT_DIR / "shards"

SHARD_PATTERN = re.compile(r"city(\d+)_year(\d+)\.parquet")


def main():
    shard_files = list(SHARD_DIR.glob("city*_year*.parquet"))
    if not shard_files:
        print(f"No shards found in {SHARD_DIR}. Run backfill_by_year.py first.")
        return

    by_year = defaultdict(list)
    for f in shard_files:
        m = SHARD_PATTERN.match(f.name)
        if not m:
            print(f"  WARNING: unrecognized shard filename, skipping: {f.name}")
            continue
        year = int(m.group(2))
        by_year[year].append(f)

    print(f"Found {len(shard_files)} shards across {len(by_year)} years.\n")

    for year in sorted(by_year):
        files = by_year[year]
        frames = [pd.read_parquet(f) for f in files]
        year_df = pd.concat(frames, ignore_index=True)

        out_path = OUTPUT_DIR / f"year_{year}.parquet"
        year_df.to_parquet(out_path, index=False)

        n_cities = year_df["city"].nunique()
        size_mb = out_path.stat().st_size / (1024 * 1024)
        print(f"  year_{year}.parquet: {n_cities} cities, "
              f"{len(year_df):,} rows, {size_mb:.1f} MB")

    print(f"\nDone. {len(by_year)} year-files written to {OUTPUT_DIR}")
    print("(Shards left in place - safe to delete once you've verified")
    print(f" the year-files look correct, to free up disk space: {SHARD_DIR})")


if __name__ == "__main__":
    main()
