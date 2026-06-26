# Changelog

## Version 1.0 - Data Foundation

* Defined the 100-city list (`city_list.py`), ranked by 2011 Census
  population, split into Tier 1/2/3 (Tier 1 matches India's official
  "Million Plus Cities" definition; Tier 2/3 are our own convention -
  see `assumptions.md`).
* Geocoded all 100 cities via Open-Meteo's geocoding API
  (`geocode_cities.py`), with a state-match filter to disambiguate
  same-named places.
* Found and fixed 4 known problem cities (`fix_problem_cities.py`):
  Vasai-Virar, Chhatrapati Sambhajinagar (renamed from Aurangabad in
  2023), Mira-Bhayandar, and Gurgaon. The Gurgaon fix was the most
  serious - the original geocode landed in Maharashtra instead of
  Haryana, ~1,000+ km from the real city, and had to be discarded
  entirely rather than relabeled.
* Discovered Open-Meteo's real billing formula is NOT 1 HTTP call = 1
  API call: effective cost is `(weeks/2) x (vars/10)`. With 22
  variables across a full year, each city-year request costs ~57
  effective calls. The original backfill attempt (100 cities x 6 years)
  would have cost ~34,000 effective calls/day - over 3x the 10,000/day
  free-tier limit - which is what caused sustained HTTP 429 errors that
  retry/backoff alone couldn't fix.
* Rewrote the backfill as a resumable, daily-budget-aware queue
  (`backfill_by_year.py`): saves one shard per city-year immediately
  after each successful fetch, tracks cumulative estimated cost, and
  stops itself at a 7,000/day budget (leaving margin under the real
  limit). Re-running picks up exactly where it left off.
* Completed the full backfill: all 100 cities, 2021-01-01 through
  2026-06-24, zero gaps, zero duplicate timestamps, zero nulls across
  all 30 columns. Consolidated via `consolidate_shards.py` into
  `data/raw/weather/year_YYYY.parquet` (one file per year, 6 files
  total, ~4.8M rows).
* Validated the tilt/azimuth approach: fetch raw radiation components
  once (no tilt param), then use `pvlib` offline to compute tilted
  irradiance for any tilt/azimuth combination at zero extra API cost.
  Found that optimal tilt varies by season (~50 deg in winter, ~0 deg
  in summer for Delhi), with a ~25 deg annual compromise. See
  `assumptions.md` for the azimuth-at-flat-tilt caveat this uncovered.
* Started Phase 1 EDA (`notebooks/01_data_audit.ipynb`): loaded all 6
  year-files, confirmed shape and column structure.

## Fixes (post-backfill)

* Found and corrected a 3-way path mismatch: `backfill_by_year.py`,
  `consolidate_shards.py`, `add_new_city.py`, and `retry_failed.py` all
  hardcoded `data/weather_core/` as the output directory, but the
  actual delivered data lived at `data/raw/weather/`, and the working
  notebook on the local machine pointed at a third path (`data\weather`).
  Standardized all four scripts and the notebook on `data/raw/weather/`.
* Found and corrected a second path mismatch: `backfill_by_year.py` and
  `add_new_city.py` referenced the master city CSV as a bare filename
  (expecting it in the working directory), but the real file lives at
  `data/metadata/city_list_with_coords_fixed.csv`. Updated both scripts,
  plus `geocode_cities.py`'s output path and `fix_problem_cities.py`'s
  instructions, to point at `data/metadata/` consistently.
* Removed `backfill_100_cities.py` - an early single-year, 5-column,
  CSV-output prototype that predates the shard/budget architecture and
  had a hardcoded local Windows path in it.
* Removed the empty `Data load code/` placeholder folder and stale
  `__pycache__/` bytecode.
* Fixed a stray, unclosed markdown code fence in `requirements.txt`
  that would have broken `pip install -r requirements.txt`.
* Found a real geocoding bug during a spot-check: Mysore (rank 52) is
  geocoded ~123 km from the actual city - it matched "Mysore Road
  Tolgate," a locality in Bengaluru, because the state-match filter in
  `geocode_cities.py` only checks that the result's state matches
  (Karnataka matches Karnataka), with no distance/plausibility check.
  Every weather record currently labeled "Mysore" is actually
  Bengaluru's weather. **Not yet fixed** - see `roadmap.md`.
* Confirmed (via spot-check against ~24 well-known cities) that
  Belgaum and Mangalore are geocoded 8-13 km from their true centers
  (matched an airport/nearby locality rather than the city center) -
  minor, still within the metro area, not currently treated as bugs.

## Known issues not yet addressed

* `add_new_city.py` was never reconciled with the budget-aware shard
  system in `backfill_by_year.py` - it fetches one city directly with
  no daily-budget tracking. Safe for adding one city at a time; unsafe
  if ever looped over many new cities at once.
* `city_list.py` has module-level `print()` statements that fire on
  every import, including when imported by other scripts.
* `geocode_cities.py`'s state-match filter has no distance/centroid
  check, so other same-state mismatches (beyond Mysore) have not been
  ruled out for the cities outside the ~24-city spot-check.

## Upcoming

* Fix the Mysore coordinate.
* Systematic distance-check of all 100 geocoded coordinates against an
  independent reference, not just a 24-city spot-check.
* Complete EDA, feature engineering, Solar Site Selection Score,
  forecasting, machine learning, dashboards (see `roadmap.md`).
