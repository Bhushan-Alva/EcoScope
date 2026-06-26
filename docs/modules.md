# Platform Modules

All modules share one weather/climate data foundation (100 Indian
cities, hourly, 2021-present) - see `architecture.md`. Each module below
is listed with its actual build status, not just its intended purpose.

## Solar Energy Potential - IN PROGRESS (current focus)

Estimate and compare solar energy generation across locations: best/worst
cities, optimal tilt/azimuth (genuinely season-dependent, not one fixed
number - see `assumptions.md`), ROI, and a Solar Site Selection Score.
Data collection is complete; EDA has started; everything past that
(scoring, forecasting, ML, dashboards) is not yet built. See
`roadmap.md`.

## Wind Energy Assessment - NOT STARTED

Structural twin of the Solar module - same pattern (physics layer over
shared weather data), different physics. Uses `wind_speed_100m` and
`wind_direction_100m` (turbine hub height), already collected in the
shared dataset specifically for this future use.

## Crop & Irrigation Advisor - NOT STARTED

Analyze weather conditions affecting crop growth and irrigation
requirements. Primary variable: `et0_fao_evapotranspiration`
(FAO-56 Penman-Monteith reference evapotranspiration), already
collected. Also uses temperature, humidity, rain, and
`vapour_pressure_deficit` (plant stress signal).

## Construction & Outdoor Work Scheduler - NOT STARTED

Assess weather suitability for outdoor construction activities, using
temperature, humidity, wind, cloud cover, and `apparent_temperature`
combined with `vapour_pressure_deficit` as a heat-stress signal for
outdoor workers.

## Cold Chain / Perishable Logistics Risk - NOT STARTED

Identify environmental risks affecting temperature-sensitive
transportation, primarily via `temperature_2m` and
`apparent_temperature`.

## Tourism Demand & Pricing Insight - NOT STARTED

Analyze weather patterns influencing seasonal tourism demand, using
temperature, cloud cover, sunshine duration, and weather codes.

## Disaster Early-Warning Dashboard - NOT STARTED

Monitor extreme weather signals: `precipitation` (broader hazard signal
including snow), wind gusts, and pressure (`pressure_msl`,
`surface_pressure` - a pressure drop is a storm signal). Reuses the
anomaly-detection approach being built for Solar, with the same
weather-pattern-vs-measured-event caveat applying here too.

## Urban Heat Island Mapper - NOT STARTED

Evaluate temperature variation across urban environments. Note: this is
constrained by the same point-coordinate limitation described in
`assumptions.md` - each city is one lat/lon point, not an area, so
within-city heat island mapping would need additional geographic data
(e.g. OSM building density) beyond what this dataset alone provides.

## Retail Footfall / Demand Sensitivity - NOT STARTED

Assess how weather influences consumer demand patterns, using
temperature, rain, cloud cover, and weather codes for dashboard-level
labeling.
