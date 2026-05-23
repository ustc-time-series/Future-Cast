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

The current processed benchmark covers **14 datasets** across **9 domains**, with approximately **145K forecasting series** and **114M timestamp-level records**. Each dataset is stored in a lightweight CSV layout with one target file, one numeric exogenous file, one text exogenous file, and one task YAML definition for each benchmark task.

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
| Target variable | The value to be forecasted | wind power, electricity price, electricity load, sales, traffic flow, clinical value, macroeconomic indicator, streamflow, CPU utilization |
| Numeric exogenous variables | Structured variables outside the target sequence | calendar features, price, promotion, weather, hydrologic forcing, sensor graph features, patient attributes, machine-resource variables |
| Text exogenous variables | Natural-language context associated with entities or timestamps | holiday descriptions, region descriptions, station descriptions, basin descriptions, machine context, product-store descriptions, variable descriptions |

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

- expanding event-rich contextual annotations for electricity markets, transportation, retail, hydrology, AIOps, and medical forecasting;
- adding more financial market and industrial operation datasets;
- releasing model baselines and leaderboard protocols;
- providing scripts for reproducible preprocessing and evaluation.

## Repository Status

This repository is under active development. The current version focuses on benchmark construction, dataset standardization, task design, and documentation. Data release links, preprocessing scripts, baseline models, and evaluation instructions will be updated as the benchmark is finalized.


## Contact

FutureCast（天星台） is developed by the AGI Research Group at the State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China.

For questions, suggestions, or collaboration, please open an issue in this repository.
