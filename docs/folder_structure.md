# Folder Structure

```
EcoScope/
├── data/
│   ├── raw/weather/         Year-partitioned Parquet files
│   │                        (year_2021.parquet ... year_2026.parquet) -
│   │                        the canonical store every module reads from.
│   │                        Also holds shards/ (per-city-year temp files
│   │                        from backfill_by_year.py, safe to delete once
│   │                        consolidated) and failed_this_run.csv if any
│   │                        city-years failed during the last backfill run.
│   ├── metadata/            city_list_with_coords_fixed.csv - the master
│   │                        100-city list with verified coordinates.
│   ├── processed/           Reserved for feature-engineered / cleaned
│   │                        data once preprocessing exists. Empty for now.
│   └── exports/             Reserved for periodically-refreshed
│                            Parquet/CSV snapshots that the Power BI
│                            dashboard will read from (Power BI Desktop
│                            without a gateway only refreshes manually,
│                            so this needs to be a static export, not a
│                            live API connection). Empty for now.
│
├── src/
│   ├── data_collection/     fetch_core.py (shared fetch logic),
│   │                        backfill_by_year.py (resumable, budget-aware
│   │                        initial backfill), consolidate_shards.py,
│   │                        add_new_city.py, retry_failed.py.
│   ├── geocoding/           city_list.py (the 100-city list, hardcoded),
│   │                        geocode_cities.py, fix_problem_cities.py.
│   ├── preprocessing/       Empty - not yet built.
│   ├── solar/               Empty - not yet built. Will hold the Solar
│   │                        Site Selection Score, pvlib physics layer,
│   │                        ROI calculations.
│   ├── machine_learning/    Empty - not yet built.
│   ├── forecasting/         Empty - not yet built.
│   └── utils/               Empty - not yet built.
│
├── notebooks/
│   └── 01_data_audit.ipynb  Phase 1 EDA / data quality checks against
│                            the consolidated year-files.
│
├── dashboards/
│   ├── streamlit/           Empty - not yet built. Planned pages:
│                            Executive Overview, Solar Potential Explorer,
│                            Forecasting, ROI Calculator, City Benchmark,
│                            ML Insights.
│   └── powerbi/             Empty - not yet built. Reads from
│                            data/exports/, not a live connection.
│
├── reports/
│   ├── figures/             Generated charts/plots. Empty for now.
│   └── tables/              Generated summary tables. Empty for now.
│
├── docs/                    This documentation (architecture, assumptions,
│                            data dictionary, methodology, modules, roadmap,
│                            change log, data sources).
│
├── requirements.txt
└── ReadMe.md
```

## Notes on what's actually populated vs. scaffolded

As of this writing, only `data/raw/weather/`, `data/metadata/`,
`src/data_collection/`, `src/geocoding/`, and `notebooks/` have real
content. Everything else listed above (`data/processed/`,
`data/exports/`, `src/preprocessing/`, `src/solar/`,
`src/machine_learning/`, `src/forecasting/`, `src/utils/`,
`dashboards/streamlit/`, `dashboards/powerbi/`, `reports/`) is
scaffolded folder structure with no files in it yet - see `roadmap.md`
for the order these are planned to be filled in.
