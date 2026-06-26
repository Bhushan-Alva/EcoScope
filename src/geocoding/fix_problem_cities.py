"""
Fix script for the 4 problem rows from
data/metadata/city_list_with_coords.csv:

1. Vasai-Virar       -> try "Vasai" (twin-city name, geocoder likely
                         only knows the individual towns, not the
                         merged municipal corporation name)
2. Chhatrapati Sambhajinagar -> try "Aurangabad, Maharashtra" (city was
                         renamed in 2023; GeoNames-based geocoders often
                         lag behind official renames)
3. Mira-Bhayandar    -> try "Mira Bhayandar" (no hyphen) or "Mira Road"
4. Gurgaon           -> try "Gurugram" (official rename in 2016) -
                         IMPORTANT: the original geocode for "Gurgaon"
                         returned (19.34, 77.27), which is in
                         Maharashtra, nowhere near the real Gurgaon
                         near Delhi (~28.4N) - that result must be
                         discarded, not just relabeled.

Run this, inspect the output, then manually patch
city_list_with_coords.csv with whichever result looks correct
(cross-check the lat/lon against a quick mental sanity check -
e.g. Gurugram should be ~28.4N, 77.0E, near Delhi).
"""

import requests
import time

ALTERNATE_QUERIES = {
    29:  ["Vasai-Virar", "Vasai", "Virar"],
    32:  ["Chhatrapati Sambhajinagar", "Aurangabad"],
    60:  ["Mira-Bhayandar", "Mira Bhayandar", "Mira Road"],
    54:  ["Gurugram", "Gurgaon"],  # try the official new name first
}

EXPECTED_STATE = {
    29: "Maharashtra",
    32: "Maharashtra",
    60: "Maharashtra",
    54: "Haryana",
}


def search(name):
    resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": name, "count": 5, "language": "en", "format": "json"},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def main():
    for rank, queries in ALTERNATE_QUERIES.items():
        print(f"\n{'='*60}")
        print(f"Rank {rank} - expected state: {EXPECTED_STATE[rank]}")
        for q in queries:
            results = search(q)
            india_results = [r for r in results if r.get("country") == "India"]
            print(f"\n  Query: '{q}' -> {len(india_results)} India result(s)")
            for r in india_results[:3]:
                admin1 = r.get("admin1", "?")
                match_flag = " <-- STATE MATCHES, LIKELY CORRECT" if EXPECTED_STATE[rank].lower() in admin1.lower() else ""
                print(f"      {r.get('name')}, {admin1} -> "
                      f"({r['latitude']:.4f}, {r['longitude']:.4f}){match_flag}")
            time.sleep(0.2)

    print(f"\n{'='*60}")
    print("Review the '<-- STATE MATCHES' lines above.")
    print("Once you've picked the right coordinate for each, manually edit")
    print("data/metadata/city_list_with_coords.csv: fill in latitude/longitude")
    print("for rows 29, 32, 60, and REPLACE row 54's (wrong) coordinate with")
    print("the correct Gurugram one - do not just relabel the status column,")
    print("the actual lat/lon for Gurgaon in the file is wrong.")


if __name__ == "__main__":
    main()