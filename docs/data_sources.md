# Data Sources

## Weather data: Open-Meteo Historical Weather API

`archive-api.open-meteo.com/v1/archive` - ERA5/ERA5-Land reanalysis data.
Chosen over Open-Meteo's Historical Forecast API, which exists for a
different use case (matching live-forecast bias-correction). The
Archive API is gap-free and consistent, which matters for seasonal
pattern analysis. No API key required; free tier with a 10,000
effective-calls/day limit (see `change_log.md` for how the real cost of
a request is calculated, and why that limit is easy to misjudge).

22 hourly variables are pulled per request - see `data_dictionary.md`
for the full column list and which planned module each one feeds.

## Geocoding: Open-Meteo Geocoding API

`geocoding-api.open-meteo.com/v1/search` - free, no API key. Used once
per city to resolve a name to a lat/lon point, filtered to India and
disambiguated by state where multiple matches exist. See
`assumptions.md` for the limitations of this approach (point coordinates,
not areas; possible same-state mismatches).

## City population ranking

Wikipedia's "List of cities in India by population," based on the 2011
Census - the most authoritative consistent baseline available across
all 100 cities (more recent "2025/2026 estimate" sources generally
derive from this same baseline rather than an independent census, since
India's next census has not yet been conducted as of this writing).

## Storage format

Apache Parquet, partitioned by year (`data/raw/weather/year_YYYY.parquet`).
Chosen over CSV after a direct benchmark: at ~4.4M rows x 18 columns,
CSV took 115s to write and produced a 1565MB file; Parquet took 2.4s and
produced a 658MB file (2.4x smaller, ~10x faster reads), while also
preserving dtypes (CSV silently stringifies everything) and supporting
column-selective reads.

Year-partitioning (rather than city-partitioning) was chosen because
new cities are added more often than new years close out: adding one
city touches all existing year-files (benchmarked at ~19 seconds for 1
city across 5 year-files), while adding a year under a city-partitioned
scheme would touch all 100 city-files instead.
