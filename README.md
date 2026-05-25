<p align="center">
  <img src="logo.png" alt="FutureCast-Bench logo" width="520" />
</p>

# FutureCast-Bench

**FutureCast-Bench** is a context-aware forecasting benchmark from the **FutureCast（天星台）** project. It is designed to evaluate whether forecasting models can move beyond numerical extrapolation and reason with real-world context.

**Chinese name:** 天星台  
**Tagline:** *A Context-Aware Forecasting Benchmark*

Instead of representing each forecasting task only as:

```text
historical time series -> future values
```

FutureCast-Bench represents each task as:

```text
historical time series + numeric exogenous variables + textual exogenous context + evidence annotations -> forecasting target
```

The goal is to support the next generation of time series foundation models, LLM-driven forecasting models, slow-thinking forecasting systems, and agentic forecasting workflows.

## Naming

| Usage | Name |
|---|---|
| Project family | **FutureCast（天星台）** |
| Benchmark | **FutureCast-Bench** |
| Data corpus | **FutureCast-Corpus** |
| Task collection | **FutureCast-Tasks** |
| Full title | **FutureCast-Bench: A Context-Aware Forecasting Benchmark** |

## Why FutureCast-Bench?

Most existing time series benchmarks are built around the numerical series itself. They evaluate whether a model can forecast future values from past values across different domains, frequencies, and horizons. This is necessary, but it is not enough for real-world forecasting.

In real applications, the future is often shaped by information outside the target sequence:

- electricity demand and prices are affected by weather, holidays, supply-demand balance, market rules, and grid conditions;
- traffic flow is affected by accidents, weather, events, commuting patterns, and spatial structure;
- retail demand is affected by promotion, price, holidays, inventory, store location, and consumer behavior;
- clinical variables are affected by patient status, treatment intervention, missingness, and medical knowledge;
- macroeconomic indicators are affected by policy changes, inflation, interest rates, employment, and market expectations;
- climate and hydrology variables are affected by seasonal cycles, geography, precipitation, snowpack, and local physical conditions;
- air quality is affected by regional transport, meteorology, co-pollutants, station location, and seasonal environmental conditions;
- cloud machine utilization is affected by workload scheduling, resource contention, business cycles, and cluster-level operations;
- industrial sensor signals are affected by operating conditions, maintenance, environment, and abnormal events.

Two time series can have similar historical shapes but very different futures because their surrounding contexts are different. A benchmark that only measures numerical error cannot tell whether a model is merely fitting statistical patterns or actually understanding why the future changes.

FutureCast-Bench is designed to fill this gap. It evaluates not only whether a model predicts accurately, but also whether it can:

- identify which contextual information is relevant;
- align context with the correct time interval and forecasting target;
- reason about how external factors affect future values;
- revise predictions when new evidence appears;
- generate evidence-grounded explanations for forecasting decisions.

## Core Capabilities

FutureCast-Bench is organized around three core capabilities.

### 1. Context-Sequence Alignment and Fusion

Models should be able to align target time series with heterogeneous context, including calendar information, spatial attributes, weather, events, business rules, domain knowledge, and textual descriptions.

### 2. Contextual Reasoning for Forecasting

Models should not only output future values, but also reason about the potential impact of contextual factors. For example, high temperature may increase electricity load, promotion may increase retail demand, and policy change may shift macroeconomic trends.

### 3. Dynamic Context Adaptation

Real forecasting is often an iterative process. A model may first make a prediction with incomplete information, then receive new evidence, update its reasoning, and revise the forecast. FutureCast-Bench includes tasks for evaluating this dynamic adaptation ability.

## Current Benchmark Status

The current processed benchmark covers **15 datasets** across **10 domains**, with approximately **149K forecasting series** and **277M timestamp-level records**. Each dataset is stored in a lightweight CSV layout with one target file, one numeric exogenous file, one text exogenous file, and one task YAML definition for each benchmark task.

| Domain | Dataset | Forecasting Target | Forecasting Unit | Frequency | Dataset Size | Variables | Lookback / Prediction Windows |
|---|---|---|---|---|---|---|---|
| Energy | SDWPF | Wind turbine active power | Wind turbine | 10 min | 134 turbine series; about 11.36M timestamp records | 1 target; 24 numeric exogenous variables; text exogenous context | Lookback: 24 hours / 7 days / 30 days; Prediction: 8 hours / 24 hours / 7 days |
| Power | AEMO NEM DispatchIS | Regional electricity price (`RRP`) | NEM region | 5 min | 5 region series; about 129.6K timestamp records | 1 target; 11 numeric exogenous variables; text exogenous context | Lookback: 24 hours / 7 days / 28 days; Prediction: 1 hour / 24 hours / 7 days |
| Power | OPSD German Load | German actual electricity load | Country-level load series | 1 hour | 1 load series; about 50.4K hourly records | 1 target; 3 numeric exogenous variables; text exogenous context | Lookback: 7 / 30 / 90 days; Prediction: 24 hours / 7 days / 30 days |
| Sales | M5 | Daily unit sales | Item-store pair | 1 day | 30,490 item-store series; about 59.18M daily records | 1 target; 7 numeric exogenous variables; text exogenous context | Lookback: 56 / 168 / 365 days; Prediction: 28 / 84 / 168 days |
| Sales | Rossmann Store Sales | Store sales | Store | 1 day | 1,115 store series; about 1.06M daily records | 1 target; 13 numeric exogenous variables; text exogenous context | Lookback: 56 / 168 / 365 days; Prediction: 28 / 84 / 168 days |
| Sales | Favorita Grocery Sales | Unit sales | Store-item pair from one selected store | 1 day | 4,081 store-item series; about 2.62M daily records | 1 target; 21 numeric exogenous variables; text exogenous context | Lookback: 56 / 168 / 365 days; Prediction: 28 / 84 / 168 days |
| Medical | PhysioNet 2012 | ICU clinical variable value | ICU stay-variable pair | 1 hour | 107,188 patient-variable series; about 5.25M hourly records | 1 target; 19 numeric exogenous variables; text exogenous context | Lookback: 6 / 12 / 24 hours; Prediction: 6 / 12 / 24 hours |
| Traffic | PEMS04 | Traffic flow | Road sensor | 5 min | 307 sensor series; about 5.22M timestamp records | 1 target; 15 numeric exogenous variables; text exogenous context | Lookback: 24 hours / 7 days / 28 days; Prediction: 1 hour / 24 hours / 7 days |
| Traffic | PEMS07 | Traffic flow | Road sensor | 5 min | 883 sensor series; about 24.92M timestamp records | 1 target; 13 numeric exogenous variables; text exogenous context | Lookback: 24 hours / 7 days / 28 days; Prediction: 1 hour / 24 hours / 7 days |
| Traffic | NYC TLC | Hourly pickup trip count | Taxi type-pickup zone pair | 1 hour | 513 taxi-zone series; about 3.36M hourly records | 1 target; 19 numeric exogenous variables; text exogenous context | Lookback: 7 / 28 / 90 days; Prediction: 24 hours / 7 days / 14 days |
| Economics | FRED-MD | Transformed macroeconomic value | Macroeconomic variable | 1 month | 126 macroeconomic series; about 100.9K monthly records | 1 target; 8 numeric exogenous variables; text exogenous context | Lookback: 36 / 60 / 120 months; Prediction: 1 / 12 / 24 months |
| Climate | Jena Climate | Air temperature | Weather station | 10 min | 1 temperature series; about 420.2K timestamp records | 1 target; 5 numeric exogenous variables; text exogenous context | Lookback: 24 hours / 7 days / 30 days; Prediction: 6 hours / 24 hours / 7 days |
| Hydrology | Basin Streamflow | Daily streamflow | River basin | 1 day | 27 basin series; about 345K daily records | 1 target; 16 numeric exogenous variables; text exogenous context | Lookback: 1 / 3 / 10 years; Prediction: 7 days / 30 days / 1 year |
| AIOps | Alibaba Cluster | CPU utilization | Machine | 1 hour | 100 machine series; about 19K hourly records | 1 target; 6 numeric exogenous variables; text exogenous context | Lookback: 24 hours / 7 days / 30 days; Prediction: 6 hours / 24 hours / 7 days |
| Air Quality | AQ Data | PM2.5 concentration | Monitoring station | 1 hour | 3,720 station series; about 163.03M hourly records | 1 target; 14 numeric exogenous variables; text exogenous context | Lookback: 24 hours / 7 days / 30 days; Prediction: 24 hours / 3 days / 7 days |

## Dataset Cards

Each dataset card summarizes the forecasting task, forecasting unit, contextual variables, business meaning, recommended windows, and current release notes. The cards are intended to make the benchmark understandable before users inspect the raw files or task YAML definitions.

### SDWPF

- **Domain:** energy and wind power forecasting.
- **Task:** forecast wind turbine active power from historical SCADA signals, weather-related variables, turbine position, and timestamp context.
- **Forecasting unit:** one wind turbine per series; 134 turbine series at 10-minute frequency.
- **Context variables:** wind speed, wind direction, temperature, pressure, humidity, turbine operating signals, turbine coordinates, elevation, and calendar fields.
- **Windows:** 24 hours to 8 hours, 7 days to 24 hours, and 30 days to 7 days.
- **Current note:** useful for evaluating context-aware renewable power forecasting under turbine-level heterogeneity.

### AEMO NEM DispatchIS

- **Domain:** electricity price forecasting.
- **Task:** forecast regional reference price (`RRP`) for Australian NEM regions.
- **Forecasting unit:** one electricity market region per series; 5 region series at 5-minute frequency.
- **Context variables:** total demand, available generation, net interchange, settlement interval, and calendar fields.
- **Windows:** 24 hours to 1 hour, 7 days to 24 hours, and 28 days to 7 days.
- **Current note:** demand, generation, and interchange variables are treated as historical market context aligned with each region.

### OPSD German Load

- **Domain:** electricity load forecasting.
- **Task:** forecast German actual electricity load with renewable generation and day-ahead price context.
- **Forecasting unit:** one country-level load series at hourly frequency.
- **Context variables:** wind generation, solar generation, and day-ahead electricity price.
- **Windows:** 7 days to 24 hours, 30 days to 7 days, and 90 days to 30 days.
- **Current note:** useful as a compact power-system benchmark linking load, renewable output, and market price.

### M5

- **Domain:** retail sales forecasting.
- **Task:** forecast daily unit sales for item-store pairs.
- **Forecasting unit:** one item-store pair per series; 30,490 daily sales series.
- **Context variables:** selling price, calendar fields, SNAP indicator, and event-day indicator with text context for product-store-time semantics.
- **Windows:** 8 weeks to 28 days, 24 weeks to 12 weeks, and 1 year to 24 weeks.
- **Current note:** large-scale daily retail benchmark for evaluating promotion, price, calendar, and item-store context.

### Rossmann Store Sales

- **Domain:** retail store sales forecasting.
- **Task:** forecast daily store sales for Rossmann stores.
- **Forecasting unit:** one store per series; 1,115 daily store series.
- **Context variables:** customers, promotion, opening status, school holiday, state holiday, competition distance, and store promotion metadata.
- **Windows:** 8 weeks to 28 days, 24 weeks to 12 weeks, and 1 year to 24 weeks.
- **Current note:** useful for store-level demand forecasting with strong calendar, promotion, and competition effects.

### Favorita Grocery Sales

- **Domain:** grocery sales forecasting.
- **Task:** forecast daily unit sales for store-item pairs from one selected store subset.
- **Forecasting unit:** one store-item pair per series; 4,081 daily series.
- **Context variables:** promotion, transactions, oil price, calendar fields, store cluster, item class, item perishability, and holiday indicators.
- **Windows:** 8 weeks to 28 days, 24 weeks to 12 weeks, and 1 year to 24 weeks.
- **Current note:** released as a compact one-store subset to keep the benchmark manageable while preserving item-level sales diversity.

### PhysioNet 2012

- **Domain:** medical and ICU time-series forecasting.
- **Task:** forecast ICU clinical variable values from recent patient measurements and patient-level context.
- **Forecasting unit:** one ICU stay-variable pair per series; 107,188 hourly clinical series.
- **Context variables:** vital signs, laboratory-style variables, hour features, age, gender, height, ICU type, SAPS-I, and SOFA.
- **Windows:** 6 hours to 6 hours, 12 hours to 12 hours, and 24 hours to 24 hours.
- **Current note:** useful for testing forecasting under clinical heterogeneity, sparse observations, and patient-state context.

### PEMS04

- **Domain:** road traffic forecasting.
- **Task:** forecast 5-minute traffic flow for road sensors.
- **Forecasting unit:** one road sensor per series; 307 sensor series.
- **Context variables:** occupancy, speed, road-network graph features, sensor index, and synthetic 5-minute calendar fields.
- **Windows:** 24 hours to 1 hour, 7 days to 24 hours, and 28 days to 7 days.
- **Current note:** the released source file does not include original wall-clock timestamps, so a regular synthetic 5-minute grid preserves temporal order.

### PEMS07

- **Domain:** road traffic forecasting.
- **Task:** forecast 5-minute traffic flow for a larger road-sensor network.
- **Forecasting unit:** one road sensor per series; 883 sensor series.
- **Context variables:** road-network graph features, sensor index, and synthetic 5-minute calendar fields.
- **Windows:** 24 hours to 1 hour, 7 days to 24 hours, and 28 days to 7 days.
- **Current note:** complements PEMS04 with a larger sensor graph and the same order-preserving synthetic timestamp design.

### NYC TLC

- **Domain:** urban mobility forecasting.
- **Task:** forecast hourly taxi pickup demand.
- **Forecasting unit:** one taxi type and pickup-zone pair per series; 513 hourly series.
- **Context variables:** passenger count, trip distance, fare amount, total amount, tip amount, drop-off diversity, location ID, and calendar cycles.
- **Windows:** 7 days to 24 hours, 28 days to 7 days, and 90 days to 14 days.
- **Current note:** useful for city-level demand forecasting with spatial zone and mobility-context signals.

### FRED-MD

- **Domain:** macroeconomic forecasting.
- **Task:** forecast transformed monthly macroeconomic indicator values.
- **Forecasting unit:** one macroeconomic variable per series; 126 monthly series.
- **Context variables:** raw value, transformation code, year, month, quarter, month index, and cyclic month features.
- **Windows:** 3 years to 1 month, 5 years to 12 months, and 10 years to 24 months.
- **Current note:** supports long-horizon macroeconomic forecasting where variable meaning and transformation metadata matter.

### Jena Climate

- **Domain:** climate and weather forecasting.
- **Task:** forecast air temperature at the Jena weather station.
- **Forecasting unit:** one station-level temperature series at 10-minute frequency.
- **Context variables:** pressure, relative humidity, wind velocity, maximum wind velocity, and wind direction.
- **Windows:** 24 hours to 6 hours, 7 days to 24 hours, and 30 days to 7 days.
- **Current note:** compact single-station weather benchmark with dense high-frequency observations.

### Basin Streamflow

- **Domain:** hydrology and streamflow forecasting.
- **Task:** forecast daily streamflow for river basins.
- **Forecasting unit:** one river basin per series; 27 daily basin series.
- **Context variables:** precipitation, radiation, snow water equivalent, maximum and minimum temperature, vapor pressure, basin latitude, basin elevation, basin area, and water-year calendar features.
- **Windows:** 1 year to 7 days, 3 years to 30 days, and 10 years to 1 year.
- **Current note:** useful for scientific forecasting where physical basin attributes and hydro-meteorological forcing are central.

### Alibaba Cluster

- **Domain:** AIOps and cloud-resource forecasting.
- **Task:** forecast machine CPU utilization.
- **Forecasting unit:** one machine per series; first 100 machine series at hourly frequency.
- **Context variables:** memory utilization, disk IO utilization, network IO utilization, hour, weekday, and weekend indicator.
- **Windows:** 24 hours to 6 hours, 7 days to 24 hours, and 30 days to 7 days.
- **Current note:** compact subset designed for standard CPU-utilization forecasting without processing the full cluster trace.

### AQ Data

- **Domain:** air quality forecasting.
- **Task:** forecast hourly PM2.5 concentration for monitoring stations.
- **Forecasting unit:** one monitoring station per series; 3,720 hourly station series.
- **Context variables:** PM10, NO2, O3, SO2, CO, latitude, longitude, coarse region code, station index, and calendar fields.
- **Windows:** 24 hours to 24 hours, 7 days to 3 days, and 30 days to 7 days.
- **Current note:** the provided source files do not contain temperature, humidity, wind speed, wind direction, or pressure, so the first release uses available co-pollutants, station coordinates, regional context, and calendar variables.

## Data Organization

Each dataset is organized into a unified lightweight CSV-based structure.

```text
datasets/<domain>/<dataset_id>/
  processed/
    target/
      <series_id>.csv
    numeric_exogenous/
      <series_id>.csv
    text_exogenous/
      <series_id>.csv
  tasks/
    <dataset_task>.yaml
```

The key components are:

- `target/`: one target-variable CSV for each forecasting series, with `timestamp`, `series_id`, and the target column;
- `numeric_exogenous/`: structured exogenous variables aligned with the target file, such as calendar fields, prices, promotions, weather variables, graph features, clinical covariates, hydrologic forcing, and machine-resource signals;
- `text_exogenous/`: timestamp-aligned natural-language context for the entity, time point, domain, and forecasting task;
- `tasks/`: YAML task definitions describing the target variable, numeric and text exogenous variables, alignment rule, chronological split policy, and short-, medium-, and long-horizon forecasting windows.

## Variable Types

FutureCast-Bench uses three public-facing variable categories.

| Variable Type | Meaning | Examples |
|---|---|---|
| Target variable | The value to be forecasted | wind power, electricity price, electricity load, sales, traffic flow, clinical value, macroeconomic indicator, streamflow, CPU utilization, PM2.5 |
| Numeric exogenous variables | Structured variables outside the target sequence | calendar features, price, promotion, weather, hydrologic forcing, sensor graph features, patient attributes, machine-resource variables, station coordinates, co-pollutants |
| Text exogenous variables | Natural-language context associated with entities or timestamps | holiday descriptions, region descriptions, station descriptions, basin descriptions, machine context, product-store descriptions, variable descriptions, air-quality station context |

## Task System

FutureCast-Bench supports a multi-layer task system from basic forecasting to context-aware reasoning.

| Task Type | Goal |
|---|---|
| Context-aware forecasting | Forecast future values using historical series and contextual information |
| Context selection | Identify which contextual variables are relevant to the current forecasting task |
| Context-sequence alignment | Align events or textual context with the corresponding time intervals and target series |
| Trend reasoning | Infer future trend direction from contextual evidence |
| Event impact analysis | Estimate how external events affect future values |
| Counterfactual forecasting | Forecast under changed contextual assumptions |
| Context gap detection | Identify missing information needed for a better forecast |
| Forecast revision | Update forecasts when new evidence becomes available |
| Explanation generation | Produce evidence-grounded forecasting explanations |

## Evaluation Dimensions

FutureCast-Bench evaluates models along multiple dimensions.

| Dimension | Example Metrics |
|---|---|
| Numerical forecasting accuracy | MAE, RMSE, WAPE, MASE, CRPS |
| Trend judgment | direction accuracy, trend accuracy, turning-point F1 |
| Context understanding | context relevance accuracy, evidence selection F1 |
| Reasoning quality | evidence-grounded score, reasoning faithfulness, counterfactual consistency |
| Dynamic adaptation | context gap detection, forecast revision gain |

### Forecast Revision Gain

One distinctive metric in FutureCast-Bench is **Forecast Revision Gain**, which measures whether a model can improve its prediction after receiving new contextual evidence.

```text
Forecast Revision Gain = initial forecast error - revised forecast error
```

A positive value indicates that the model successfully used new contextual information to revise its forecast.

## Why This Benchmark Matters

FutureCast-Bench is designed for a forecasting setting where models need to understand not only *what happened before*, but also *why the future may change*.

It aims to support research on:

- context-aware time series foundation models;
- LLM-driven time series forecasting;
- multimodal forecasting with numerical and textual context;
- reasoning-enhanced forecasting models;
- agentic forecasting systems that actively seek missing context;
- robust forecasting under events, distribution shifts, and hard-test scenarios.

## Roadmap

Planned next steps include:

- expanding event-rich contextual annotations for electricity markets, transportation, retail, hydrology, air quality, AIOps, and medical forecasting;
- adding more financial market and industrial operation datasets;
- releasing model baselines and leaderboard protocols;
- providing scripts for reproducible preprocessing and evaluation.

## Repository Status

This repository is under active development. The current version focuses on benchmark construction, dataset standardization, task design, and documentation. Data release links, preprocessing scripts, baseline models, and evaluation instructions will be updated as the benchmark is finalized.


## Contact

FutureCast（天星台） is developed by the AGI Research Group at the State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China.

For questions, suggestions, or collaboration, please open an issue in this repository.
