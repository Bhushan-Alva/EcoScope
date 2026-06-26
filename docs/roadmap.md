# Project Roadmap

Status key: `[x]` done, `[~]` in progress, `[ ]` not started.

## Phase 1 - Weather Data Collection & Validation - MOSTLY COMPLETE

* [x] 100-city list defined and geocoded
* [x] Backfill complete: 2021-01-01 through 2026-06-24, all 100 cities,
      zero gaps, zero duplicate timestamps, zero nulls
* [x] Consolidated into year-partitioned Parquet (`data/raw/weather/`)
* [x] `01_data_audit.ipynb` - validates completeness, consistency, and
      integrity of the dataset before analysis (run, output verified)
* [ ] Fix the Mysore geocoding error (~123 km off - matched a Bengaluru
      locality instead of the actual city; see `change_log.md`)
* [ ] Systematic distance-check of all 100 coordinates against an
      independent reference (only ~24 were spot-checked so far)
* [ ] Reconcile `add_new_city.py` with the budget-aware shard system
      used by `backfill_by_year.py`

## Phase 2 - Exploratory Data Analysis & Feature Engineering - NOT STARTED

Notebooks planned (numbering continues from `01_data_audit.ipynb`):

* [ ] `02_univariate_analysis.ipynb` - statistical distribution of each
      weather variable independently (range, skew, outliers)
* [ ] `03_time_series_analysis.ipynb` - temporal trends, seasonal
      cycles, monthly patterns, year-over-year changes
* [ ] `04_city_comparison.ipynb` - weather characteristics and solar
      resources compared across all 100 cities via aggregated stats
      and rankings
* [ ] `05_correlation_analysis.ipynb` - relationships between weather
      variables; which factors most influence solar potential
* [ ] `06_geospatial_analysis.ipynb` - geographic variation in
      environmental variables via interactive maps and spatial
      comparisons
* [ ] `07_feature_engineering.ipynb` - derived variables for
      forecasting/ML: clear-sky ratio (needs pvlib's `clearsky`
      module - see Phase 3), tilted irradiance at the chosen
      tilt/azimuth, panel temperature (pvlib's `temperature` module,
      from air temp + irradiance + wind rather than air temp alone)

EDA deliverables this phase should produce:

* [ ] Best/worst cities for solar potential (ranked table)
* [ ] Seasonal pattern charts: irradiance and cloud cover by month,
      per tier and per city
* [ ] Cloud-cover-to-generation relationship (scatter/regression)

## Phase 3 - Solar Energy Assessment - NOT STARTED

* [ ] `08_solar_score.ipynb` - composite solar suitability score
* [ ] Solar Site Selection Score: weighted composite of irradiance,
      cloud cover, temperature, seasonal stability, and rainfall -
      **with explicit weight justification or a sensitivity analysis**,
      not asserted weights (see `methodology.md`)
* [ ] Full tilt x azimuth grid search per city (already validated as a
      method - see `methodology.md` - not yet run as the basis for a
      published per-city recommendation)
* [ ] Explicitly handle the flat-tilt/azimuth-meaningless edge case in
      any reported "best azimuth" output (see `assumptions.md`)
* [ ] ROI calculation - initial version can use DNI/DHI/GHI directly;
      a more rigorous version would bring in pvlib's `pvsystem`/
      `inverter` modules for full DC->AC system modeling (currently
      unused, listed here as a known upgrade path)
* [ ] Soiling-loss estimate via pvlib's `soiling` module (dust
      accumulation loss from wind patterns) - feeds both the ROI
      number and the Phase 5 anomaly detection feature
* [ ] Snow-loss estimate via pvlib's `snow` module - low priority for
      India now (snow columns are ~0), relevant once non-India cities
      are added
* [ ] Geographic visualization (plotly `scatter_mapbox`): solar
      potential, ROI, and tilt angle plotted across all 100 cities

## Phase 4 - Forecasting - NOT STARTED

* [ ] `09_forecasting.ipynb`
* [ ] Pipeline: Weather -> Physics Layer (pvlib) -> Energy Generation
      -> Forecast - predicting actual estimated kWh, not raw GHI
* [ ] Model selection and backtesting against the 2021-2025 history,
      validating on 2026 partial-year data

## Phase 5 - Machine Learning - NOT STARTED

* [ ] `10_machine_learning.ipynb`
* [ ] Regression (Linear / Random Forest / XGBoost) - predict
      generation amount
* [ ] Classification - low/medium/high solar day
* [ ] Clustering - group the 100 cities by solar profile
* [ ] Anomaly detection (Isolation Forest) - flags weather-PATTERN
      anomalies only (cloud-cover spikes, soiling-prone wind patterns),
      **not** equipment-failure anomalies; this distinction must be
      stated wherever results are shown (see `assumptions.md`)

## Phase 6 - Interactive Dashboards - NOT STARTED

### Streamlit (`dashboards/streamlit/`)

* [ ] **Executive Overview** - top-line summary: best cities, headline
      stats, project status at a glance
* [ ] **Solar Potential Explorer** - per-city irradiance/cloud-cover
      browsing, seasonal charts
* [ ] **Forecasting** - generation forecast view, depends on Phase 4
* [ ] **ROI Calculator** - interactive input (system size, location,
      tilt) -> estimated payback, depends on Phase 3 ROI work
* [ ] **City Benchmark** - side-by-side comparison across cities/tiers
* [ ] **ML Insights** - classification/clustering/anomaly results,
      depends on Phase 5, must carry the anomaly-detection caveat in
      the UI itself, not just in docs

### Power BI (`dashboards/powerbi/`)

* [ ] Separate track from Streamlit, built against the same underlying
      data
* [ ] Reads from periodically-refreshed Parquet/CSV snapshots in
      `data/exports/` - **not** a live API connection, since Power BI
      Desktop without a gateway only refreshes on manual click
* [ ] Refresh workflow: re-run fetch/export script -> click refresh in
      Power BI (manual, no automation planned for this step)

## Phase 7 - Additional Environmental Modules - NOT STARTED

Each reuses the Phase 1 data foundation; see `modules.md` for the
specific variables each one needs.

* [ ] Wind Energy Potential - structural twin of Solar (same pattern,
      different physics), already has `wind_speed_100m` and
      `wind_direction_100m` collected for this
* [ ] Crop & Irrigation Advisor
* [ ] Construction & Outdoor Work Scheduler
* [ ] Cold Chain / Perishable Logistics Risk
* [ ] Tourism Demand & Pricing Insight
* [ ] Disaster Early-Warning Dashboard - reuses the Phase 5 anomaly
      detection approach, same caveat applies
* [ ] Urban Heat Island Mapper - needs additional geographic data
      (e.g. OSM building density) beyond this dataset's point
      coordinates - see `assumptions.md`
* [ ] Retail Footfall / Demand Sensitivity
