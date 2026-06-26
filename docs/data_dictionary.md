# Data Dictionary

## Overview

This document provides a detailed description of every variable contained in the historical weather dataset used by the **EcoScope - Environmental Intelligence Platform**.

The dataset consists of hourly meteorological observations collected for multiple cities and is designed to support environmental analytics, renewable energy assessment, forecasting, machine learning, and geospatial visualization. While the current implementation focuses on selected cities in India, the dataset structure is designed to support future expansion to additional countries and regions.

---

# Dataset Information

| Attribute               | Value                                            |
| ----------------------- | ------------------------------------------------ |
| **Dataset Name**        | Historical Weather Dataset                       |
| **Temporal Resolution** | Hourly                                           |
| **Observation Period**  | Six Years                                        |
| **Storage Format**      | Apache Parquet                                   |
| **Geographic Coverage** | Multiple Cities (Scalable to Multiple Countries) |
| **Primary Domain**      | Environmental Intelligence                       |

---

# Column Dictionary

| Column                         | Data Type | Unit            | Typical Range          | Description                                                                                                                  | Intended Use                                         |
| ------------------------------ | --------- | --------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **time**                       | datetime  | DateTime        | Hourly timestamps      | Date and time of each weather observation.                                                                                   | Time-series analysis, forecasting, seasonal analysis |
| **dni**                        | float     | W/m²            | 0–1200                 | Direct Normal Irradiance representing solar radiation received directly from the sun on a surface perpendicular to sunlight. | Solar energy estimation, PV analysis                 |
| **dhi**                        | float     | W/m²            | 0–600                  | Diffuse Horizontal Irradiance representing scattered solar radiation reaching a horizontal surface.                          | Solar radiation analysis                             |
| **ghi**                        | float     | W/m²            | 0–1400                 | Global Horizontal Irradiance representing total incoming solar radiation on a horizontal surface.                            | Solar potential assessment                           |
| **temperature_2m**             | float     | °C              | -20 to 55              | Air temperature measured at 2 meters above ground level.                                                                     | Weather analysis, panel temperature estimation       |
| **relative_humidity_2m**       | integer   | %               | 0–100                  | Relative humidity at 2 meters above ground.                                                                                  | Climate analysis, comfort indices                    |
| **rain**                       | float     | mm              | 0+                     | Rainfall recorded during the observation period.                                                                             | Rainfall analysis, logistics planning                |
| **precipitation**              | float     | mm              | 0+                     | Total precipitation including rain and snowfall (water equivalent).                                                          | Hydrological and weather analysis                    |
| **wind_speed_10m**             | float     | km/h            | 0–150                  | Average wind speed measured at 10 meters above ground.                                                                       | Weather analysis                                     |
| **wind_direction_10m**         | integer   | Degrees         | 0–360                  | Wind direction measured at 10 meters.                                                                                        | Wind pattern analysis                                |
| **wind_direction_100m**        | integer   | Degrees         | 0–360                  | Wind direction measured at 100 meters above ground.                                                                          | Wind energy assessment                               |
| **wind_gusts_10m**             | float     | km/h            | 0–200                  | Maximum wind gust recorded during the observation period.                                                                    | Extreme weather analysis                             |
| **wind_speed_100m**            | float     | km/h            | 0–200                  | Wind speed measured at 100 meters above ground.                                                                              | Wind energy potential                                |
| **cloud_cover**                | integer   | %               | 0–100                  | Percentage of sky covered by clouds.                                                                                         | Solar generation analysis                            |
| **sunshine_duration**          | float     | Seconds         | 0–3600                 | Duration of bright sunshine during the hour.                                                                                 | Solar resource analysis                              |
| **weather_code**               | integer   | Code            | Standard weather codes | Numerical code describing the observed weather condition.                                                                    | Weather classification                               |
| **snowfall**                   | float     | cm              | 0+                     | Snowfall accumulated during the observation period.                                                                          | Cold climate analysis                                |
| **snow_depth**                 | float     | m               | 0+                     | Snow depth present on the ground.                                                                                            | Snow monitoring                                      |
| **et0_fao_evapotranspiration** | float     | mm              | 0–20                   | Reference evapotranspiration calculated using the FAO-56 Penman–Monteith method.                                             | Agriculture, irrigation planning                     |
| **pressure_msl**               | float     | hPa             | 870–1085               | Atmospheric pressure reduced to mean sea level.                                                                              | Weather system analysis                              |
| **surface_pressure**           | float     | hPa             | 700–1100               | Atmospheric pressure measured at the Earth's surface.                                                                        | Meteorological analysis                              |
| **vapour_pressure_deficit**    | float     | kPa             | 0–10                   | Difference between saturated and actual water vapor pressure, indicating atmospheric drying potential.                       | Agriculture, plant stress analysis                   |
| **apparent_temperature**       | float     | °C              | -30 to 60              | Human-perceived temperature considering humidity and wind.                                                                   | Comfort analysis                                     |
| **dew_point_2m**               | float     | °C              | -30 to 35              | Temperature at which air becomes saturated and condensation begins.                                                          | Moisture and humidity analysis                       |
| **city**                       | string    | —               | Text                   | Name of the observation city.                                                                                                | Geographic grouping                                  |
| **state**                      | string    | —               | Text                   | State or administrative region corresponding to the city.                                                                    | Regional analysis                                    |
| **rank**                       | integer   | —               | Positive Integer       | Population-based ranking assigned to the city.                                                                               | City comparison                                      |
| **tier**                       | integer   | —               | 1–3                    | User-defined city classification based on population ranking.                                                                | Comparative analysis                                 |
| **latitude**                   | float     | Decimal Degrees | -90 to 90              | Latitude coordinate of the observation location.                                                                             | Mapping and geospatial analysis                      |
| **longitude**                  | float     | Decimal Degrees | -180 to 180            | Longitude coordinate of the observation location.                                                                            | Mapping and geospatial analysis                      |

---

# Variable Categories

The dataset is organized into the following logical groups:

| Category                     | Variables                                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| **Temporal**                 | time                                                                                     |
| **Solar Radiation**          | dni, dhi, ghi                                                                            |
| **Temperature & Humidity**   | temperature_2m, apparent_temperature, dew_point_2m, relative_humidity_2m                 |
| **Precipitation**            | rain, precipitation, snowfall, snow_depth                                                |
| **Wind**                     | wind_speed_10m, wind_speed_100m, wind_direction_10m, wind_direction_100m, wind_gusts_10m |
| **Atmospheric Conditions**   | pressure_msl, surface_pressure, vapour_pressure_deficit, cloud_cover                     |
| **Environmental Indicators** | sunshine_duration, weather_code, et0_fao_evapotranspiration                              |
| **Geographic Information**   | city, state, rank, tier, latitude, longitude                                             |

---

# Applications

The variables documented in this dataset support multiple environmental intelligence applications, including:

* Solar Energy Potential Assessment
* Renewable Energy Forecasting
* Weather Analytics
* Environmental Monitoring
* Agriculture and Irrigation Planning
* Wind Energy Assessment
* Geospatial Analysis
* Time-Series Forecasting
* Machine Learning
* Interactive Dashboards
* Climate and Sustainability Research
