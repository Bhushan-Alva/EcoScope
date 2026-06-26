# Assumptions

This document lists the assumptions and known limitations baked into
EcoScope's data and analysis, so that anyone reading the outputs
(including future-me) doesn't overclaim what the numbers actually mean.

## Solar generation is theoretical, not measured

Every "solar generation" or "energy potential" number in this project is
derived from weather variables (`dni`, `dhi`, `ghi`, temperature, wind)
run through physics models (`pvlib`), not from a real installed panel
reporting actual output. This matters most for the planned anomaly
detection feature: with this data, anomaly detection can only flag
**weather-pattern anomalies** (unusual cloud-cover spikes, soiling-prone
wind patterns) - it cannot detect equipment failure, panel degradation,
or inverter faults, because there is no measured panel output to compare
against. Any writeup of anomaly detection results must state this
distinction explicitly.

## Optimal tilt is not a single number - it depends on season

Early analysis (Delhi, full year) found that the optimal panel tilt
varies dramatically with season: ~50 deg in winter (Nov-Jan, sun low in
the sky) down to ~0 deg / flat in summer (May-Jul, sun nearly overhead
at this latitude), with a smooth transition between. A single
"annual-compromise" angle (around 25 deg, south-facing) exists and is
useful as a simple answer, but it is a compromise, not the genuinely
optimal setup for any individual month. Any feature or dashboard page
that reports "the best tilt" should make clear whether it means the
annual compromise or a season-aware recommendation.

**Caveat on azimuth:** when the optimal tilt for a given period is 0
deg (flat), azimuth is mathematically meaningless - a flat panel has no
facing direction. Any "best azimuth" value reported for a flat-tilt
period is an arbitrary tie-break in the grid search, not a real result,
and should not be presented as one.

## City coordinates are points, not areas

Each of the 100 cities is represented by a single lat/lon point from
Open-Meteo's geocoding API, not a city boundary or area average. Two
consequences:

- The point is usually close to the city center, but geocoding can
  silently match the wrong place if a locality elsewhere in the same
  state shares part of the city's name (this happened with Mysore,
  which matched a Bengaluru locality ~123 km away - see `change_log.md`).
  A same-state mismatch will not be caught by the state-filter check in
  `geocode_cities.py`, since the filter only checks state, not distance.
- Large or sprawling cities (e.g. Delhi/NCR) get one representative
  point, not multiple sub-area readings. City-level comparison is the
  intended grain of analysis here, not neighborhood-level precision.

## Tier labels are our own convention, not an official standard

Tier 1 (rank 1-46) matches India's official "Million Plus Cities"
definition exactly, so it's defensible. Tier 2 (47-75) and Tier 3
(76-100) are our own rank-based splits - there is no single official
"popularity tier" system in India that distinguishes cities at this
scale (RBI's official tiers use population thresholds like 100k+ that
don't usefully separate big cities from each other).

## Historical depth (2021-present) is a deliberate choice, not a limitation we'd fix given more time

Solar irradiance and cloud cover don't have strong multi-decade trends
the way temperature does, so going back further than ~5 years adds
storage/processing cost without adding much analytical signal. Satellite
observation density was also sparser before 2021, which would mix data
quality eras together in any trend analysis. Five years still covers 5
monsoons and 5 summers, which is enough variety for the planned ML
work.

## Missing values

As of the last full data-integrity check (see `change_log.md`), the
collected dataset has zero nulls across all columns, zero duplicate
timestamps, and zero timestamp gaps for any of the 100 cities. This
assumption ("missing values are handled during preprocessing") is
currently moot for the raw weather store - there's nothing missing to
handle. It will likely become relevant once a new city is added via
`add_new_city.py`, since that script fetches independently of the main
backfill and hasn't yet been load-tested at scale.
