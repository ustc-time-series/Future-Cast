<p align="center">
  <img src="logo.png" alt="FutureCast logo" width="520">
</p>

<h1 align="center">FutureCast</h1>

<p align="center">
  <strong>A Multi-Domain Benchmark for Contextual Time Series Forecasting with Large Language Models</strong>
</p>

<p align="center">
  <a href="https://ustc-time-series.github.io/future-cast/">Project website</a> ·
  <a href="#benchmark-overview">Benchmark</a> ·
  <a href="#datasets">Datasets</a> ·
  <a href="#citation">Citation</a>
</p>

FutureCast evaluates whether LLM-based and agentic forecasting systems can integrate historical target observations with heterogeneous contextual information relevant to future evolution. It unifies diverse real-world forecasting tasks under a common, leakage-safe forecast-time boundary and supports matched interventions that add, remove, isolate, shuffle, or sanitize context while keeping the forecasting case fixed.

<p align="center">
  <img src="https://ustc-time-series.github.io/future-cast/assets/futurecast-overview.png" alt="FutureCast benchmark overview" width="100%">
</p>

## Benchmark overview

- **26 real-world data sources** across **8 domain families**
- **484,435 benchmark instances** spanning 0.1-second telemetry to monthly indicators
- Lookback windows of **6–672** observations and prediction windows of **1–288** observations
- **474,796** instances in the core numerical forecasting track
- Separate evaluation tracks for **remaining-useful-life regression** and **market-direction classification**
- Five context families: observed covariates, known-future covariates, static attributes, textual descriptions, and event information
- Unified JSONL instances with explicit forecast origins, time-valid context, and hidden future targets

## Datasets

| Domain | Sources |
|---|---|
| Energy | AEMO, Liander, OPSD, SDWPF, iFLYTEK |
| Scientific | AQData, Basin Streamflow, Jena Climate, MEG03 |
| Computing | Alibaba Cluster, MSDS, TelecomTS |
| Finance | FI2010LOB, FNSPID100, FRED-MD |
| Retail | Favorita, M5, Rossmann |
| Healthcare | MIMIC-III, PhysioNet 2012, VitalDB |
| Transportation | NYC-TLC, PEMS04, PEMS07 |
| Industrial | C-MAPSS, Stanford Nova |

## Contextual information

FutureCast separates context by semantic role and forecast-time availability:

- **Observed covariates:** auxiliary numerical variables observed up to the forecast origin.
- **Known-future covariates:** inputs legitimately known over the prediction window, such as calendars or schedules.
- **Static attributes:** time-invariant information describing the entity, system, or location.
- **Textual descriptions:** dataset, variable, entity, task, and domain-knowledge descriptions.
- **Event information:** time-stamped events that may influence the future target.

Context is exposed only when it is available at the forecast origin or legitimately known over the prediction horizon. Target-equivalent language is removed before formal evaluation.

## Evaluation

The main benchmark compares statistical, machine-learning, deep-learning, foundation-model, LLM-based, and agentic forecasters under the same target-history boundary. Controlled contextual analyses keep the model, numerical history, forecast origin, horizon, output parser, and hidden target fixed while varying only the textual information.

The paper evaluates ARIMA, Prophet, XGBoost, PatchTST, DLinear, ConvTimeNet, Sundial, Chronos-2, TimesFM 2.5, TokenCast, Time-LLM, TimeReasoner, Time-R1, AlphaCast, Cast-R1, and TimeSeriesScientist. Metrics include source-level MSE and MAE, Average Relative MAE for matched context comparisons, MAE ranks, paired Wilcoxon tests, and source-clustered bootstrap intervals.

## Main findings

- Basic task context reduces paired relative MAE by **12.55%**, while full leakage-filtered context reaches **25.69%** relative to numerical-only forecasting.
- Event/temporal information and domain descriptions are the strongest individual context types by mean MAE rank, although no universal ordering is established.
- Context is especially helpful for short histories and near-term horizons.
- Context effects vary substantially across sources; irrelevant or poorly calibrated context can degrade forecasting.
- Longer prompts are not consistently better, and unsanitized target-equivalent text can create invalid performance gains.

## Repository status

The current code release contains a lightweight Python package, loader and validator components, tests, a toy file-processing workflow, and benchmark documentation. Full processed-data links, benchmark adapters, baseline scripts, and submission checks will be released in versioned updates.

```bash
git clone https://github.com/ustc-time-series/Future-Cast.git
cd Future-Cast
pip install -e .
pytest
```

## Citation

```bibtex
@misc{wang2026futurecast,
  title  = {FutureCast: A Multi-Domain Benchmark for Contextual Time Series Forecasting with Large Language Models},
  author = {Wang, Jiahao and Cheng, Mingyue and Tao, Xiaoyu and Zhang, Shilong and Liu, Qi},
  year   = {2026},
  url    = {https://github.com/ustc-time-series/Future-Cast}
}
```

## Contact

FutureCast is developed at the State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China. Please open a GitHub issue for questions, feedback, or collaboration.
