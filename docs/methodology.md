# Methodology

This document describes the analytical methods used in EcoScope's Solar
module, the first module being built on the shared weather data
foundation. See `roadmap.md` for sequencing and `assumptions.md` for
the caveats that apply to each method below.

## Data validation

Before any analysis runs against `data/raw/weather/`, the data is
checked for: gaps in the hourly time series per city, duplicate
(city, time) rows, and nulls across all columns. As of the last check,
all three came back clean across all 100 cities and all 6 years. See
`notebooks/01_data_audit.ipynb`.

## Exploratory data analysis

Identifies best/worst cities for solar potential, seasonal patterns in
irradiance and cloud cover, and the relationship between cloud cover
and actual generation. This is the current phase of work.

## Solar physics: tilt and azimuth via pvlib

Rather than using Open-Meteo's built-in `tilt`/`azimuth` request
parameters (which would require a separate API call per angle tested),
EcoScope fetches raw radiation components once per city (`dni`, `dhi`,
`ghi` - no tilt) and computes tilted irradiance offline using `pvlib`,
for any tilt/azimuth combination, at zero additional API cost. This
was validated against Open-Meteo's own tilt parameter (mean error
<1.1 W/m², correlation 1.0000) before being adopted as the primary
method, since it enables a full tilt x azimuth grid search rather than
testing one angle at a time.

Note the pvlib azimuth convention differs from Open-Meteo's:
pvlib uses 0=North/180=South, Open-Meteo uses 0=South
(`pvlib_azimuth = openmeteo_azimuth + 180`).

## Solar Site Selection Score

A weighted composite of irradiance, cloud cover, temperature, seasonal
stability, and rainfall, used to rank the 100 cities. The weights need
explicit justification or a sensitivity analysis before being presented
as authoritative - an asserted weighting scheme without either is not
yet defensible. Not yet built.

## Forecasting

Predicts actual Estimated Energy Generation (kWh), not raw GHI.
Pipeline: Weather -> Physics Layer (pvlib) -> Energy Generation ->
Forecast. Not yet built.

## Machine learning

Three planned tasks: regression (Linear/Random Forest/XGBoost) for
generation amount; classification (low/medium/high solar day);
clustering (group cities by solar profile). Not yet built.

## Anomaly detection

Planned to use Isolation Forest. Important methodological constraint:
because the dataset is weather-derived theoretical generation, not
measured panel output, this can only detect weather-PATTERN anomalies
(unusual cloud-cover spikes, soiling-prone wind patterns) - not
equipment-failure anomalies. See `assumptions.md`. Not yet built.

## Evaluation

No models have been trained yet, so no evaluation metrics have been
selected or reported. This section will be filled in once forecasting
and ML work begins (see `roadmap.md`).
