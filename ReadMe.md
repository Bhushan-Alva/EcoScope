# EcoScope

## Overview

EcoScope is a modular Environmental Intelligence Platform that
transforms historical weather and climate observations into actionable
insights through data analytics, forecasting, machine learning, and
interactive dashboards.

The platform is built around one shared weather/climate dataset (100
Indian cities, hourly, 2021-present) that supports multiple
decision-support modules rather than a single application. Although
development currently focuses on selected cities in India, the data
schema is designed to support additional countries and regions later
(see `docs/data_dictionary.md` for columns kept specifically for that,
e.g. snow variables that are ~0 for India today).

The first module being built is Solar Energy Potential Assessment.
Eight further modules are scoped but not started - see `docs/modules.md`.

## Current Status

* ✅ 100-city list defined, geocoded, and verified
* ✅ Historical weather dataset collected (2021-01-01 to 2026-06-24, all
  100 cities, zero gaps/duplicates/nulls)
* ✅ Data audit notebook run (`01_data_audit.ipynb`)
* 🚧 One open data-quality bug: Mysore is geocoded ~123 km from the
  actual city (matched a Bengaluru locality) - not yet fixed, see
  `docs/change_log.md`
* ⏳ Exploratory data analysis (notebooks 02-07)
* ⏳ Solar Site Selection Score
* ⏳ Forecasting
* ⏳ Machine learning (regression, classification, clustering, anomaly
  detection)
* ⏳ Streamlit dashboard (6 pages planned)
* ⏳ Power BI dashboard

See `docs/roadmap.md` for the full phase-by-phase breakdown, including
individual notebooks, dashboard pages, and pvlib modules still to be
used.

## Planned Modules

* Solar Energy Potential *(in progress)*
* Wind Energy Assessment
* Crop & Irrigation Advisor
* Construction & Outdoor Work Scheduler
* Cold Chain & Logistics Risk
* Tourism Insights
* Disaster Early Warning
* Urban Heat Island Analysis
* Weather-Driven Retail Demand

## Technologies

Python • Pandas • NumPy • PyArrow • Plotly • Scikit-learn • XGBoost •
PVLib • Streamlit • Power BI

## Documentation Files

| File | Description |
| --- | --- |
| **ReadMe.md** | Overview of the project, current status, technologies, and planned modules. Main entry point for the repository. |
| **docs/architecture.md** | How the platform is organized: layers, data flow from raw collection through to each module. |
| **docs/data_dictionary.md** | Every dataset column: data type, unit, range, description, and which module it's intended for. |
| **docs/data_sources.md** | The weather, geocoding, and population-ranking sources used, and why each storage/partitioning choice was made. |
| **docs/methodology.md** | The analytical methods used so far (and planned), with their current build status. |
| **docs/modules.md** | Every planned module, its purpose, the variables it needs, and its actual build status. |
| **docs/roadmap.md** | Full phase-by-phase plan, broken down to individual notebooks, dashboard pages, and library modules - not just phase names. |
| **docs/folder_structure.md** | What each directory holds, and which ones are populated vs. still empty scaffolding. |
| **docs/assumptions.md** | Assumptions, caveats, and known limitations - what the data and analysis can and can't honestly claim. |
| **docs/change_log.md** | Chronological record of what's been built, what bugs were found, and what's still open. |

## Project Modules

| Module | Status | Description |
| --- | --- | --- |
| **Solar Energy Potential** | In progress | Evaluates historical solar resources, estimates theoretical energy generation, compares cities, supports solar site selection. |
| **Wind Energy Assessment** | Not started | Structural twin of Solar - same pattern, different physics. Wind speed/direction at hub height already collected. |
| **Crop & Irrigation Advisor** | Not started | Crop growth, evapotranspiration, rainfall, and irrigation planning. |
| **Construction & Outdoor Work Scheduler** | Not started | Favorable weather windows for outdoor work, using rainfall, temperature, wind, heat-stress signals. |
| **Cold Chain & Logistics Risk** | Not started | Environmental risk to temperature-sensitive transportation. |
| **Tourism & Weather Insights** | Not started | Seasonal weather patterns and favorable travel periods. |
| **Disaster Early Warning** | Not started | Unusual weather patterns that may signal increased risk of extreme events. Reuses Solar's anomaly detection approach. |
| **Urban Heat Island Analysis** | Not started | Temperature variation across urban areas - needs additional geographic data beyond point coordinates. |
| **Weather-Driven Retail Demand** | Not started | Relationships between weather and consumer demand. |

## Project Notebooks

| Notebook | Status | Description |
| --- | --- | --- |
| **01_data_audit.ipynb** | ✅ Done | Validates completeness, consistency, and integrity of the historical weather dataset before analysis. |
| **02_univariate_analysis.ipynb** | ⏳ Not started | Statistical distribution of each weather variable independently. |
| **03_time_series_analysis.ipynb** | ⏳ Not started | Temporal trends, seasonal cycles, monthly patterns, long-term changes. |
| **04_city_comparison.ipynb** | ⏳ Not started | Compares weather characteristics and solar resources across cities. |
| **05_correlation_analysis.ipynb** | ⏳ Not started | Relationships between weather variables and solar energy potential. |
| **06_geospatial_analysis.ipynb** | ⏳ Not started | Geographic variation via interactive maps and spatial comparisons. |
| **07_feature_engineering.ipynb** | ⏳ Not started | Derived variables and features for forecasting/ML. |
| **08_solar_score.ipynb** | ⏳ Not started | Composite solar suitability score for comparing locations. |
| **09_forecasting.ipynb** | ⏳ Not started | Time-series forecasting models for future solar energy generation. |
| **10_machine_learning.ipynb** | ⏳ Not started | Regression, classification, clustering, and anomaly detection models. |

## Known Open Issues

See `docs/change_log.md` for the full history. The two currently open:

* Mysore's geocoded coordinate is ~123 km from the actual city.
* `add_new_city.py` is not yet reconciled with the budget-aware shard
  system used by the main backfill script.
