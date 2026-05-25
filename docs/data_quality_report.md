# FutureCast-Bench Data Quality Report

**Version:** current processed benchmark snapshot  
**Generated on:** 2026-05-25  
**Scope:** 15 processed datasets across 10 domains  

This report summarizes the current quality status of the processed FutureCast-Bench datasets. It focuses on the lightweight benchmark layout:

```text
processed/
  target/
  numeric_exogenous/
  text_exogenous/
tasks/
```

The current report is a **format-level and sample-level quality report**. It verifies file organization, file count consistency, sampled key alignment, sampled missingness, and known source-data limitations. It is not yet a full row-by-row audit of every timestamp in the 277M-record processed corpus.

## Overall Status

| Check | Current Status |
|---|---|
| Dataset count | 15 datasets |
| Domain count | 10 domains |
| Target/numeric/text folder layout | Present for all datasets |
| Target/numeric/text file counts | Matched for all datasets |
| Sampled `timestamp + series_id` alignment | Passed for all datasets |
| Sampled text exogenous blank rate | 0.00% for all sampled files |
| Full row-level audit | Planned next step |

## Quality Method

The current quality pass used the following checks:

1. **Folder-level validation:** confirm that every dataset has `processed/target`, `processed/numeric_exogenous`, `processed/text_exogenous`, and `tasks`.
2. **File-count validation:** confirm that each dataset has the same number of target, numeric exogenous, and text exogenous CSV files.
3. **Sample alignment validation:** for each dataset, inspect first/middle/last available series when possible and verify that target, numeric exogenous, and text exogenous files have the same row count and identical `timestamp + series_id` order.
4. **Sample missingness validation:** compute missing rates for target and numeric exogenous variables in sampled files.
5. **Known limitation review:** record source-data issues, synthetic timestamp usage, sparse observations, and compact-subset decisions.

## Dataset Quality Summary

| Dataset | Target Files | Numeric Files | Text Files | Sample Rows Per Series | Sample Alignment | Sample Target Missing | Sample Numeric Missing | Sample Text Blank | Status |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| SDWPF | 134 | 134 | 134 | 84,785 | Pass | 4.28% | 1.61% | 0.00% | Usable with missing-value handling |
| AEMO NEM DispatchIS | 5 | 5 | 5 | 25,920 | Pass | 0.08% | 0.02% | 0.00% | Good |
| OPSD German Load | 1 | 1 | 1 | 50,401 | Pass | 0.00% | 21.85% | 0.00% | Usable; covariate missingness should be documented |
| M5 | 30,490 | 30,490 | 30,490 | 1,941 | Pass | 0.00% | 0.00% | 0.00% | Good |
| Rossmann Store Sales | 1,115 | 1,115 | 1,115 | 990 | Pass | 4.85% | 15.76% | 0.00% | Usable with holiday/store-metadata caveats |
| Favorita Grocery Sales | 4,081 | 4,081 | 4,081 | 85-1,554 | Pass | 8.67% | 1.71% | 0.00% | Compact subset; uneven series length |
| PhysioNet 2012 | 107,188 | 107,188 | 107,188 | 49 | Pass | 17.69% | 33.33% | 0.00% | Clinically sparse; missingness is part of the task |
| PEMS04 | 307 | 307 | 307 | 16,992 | Pass | 0.00% | 4.44% | 0.00% | Good; synthetic timestamps |
| PEMS07 | 883 | 883 | 883 | 28,224 | Pass | 0.00% | 0.00% | 0.00% | Good; synthetic timestamps |
| NYC TLC | 513 | 513 | 513 | 4,368-8,784 | Pass | 0.00% | 0.00% | 0.00% | Good; variable active-zone coverage |
| FRED-MD | 1 | 1 | 1 | 100,926 | Pass | 1.22% | 0.13% | 0.00% | Good; initial transform missingness expected |
| Jena Climate | 1 | 1 | 1 | 420,224 | Pass | 0.00% | 0.00% | 0.00% | Good |
| Basin Streamflow | 27 | 27 | 27 | 12,784 | Pass | 1.54% | 0.00% | 0.00% | Good; hydrologic gaps retained |
| Alibaba Cluster | 100 | 100 | 100 | 85-192 | Pass | 3.47% | 1.74% | 0.00% | Compact subset; trace timestamps are relative |
| AQ Data | 3,720 | 3,720 | 3,720 | 43,824 | Pass | 67.80% | 27.44% | 0.00% | Sparse station observations; source covariate limitation |

## Dataset-Level Notes

### SDWPF

The SDWPF wind-power dataset has aligned turbine-level files and consistent per-series length in sampled checks. Missing target and numeric values exist, which is expected for SCADA-style wind data. Models should handle missing target history and operating-signal gaps explicitly.

### AEMO NEM DispatchIS

The AEMO electricity price dataset has clean sampled alignment across the five market regions. Missingness is very low in the sampled files. The dataset is currently a 2026 DispatchIS slice, so downstream users should treat it as a compact regional electricity price task rather than a long historical market archive.

### OPSD German Load

The target load series is complete in the sampled check, but numeric covariates have noticeable missingness. This comes mainly from the source coverage of wind generation, solar generation, and day-ahead price fields. The dataset is still useful for load forecasting, but covariate availability should be documented in experiments.

### M5

The M5 processed layout is well aligned, dense, and large-scale. It is one of the strongest current sales datasets in the benchmark because it combines many item-store series with calendar, price, and event context.

### Rossmann Store Sales

Rossmann files align correctly. Target and numeric missingness appear in sampled checks, mostly reflecting store opening status, holiday effects, and competition/promotion metadata availability. Experiments should distinguish true zero sales from closed-store or missing-context periods.

### Favorita Grocery Sales

Favorita is released as a compact one-store subset to avoid excessive benchmark size. Alignment checks pass, but series lengths are uneven because item histories differ. This dataset is useful for grocery-demand context, but it should not be presented as the full Favorita corpus.

### PhysioNet 2012

PhysioNet is intentionally sparse. Missing target and covariate values are part of the clinical time-series setting rather than a simple processing error. This dataset should be evaluated with models and metrics that can handle irregular clinical observations and missing patient measurements.

### PEMS04 and PEMS07

Both PEMS datasets pass sampled alignment checks. The original files do not include real wall-clock timestamps in the processed source, so the benchmark uses a regular synthetic 5-minute grid to preserve temporal order. This should be reported whenever interpreting calendar variables.

### NYC TLC

NYC TLC passes sampled alignment checks with zero sampled missingness. Some series have shorter active coverage than others because taxi-zone activity varies by taxi type and pickup zone.

### FRED-MD

FRED-MD passes sampled alignment checks. Initial missing target values are expected because transformed macroeconomic indicators may require lagged or differenced values. Users should avoid treating early transformed missingness as random data corruption.

### Jena Climate

Jena Climate is the cleanest compact climate dataset in the current release. It has dense 10-minute observations and zero sampled missingness in target and numeric exogenous variables.

### Basin Streamflow

Basin Streamflow passes sampled alignment checks. The small target missingness is retained rather than aggressively imputed because hydrologic data gaps should remain visible to forecasting models and evaluators.

### Alibaba Cluster

Alibaba Cluster is a compact first-100-machine subset. Alignment checks pass, but sampled row counts vary by machine because the selected machines have different available trace durations. Timestamps are relative trace times converted from source values, so users should not interpret them as real calendar dates.

### AQ Data

AQ Data has the largest processed footprint in the current benchmark. Alignment checks pass, but sampled PM2.5 missingness is high because monitoring stations and pollutant measurements are sparse. The provided source files do not include temperature, humidity, wind speed, wind direction, or pressure, so the current release uses available co-pollutants, station coordinates, coarse region context, and calendar features.

## Current Risks and Limitations

| Risk | Affected Datasets | Mitigation |
|---|---|---|
| Sparse target observations | AQ Data, PhysioNet 2012, Favorita, SDWPF, Rossmann | Keep missing values visible; document missingness; use models and metrics that handle sparse histories |
| Numeric covariate missingness | AQ Data, PhysioNet 2012, OPSD German Load, Rossmann | Add per-variable missingness reports in the next quality pass |
| Synthetic timestamps | PEMS04, PEMS07 | Clearly mark calendar features as synthetic order-preserving features |
| Relative timestamps | Alibaba Cluster | Treat timestamps as trace-relative time, not real-world calendar time |
| Uneven series length | Favorita, NYC TLC, Alibaba Cluster | Use chronological splits per series rather than assuming globally identical lengths |
| Compact subset release | Favorita, Alibaba Cluster | Report subset policy and avoid claiming full-corpus coverage |
| Source covariate mismatch | AQ Data | Document unavailable weather variables and avoid listing them as processed covariates |

## Recommended Next Quality Work

The next quality pass should upgrade this report from sample-level validation to full benchmark validation:

1. **Full duplicate-key scan:** verify no duplicated `timestamp + series_id` rows in any processed CSV.
2. **Per-variable missingness table:** report missingness for every target and numeric exogenous variable, not only averaged sampled rates.
3. **Per-series length distribution:** compute min, median, max, and percentile lengths for each dataset.
4. **Timestamp continuity check:** verify expected frequency gaps per series.
5. **Domain range checks:** flag impossible values such as negative demand, impossible humidity, invalid geographic coordinates, or invalid clinical ranges.
6. **Context-text quality check:** detect duplicated, empty, or overly generic text context and separate template text from real event/context text.
7. **Release checklist:** mark each dataset as `ready`, `usable with caveats`, or `needs revision` before public data release.

## Release Interpretation

The current processed benchmark is suitable for documentation, task-design iteration, and initial model-loading experiments. Before a formal public benchmark release, FutureCast-Bench should add automated validators and generate full data quality reports as part of the preprocessing pipeline.
