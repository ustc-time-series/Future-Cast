# FutureCast

**FutureCast** is a context-aware time series forecasting benchmark and training corpus for evaluating whether forecasting models can move beyond numerical extrapolation and reason with real-world context.

Instead of representing each forecasting task only as:

```text
historical time series -> future values
```

FutureCast represents each task as:

```text
historical time series + numeric exogenous variables + textual exogenous context + evidence annotations -> forecasting target
```

The goal is to support the next generation of time series foundation models, LLM-driven forecasting models, slow-thinking forecasting systems, and agentic forecasting workflows.

## Why FutureCast?

Most existing time series benchmarks are built around the numerical series itself. They evaluate whether a model can forecast future values from past values across different domains, frequencies, and horizons. This is necessary, but it is not enough for real-world forecasting.

In real applications, the future is often shaped by information outside the target sequence:

- electricity demand and prices are affected by weather, holidays, supply-demand balance, market rules, and grid conditions;
- traffic flow is affected by accidents, weather, events, commuting patterns, and spatial structure;
- retail demand is affected by promotion, price, holidays, inventory, store location, and consumer behavior;
- clinical variables are affected by patient status, treatment intervention, missingness, and medical knowledge;
- macroeconomic indicators are affected by policy changes, inflation, interest rates, employment, and market expectations;
- industrial sensor signals are affected by operating conditions, maintenance, environment, and abnormal events.

Two time series can have similar historical shapes but very different futures because their surrounding contexts are different. A benchmark that only measures numerical error cannot tell whether a model is merely fitting statistical patterns or actually understanding why the future changes.

FutureCast is designed to fill this gap. It evaluates not only whether a model predicts accurately, but also whether it can:

- identify which contextual information is relevant;
- align context with the correct time interval and forecasting target;
- reason about how external factors affect future values;
- revise predictions when new evidence appears;
- generate evidence-grounded explanations for forecasting decisions.

## Core Capabilities

FutureCast is organized around three core capabilities.

### 1. Context-Sequence Alignment and Fusion

Models should be able to align target time series with heterogeneous context, including calendar information, spatial attributes, weather, events, business rules, domain knowledge, and textual descriptions.

### 2. Contextual Reasoning for Forecasting

Models should not only output future values, but also reason about the potential impact of contextual factors. For example, high temperature may increase electricity load, promotion may increase retail demand, and policy change may shift macroeconomic trends.

### 3. Dynamic Context Adaptation

Real forecasting is often an iterative process. A model may first make a prediction with incomplete information, then receive new evidence, update its reasoning, and revise the forecast. FutureCast includes tasks for evaluating this dynamic adaptation ability.

## Current Benchmark Status

The current processed benchmark covers **10 datasets** across **6 domains**, with approximately **359K forecasting series**, **239M timestamp-level records**, and **230M valid target observations**.

| Domain | Dataset | Forecasting Target | Forecasting Unit | Frequency | Dataset Size | Variables | Lookback / Prediction Windows |
|---|---|---|---|---|---|---|---|
| Energy | SDWPF | Wind turbine power (`Patv`) | Turbine | 10 min | 134 turbines; about 11.36M timestamp records; about 7.81M valid target observations | 1 target; 17 numeric exogenous variables; 2 types of text exogenous context | Lookback: 1 / 10 / 15 days; Prediction: 8 hours / 3.3 days / 5 days |
| Power | AEMO NEM DispatchIS | Regional electricity price (`RRP`) | NEM region | 5 min | 5 regions; about 130K timestamp records; about 129K valid target observations | 1 target; 15 numeric exogenous variables; 2 types of text exogenous context | Lookback: 3 hours / 3 days / 21 days; Prediction: 1 hour / 1 day / 7 days |
| Sales | M5 | Daily unit sales | Item-store pair | 1 day | 30,490 item-store series; about 59.18M daily records | 1 target; 12 numeric exogenous variables; 2 types of text exogenous context | Lookback: 84 / 252 / 504 days; Prediction: 28 / 84 / 168 days |
| Sales | Rossmann Store Sales | Store sales (`Sales`) | Store | 1 day | 1,115 store series; about 1.06M daily records; about 1.02M valid target observations | 1 target; 20 numeric exogenous variables; 2 types of text exogenous context | Lookback: 84 / 252 / 504 days; Prediction: 28 / 84 / 168 days |
| Sales | Favorita Grocery Sales | Unit sales (`unit_sales`) | Store-item pair | 1 day | 219,126 store-item series; about 128.87M daily records; about 125.49M valid target observations | 1 target; 27 numeric exogenous variables; 2 types of text exogenous context | Lookback: 84 / 252 / 504 days; Prediction: 28 / 84 / 168 days |
| Medical | PhysioNet 2012 | Clinical variable value | ICU stay-variable pair | 1 hour | 107,188 patient-variable series; about 5.25M hourly records; about 3.11M valid target observations | 1 target; 30 numeric exogenous variables; 2 types of text exogenous context | Lookback: 18 / 36 / 72 hours; Prediction: 6 / 12 / 24 hours |
| Traffic | PEMS04 | Traffic flow | Traffic sensor | 5 min | 307 sensor series; about 5.22M timestamp records | 1 target; 16 numeric exogenous variables; 2 types of text exogenous context | Lookback: 3 / 9 / 72 hours; Prediction: 1 / 3 / 24 hours |
| Traffic | PEMS07 | Traffic flow | Traffic sensor | 5 min | 883 sensor series; about 24.92M timestamp records | 1 target; 14 numeric exogenous variables; 2 types of text exogenous context | Lookback: 3 / 9 / 72 hours; Prediction: 1 / 3 / 24 hours |
| Traffic | NYC TLC | Hourly pickup trip count | Taxi type-pickup zone pair | 1 hour | 513 taxi-zone series; about 3.36M hourly records | 1 target; 23 numeric exogenous variables; 2 types of text exogenous context | Lookback: 3 / 21 / 42 days; Prediction: 1 / 7 / 14 days |
| Economics | FRED-MD | Transformed macroeconomic value | Macroeconomic variable | 1 month | 126 macroeconomic series; about 100K monthly records; about 99.7K valid target observations | 1 target; 12 numeric exogenous variables; 2 types of text exogenous context | Lookback: 36 / 36 / 72 months; Prediction: 1 / 12 / 24 months |

## Data Organization

Each dataset is organized into a unified CSV-based structure.

```text
datasets/<domain>/<dataset_id>/
  raw/
  processed/
    <dataset_id>_<frequency>_long.csv
    <dataset_id>_static_features.csv
    by_series/
      target/
      numeric_exogenous/
        observed/
        known_future/
      text_exogenous/
        static_context/
        time_context/
      masks/
      manifest.csv
  splits/
    *_temporal_split.csv
    *_rolling_windows_short.csv
    *_rolling_windows_medium.csv
    *_rolling_windows_long.csv
  tasks/
    *_short.yaml
    *_medium.yaml
    *_long.yaml
  dataset_card.md
```

The key components are:

- `target/`: one target-variable CSV for each forecasting series;
- `numeric_exogenous/`: structured exogenous variables such as calendar fields, prices, promotions, weather-related variables, traffic attributes, clinical covariates, and entity metadata;
- `text_exogenous/`: textual descriptions of entities and time points, such as event descriptions, holiday context, missingness descriptions, region descriptions, or variable descriptions;
- `masks/`: quality-control masks for missing values, invalid observations, future rows, and hard-test cases;
- `splits/`: train, validation, test splits and non-overlapping rolling evaluation windows;
- `tasks/`: YAML task definitions for short-, medium-, and long-horizon forecasting;
- `dataset_card.md`: dataset-level documentation.

## Variable Types

FutureCast uses three public-facing variable categories.

| Variable Type | Meaning | Examples |
|---|---|---|
| Target variable | The value to be forecasted | wind power, electricity price, sales, traffic flow, clinical value, macroeconomic indicator |
| Numeric exogenous variables | Structured variables outside the target sequence | calendar features, price, promotion, region, store metadata, sensor graph features, patient attributes, historical covariates |
| Text exogenous variables | Natural-language context associated with entities or timestamps | holiday descriptions, event descriptions, region descriptions, product-store descriptions, missingness descriptions, variable descriptions |

## Task System

FutureCast supports a multi-layer task system from basic forecasting to context-aware reasoning.

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

FutureCast evaluates models along multiple dimensions.

| Dimension | Example Metrics |
|---|---|
| Numerical forecasting accuracy | MAE, RMSE, WAPE, MASE, CRPS |
| Trend judgment | direction accuracy, trend accuracy, turning-point F1 |
| Context understanding | context relevance accuracy, evidence selection F1 |
| Reasoning quality | evidence-grounded score, reasoning faithfulness, counterfactual consistency |
| Dynamic adaptation | context gap detection, forecast revision gain |

### Forecast Revision Gain

One distinctive metric in FutureCast is **Forecast Revision Gain**, which measures whether a model can improve its prediction after receiving new contextual evidence.

```text
Forecast Revision Gain = initial forecast error - revised forecast error
```

A positive value indicates that the model successfully used new contextual information to revise its forecast.

## Why This Benchmark Matters

FutureCast is designed for a forecasting setting where models need to understand not only *what happened before*, but also *why the future may change*.

It aims to support research on:

- context-aware time series foundation models;
- LLM-driven time series forecasting;
- multimodal forecasting with numerical and textual context;
- reasoning-enhanced forecasting models;
- agentic forecasting systems that actively seek missing context;
- robust forecasting under events, distribution shifts, and hard-test scenarios.

## Roadmap

Planned next steps include:

- adding standalone electricity load forecasting datasets;
- expanding weather and environmental forecasting tasks;
- adding more financial market datasets;
- enriching event-based and text-based contextual annotations;
- releasing model baselines and leaderboard protocols;
- providing scripts for reproducible preprocessing and evaluation.

## Repository Status

This repository is under active development. The current version focuses on benchmark construction, dataset standardization, task design, and documentation. Data release links, preprocessing scripts, baseline models, and evaluation instructions will be updated as the benchmark is finalized.


## Contact

FutureCast is developed by the AGI Research Group at the State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China.

For questions, suggestions, or collaboration, please open an issue in this repository.

