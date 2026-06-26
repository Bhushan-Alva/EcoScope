"""
Initial backfill: builds data/raw/weather/year_YYYY.parquet for each
year from START_YEAR to the current year, each file containing ALL
cities in city_list_with_coords_fixed.csv.

IMPORTANT - Open-Meteo's real call cost is NOT 1-request-per-call:
"Requests for data covering more than 10 weather variables or
extending over a period of more than 2 weeks for a single location
are considered multiple API calls... a request for 2 weeks of data
with 15 weather variables is calculated as 1.5 API calls, while 4
weeks equals 3.0 API calls." (open-meteo.com/en/pricing)

With 22 variables x 52 weeks, EACH city-year request actually costs:
    (52 weeks / 2) x (22 vars / 10) = ~57 effective calls
100 cities x 6 years x 57 = ~34,000 effective calls - over 3x the
10,000/day free limit. This is why slowing down requests alone (our
earlier fix) didn't solve sustained 429s: it's a quota-size problem,
not a burst-speed problem.

THE FIX: this script tracks estimated cumulative cost as it runs and
STOPS ITSELF before exceeding a safe daily budget, saving progress
incrementally (one shard per city-year, immediately after each
successful fetch). Re-running the script on a later day picks up
exactly where it left off - already-completed city-years are skipped,
not re-fetched. After enough days, run consolidate_shards.py to merge
shards into the final year_YYYY.parquet files.
"""

import pandas as pd
import time
import datetime
import sys
from pathlib import Path

from fetch_core import fetch_city_year, attach_city_metadata, HOURLY_VARS

START_YEAR = 2021
OUTPUT_DIR = Path("data/raw/weather")
SHARD_DIR = OUTPUT_DIR / "shards"
CITIES_CSV = "data/metadata/city_list_with_coords_fixed.csv"

DAILY_BUDGET = 7000  # 70% of the 10,000/day limit, leaving margin for
                      # retries, other scripts, and any other Open-Meteo
                      # endpoint usage that day

N_VARS = len(HOURLY_VARS.split(","))


def estimate_call_cost(start_date, end_date):
    """
    Open-Meteo's fractional-call formula: (weeks/2) x (vars/10).
    Used here purely to track OUR OWN cumulative spend against the
    daily budget - not sent to the API, just our own bookkeeping.
    """
    days = (pd.Timestamp(end_date) - pd.Timestamp(start_date)).days + 1
    weeks = days / 7
    return (weeks / 2) * (N_VARS / 10)


def shard_path(rank, year):
    return SHARD_DIR / f"city{int(rank):03d}_year{year}.parquet"


def main():
    cities_path = Path(CITIES_CSV)
    if not cities_path.exists():
        print(f"ERROR: {CITIES_CSV} not found. Run geocode_cities.py first.")
        sys.exit(1)

    cities_df = pd.read_csv(cities_path)
    valid_cities = cities_df.dropna(subset=["latitude", "longitude"])
    print(f"Loaded {len(valid_cities)} valid cities.\n")

    current_year = datetime.date.today().year
    years = list(range(START_YEAR, current_year + 1))

    SHARD_DIR.mkdir(parents=True, exist_ok=True)

    # Build the full work queue: every (city, year) combination
    work_queue = [
        (row, year)
        for _, row in valid_cities.iterrows()
        for year in years
    ]

    # Skip anything already shard-saved from a previous run (today or
    # an earlier day) - this is what makes the script resumable
    pending = [
        (row, year) for row, year in work_queue
        if not shard_path(row["rank"], year).exists()
    ]
    already_done = len(work_queue) - len(pending)

    print(f"Total work items (city x year): {len(work_queue)}")
    print(f"Already completed (found existing shards): {already_done}")
    print(f"Remaining: {len(pending)}")
    print(f"Today's effective-call budget: {DAILY_BUDGET}\n")

    if not pending:
        print("Nothing left to do - all city-years already backfilled.")
        print("Run consolidate_shards.py to merge shards into year_YYYY.parquet files.")
        return

    spent = 0.0
    completed_this_run = 0
    failed_this_run = []

    for row, year in pending:
        rank, name, state, tier = row["rank"], row["name"], row["state"], row["tier"]

        start_date = f"{year}-01-01"
        year_end = datetime.date(year, 12, 31)
        safe_today = datetime.date.today() - datetime.timedelta(days=2)
        end_date = str(min(year_end, safe_today))
        if pd.Timestamp(end_date) < pd.Timestamp(start_date):
            continue  # future year, nothing to fetch yet

        cost = estimate_call_cost(start_date, end_date)
        if spent + cost > DAILY_BUDGET:
            print(f"\nBudget reached ({spent:.0f}/{DAILY_BUDGET} effective calls spent).")
            print(f"Stopping here for today - {len(pending) - completed_this_run} "
                  f"city-years still remain.")
            print(f"Re-run this script again later (today or tomorrow, depending on")
            print(f"when your daily quota resets) to continue from this point.")
            break

        try:
            df = fetch_city_year(row["latitude"], row["longitude"], year)
            if df is None:
                continue
            df = attach_city_metadata(df, rank, name, state, tier,
                                       row["latitude"], row["longitude"])
            df.to_parquet(shard_path(rank, year), index=False)
            spent += cost
            completed_this_run += 1
            print(f"  [{int(rank):>3}] {name:25} {year} -> {len(df)} hours OK "
                  f"(spent {spent:.0f}/{DAILY_BUDGET})")
        except Exception as e:
            print(f"  [{int(rank):>3}] {name:25} {year} -> FAILED: {e}")
            failed_this_run.append((rank, name, state, tier,
                                     row["latitude"], row["longitude"], year))
            spent += cost  # count it - the attempt still cost quota

        time.sleep(1.5)

    print(f"\n{'='*60}")
    print(f"RUN SUMMARY")
    print(f"{'='*60}")
    print(f"Completed this run: {completed_this_run}")
    print(f"Failed this run: {len(failed_this_run)}")
    print(f"Effective calls spent: {spent:.0f}/{DAILY_BUDGET}")

    total_shards = len(list(SHARD_DIR.glob("city*_year*.parquet")))
    print(f"Total shards on disk now: {total_shards}/{len(work_queue)}")

    if failed_this_run:
        failed_df = pd.DataFrame(
            failed_this_run,
            columns=["rank", "name", "state", "tier", "latitude", "longitude", "year"],
        )
        failed_path = OUTPUT_DIR / "failed_this_run.csv"
        failed_df.to_csv(failed_path, index=False)
        print(f"Failed city-years saved to {failed_path}")

    if total_shards < len(work_queue):
        print(f"\nNot done yet - re-run this script to continue "
              f"({len(work_queue) - total_shards} city-years remaining).")
    else:
        print(f"\nAll city-years collected. Run consolidate_shards.py next.")


if __name__ == "__main__":
    main()
