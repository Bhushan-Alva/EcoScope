"""
Step 1 of the 100-city pipeline: geocode every city in city_list.py
using Open-Meteo's free geocoding API, filtered to India, disambiguated
by state where a name is ambiguous (e.g. multiple "Hyderabad" worldwide).

Output: city_list_with_coords.csv - the master file the backfill
script will read from.
"""

import requests
import pandas as pd
import time
from city_list import CITIES

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


def geocode_city(name, state, country="India"):
    """
    Look up a city's coordinates, filtering to India and preferring
    a result whose admin1 (state) field matches what we expect -
    this disambiguates cases like multiple towns sharing a name.
    """
    params = {"name": name, "count": 10, "language": "en", "format": "json"}
    resp = requests.get(GEOCODE_URL, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("results", [])
    if not results:
        return None, "NO_RESULTS"

    # filter to India
    india_results = [r for r in results if r.get("country") == "India"]
    if not india_results:
        return None, "NO_INDIA_MATCH"

    # prefer a result whose admin1 (state) matches our expected state
    state_matches = [
        r for r in india_results
        if state.lower() in r.get("admin1", "").lower()
        or r.get("admin1", "").lower() in state.lower()
    ]
    best = state_matches[0] if state_matches else india_results[0]

    flag = "OK" if state_matches else "STATE_MISMATCH_USED_FIRST_INDIA_MATCH"
    return best, flag


def main():
    rows = []
    print(f"Geocoding {len(CITIES)} cities (one call each, ~{len(CITIES)*0.3:.0f}s estimated)...\n")

    for rank, name, state, tier in CITIES:
        result, flag = geocode_city(name, state)
        if result is None:
            print(f"  [{rank:>3}] {name:30} -> FAILED ({flag})")
            rows.append({
                "rank": rank, "name": name, "state": state, "tier": tier,
                "latitude": None, "longitude": None,
                "matched_name": None, "geocode_status": flag,
            })
        else:
            flag_note = "" if flag == "OK" else f"  [WARNING: {flag}]"
            print(f"  [{rank:>3}] {name:30} -> "
                  f"({result['latitude']:.4f}, {result['longitude']:.4f}) "
                  f"matched '{result.get('name')}', {result.get('admin1', '?')}{flag_note}")
            rows.append({
                "rank": rank, "name": name, "state": state, "tier": tier,
                "latitude": result["latitude"], "longitude": result["longitude"],
                "matched_name": result.get("name"), "geocode_status": flag,
            })
        time.sleep(0.15)  # be polite, well under any rate limit

    df = pd.DataFrame(rows)
    df.to_csv("city_list_with_coords.csv", index=False)

    print(f"\n{'='*60}")
    print(f"Done. Saved to city_list_with_coords.csv")
    print(f"  OK: {(df['geocode_status']=='OK').sum()}")
    print(f"  Warnings (state mismatch, used first India match): "
          f"{(df['geocode_status']=='STATE_MISMATCH_USED_FIRST_INDIA_MATCH').sum()}")
    print(f"  Failed: {df['latitude'].isna().sum()}")
    print(f"\nReview any WARNING/FAILED rows manually before running the backfill -")
    print(f"a wrong coordinate silently pulls weather for the wrong place.")


if __name__ == "__main__":
    main()
