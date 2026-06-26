# Architecture

EcoScope is built on ONE shared historical weather/climate data foundation
(100 Indian cities, hourly, 2021-present), with multiple thin analytical
modules reading from that same data layer. The Solar Potential & Energy
Advisor is the first module being built; the architecture is deliberately
shaped so that adding a new module later means reading existing data, not
re-fetching it.

## Layers

1. **Data Collection** (`src/data_collection/`, `src/geocoding/`) - fetches
   raw weather data from Open-Meteo and resolves city names to coordinates.
2. **Raw Data Store** (`data/raw/weather/`) - year-partitioned Parquet
   files, one row per city-hour.
3. **Data Validation** - integrity checks (no gaps, no duplicate
   timestamps, no nulls) run against the raw store before anything reads
   from it. See `notebooks/01_data_audit.ipynb`.
4. **Preprocessing / Feature Engineering** (`src/preprocessing/`) - not
   yet built. Will derive things like clear-sky ratios and tilted
   irradiance (via `pvlib`) on top of the raw store.
5. **Analytical Modules** (`src/solar/`, future `src/wind/` etc.) - not
   yet built. Each module asks a different question of the same data.
6. **Machine Learning / Forecasting** (`src/machine_learning/`,
   `src/forecasting/`) - not yet built.
7. **Dashboards** (`dashboards/streamlit/`, `dashboards/powerbi/`) - not
   yet built.

## Why this shape

The platform's modules listed in `modules.md` all consume the same
underlying weather variables (temperature, radiation, wind, humidity,
etc.) at the same 100 city locations. Fetching and storing that once,
then letting each module read only the columns it needs, is far cheaper
than having each module run its own data collection. Parquet's
column-selective reads (see `data_dictionary.md` for the full column
list) make this practical even as more modules are added.

## Data flow (current state)

```
city_list.py (100 cities, hardcoded)
        |
geocode_cities.py  -->  data/metadata/city_list_with_coords.csv
        |
fix_problem_cities.py  -->  manual review of flagged rows
        |
   (manually saved as)  data/metadata/city_list_with_coords_fixed.csv
        |
backfill_by_year.py  -->  data/raw/weather/shards/cityNNN_yearYYYY.parquet
        |  (resumable, budget-aware - see assumptions.md)
        |
consolidate_shards.py  -->  data/raw/weather/year_YYYY.parquet
        |
   [ THIS IS WHERE EVERY MODULE READS FROM ]
```

`add_new_city.py` and `retry_failed.py` both append into this same store
once it exists, without re-fetching existing cities. See
`change_log.md` for what's actually been built so far and `roadmap.md`
for what's planned but not yet started.
