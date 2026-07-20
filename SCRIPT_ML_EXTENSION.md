# ML extension: acute-to-chronic prediction

Use this after the mixed-effects route, not as the opening workshop sequence. The extension
requires an AI chat and the [advanced Colab notebook](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/02_advanced_recovery_starter.ipynb).

## 0:00-0:05 | Define the prediction boundary

Run Task A1. The outcome is synthetic 12-month WAB-AQ. Predictor sets include only measures
available at the acute assessment. Confirm 90 participants, one row per participant, and no
outcome or identifier in either predictor list.

Say:

> Prediction begins with temporal ordering. The 12-month outcome is unavailable at the acute
> assessment and cannot enter the acute predictor matrix.

## 0:05-0:13 | Evaluate two predictor sets

Run Task A2. Inspect the returned code before executing it: imputation, scaling, and Ridge
regression must be inside the pipeline, and repeated cross-validation must evaluate the pipeline.

Say:

> The clinical-plus-imaging model has lower mean absolute error in this synthetic development
> exercise, 4.85 versus 5.25 WAB points. The comparison concerns predictor sets under the stated
> resampling procedure. It does not identify a causal imaging feature or establish clinical use.

## 0:13-0:15 | Limit the written claim

Run Task A4. The response may report the displayed resampled MAE and R-squared values. It may not
claim external validation, calibration, clinical utility, or deployment readiness.

Task A3 is the optional second ML example. It displays one out-of-fold prediction per participant
and a descriptive error audit. Use it when an additional 10 minutes are available.
