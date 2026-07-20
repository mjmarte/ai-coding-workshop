"""Generate the advanced recovery-prediction notebooks."""
import json
import pathlib


REPO = "mjmarte/ai-coding-workshop"


def md(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.strip().splitlines(keepends=True),
    }


def code(text):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.strip("\n").splitlines(keepends=True),
    }


SETUP = f'''
import os, subprocess, sys

REPO = "{REPO}"
if os.path.isdir(".git"):
    result = subprocess.run(["git", "pull", "--ff-only", "-q"])
elif os.path.isdir("ai-coding-workshop"):
    os.chdir("ai-coding-workshop")
    result = subprocess.run(["git", "pull", "--ff-only", "-q"])
elif not os.path.exists("data"):
    result = subprocess.run(["git", "clone", "-q", f"https://github.com/{{REPO}}.git"])
    if result.returncode == 0:
        os.chdir("ai-coding-workshop")
else:
    result = subprocess.run(["git", "status"], capture_output=True)
if result.returncode != 0:
    raise SystemExit("Could not download or update the workshop files. Check the GitHub link.")

missing = [path for path in ("data/recovery_prediction.csv",) if not os.path.exists(path)]
if missing:
    raise SystemExit(f"Setup incomplete. Missing: {{missing}}")
print("Ready.")
'''


HEADER_STARTER = '''
# Advanced Python: acute-to-12-month recovery prediction

This advanced notebook uses a separate synthetic cohort. It defines predictors available at
an acute assessment and estimates a synthetic 12-month language outcome.

The exercise evaluates a prediction workflow. It does not provide external validation,
clinical utility, calibration, or evidence from real participants.

For each task, copy the prompt into an AI assistant, paste the returned code into the empty
cell, run it, and compare the result with the checkpoint.
'''


HEADER_SOLUTION = '''
# Advanced Python: solution / reference

Working code for the advanced recovery-prediction exercises.
'''


TASKS = [
    (
        "Task A1 - Define the prediction question before fitting a model",
        '''
Goal: identify the outcome, specify predictors available at the acute assessment,
and confirm one row per participant.

The prediction question requires a time boundary. The 12-month outcome and later measurements
are excluded from the acute predictor matrix.
''',
        '''I am working in Python with `data/recovery_prediction.csv`, a synthetic cohort with one
row per acute-stroke participant. My outcome is `outcome_wab_aq_12m`, a 12-month WAB-AQ.

The following variables are available at the acute assessment: age, sex, education_years,
acute_wab_aq, acute_discourse_score, lesion_volume_ml, cortical_lesion_pct,
dorsal_disconnection_pct, and ventral_disconnection_pct.

Write pandas code that loads the file into `recovery`, verifies that participant_id is unique,
prints the sample size and missing-value count per column, and creates two named predictor
lists:
- `clinical_features`: age, education_years, acute_wab_aq, acute_discourse_score
- `multimodal_features`: every clinical feature plus lesion_volume_ml, cortical_lesion_pct,
  dorsal_disconnection_pct, and ventral_disconnection_pct

Do not put participant_id, sex, or outcome_wab_aq_12m into either predictor list. Give only
code with short comments.''',
        '''
import pandas as pd

recovery = pd.read_csv("data/recovery_prediction.csv")
outcome = "outcome_wab_aq_12m"
clinical_features = [
    "age", "education_years", "acute_wab_aq", "acute_discourse_score",
]
multimodal_features = clinical_features + [
    "lesion_volume_ml", "cortical_lesion_pct",
    "dorsal_disconnection_pct", "ventral_disconnection_pct",
]

assert recovery["participant_id"].is_unique
print("participants:", len(recovery))
print(recovery.isna().sum())
''',
        "Expected: 90 participants, one row per participant, and no outcome or identifier in either predictor list.",
    ),
    (
        "Task A2 - Compare baseline and multimodal models without leakage",
        '''
Goal: compare a clinical baseline model with a model that additionally includes acute
lesion and disconnection measures.

Imputation, scaling, and fitting occur within each resampling fold so that held-out records do
not influence the training procedure.
''',
        '''Using `recovery`, `outcome`, `clinical_features`, and `multimodal_features`, compare two
Ridge-regression pipelines: a clinical model and a clinical-plus-imaging model.

Use 5-fold repeated cross-validation with 20 repeats and random_state=202607. Each pipeline
must impute missing values, standardize predictors, and fit RidgeCV with alphas
[0.01, 0.1, 1, 10, 100]. Keep all preprocessing inside the Pipeline.

For each feature set, report the mean and SD of cross-validated mean absolute error and R-squared.
Return a two-row DataFrame named `cv_summary`. Do not fit on the full dataset before evaluating.
Give only code with short comments.''',
        '''
from sklearn.impute import SimpleImputer
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import RepeatedKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

cv = RepeatedKFold(n_splits=5, n_repeats=20, random_state=202607)

def evaluate_feature_set(features):
    model = make_pipeline(
        SimpleImputer(),
        StandardScaler(),
        RidgeCV(alphas=[0.01, 0.1, 1, 10, 100]),
    )
    scores = cross_validate(
        model,
        recovery[features],
        recovery[outcome],
        cv=cv,
        scoring={"mae": "neg_mean_absolute_error", "r2": "r2"},
    )
    return {
        "MAE_mean": -scores["test_mae"].mean(),
        "MAE_sd": scores["test_mae"].std(),
        "R2_mean": scores["test_r2"].mean(),
        "R2_sd": scores["test_r2"].std(),
    }

cv_summary = pd.DataFrame(
    [evaluate_feature_set(clinical_features), evaluate_feature_set(multimodal_features)],
    index=["clinical", "clinical_plus_imaging"],
).round(2)
print(cv_summary)
''',
        "Expected: clinical MAE 5.25 (SD 0.71), R-squared 0.81 (SD 0.08); "
        "clinical-plus-imaging MAE 4.85 (SD 0.84), R-squared 0.82 (SD 0.08). "
        "These are synthetic development results, not evidence of clinical utility.",
    ),
    (
        "Task A3 - Inspect out-of-fold predictions and error distribution",
        '''
Goal: generate held-out predictions and inspect their errors alongside the resampled summary.
''',
        '''Using the multimodal feature set, generate one out-of-fold prediction per participant with
5-fold shuffled KFold cross-validation and random_state=202607. Keep imputation, scaling, and
RidgeCV inside a Pipeline. Store predictions in `oof_pred`.

Make a two-panel matplotlib figure: observed versus predicted 12-month WAB-AQ with an identity
line, and absolute prediction error by sex with individual points. Print overall MAE and MAE by
sex with the number of participants per group.

Treat the sex comparison as a descriptive error audit, not evidence of a subgroup difference.
Give only code with short comments.''',
        '''
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold, cross_val_predict

oof_model = make_pipeline(
    SimpleImputer(),
    StandardScaler(),
    RidgeCV(alphas=[0.01, 0.1, 1, 10, 100]),
)
oof_cv = KFold(n_splits=5, shuffle=True, random_state=202607)
oof_pred = cross_val_predict(
    oof_model, recovery[multimodal_features], recovery[outcome], cv=oof_cv,
)

audit = recovery[["sex", outcome]].copy()
audit["predicted_wab_aq_12m"] = oof_pred
audit["absolute_error"] = (audit[outcome] - audit["predicted_wab_aq_12m"]).abs()

print("overall MAE:", round(mean_absolute_error(audit[outcome], oof_pred), 2))
print(audit.groupby("sex")["absolute_error"].agg(["count", "mean"]).round(2))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(audit[outcome], audit["predicted_wab_aq_12m"], alpha=0.7)
axes[0].plot([20, 100], [20, 100], color="black", linewidth=1)
axes[0].set(xlabel="Observed 12-month WAB-AQ", ylabel="Out-of-fold prediction")

for x, group in enumerate(["F", "M"]):
    values = audit.loc[audit["sex"] == group, "absolute_error"]
    axes[1].scatter([x] * len(values), values, alpha=0.7)
axes[1].set(xticks=[0, 1], xticklabels=["F", "M"], ylabel="Absolute prediction error")
fig.tight_layout()
plt.show()
''',
        "Expected: overall out-of-fold MAE 4.84. Each point in the first panel was predicted "
        "without fitting that participant. The displayed subgroup errors are descriptive.",
    ),
    (
        "Task A4 - Fact-check an AI-written prediction summary",
        '''
Goal: constrain an AI-written summary to the resampling output and the scope of a
synthetic development exercise.

Cross-validation estimates performance under the specified resampling procedure. It does not
establish clinical utility, causal contribution, external validity, calibration, or deployment readiness.
''',
        '''Here is my cross-validation summary table from a synthetic development exercise:

[PASTE cv_summary HERE]

Write two Results sentences. Report only numbers in the table. State which model had lower
resampled MAE. Do not call the model clinically useful, externally validated, calibrated,
causal, or ready for deployment.''',
        '''
# Do not run code for this task. Paste the prompt into the AI assistant, then compare every
# number and every claim in its response against cv_summary and the stated scope of the dataset.
''',
        "A correct response reports only the resampled metrics shown in `cv_summary` and makes no clinical, causal, or external-validation claim.",
    ),
    (
        "Task A5 - Use an agent for a bounded reproducibility audit",
        '''
Goal: ask an agent to inspect the project without authority to alter data or
analysis files.

An agent can inventory files and identify consistency questions. It does not determine the
predictor set or the validity of a clinical claim.
''',
        '''I am in the `ai-coding-workshop` repository. Perform a READ-ONLY reproducibility audit of
the advanced recovery-prediction exercise. Do not edit, create, delete, or run any file.

Return a compact table with: (1) raw or generated input files, (2) the script that produces each
input, (3) the notebook that consumes it, (4) model outcome and predictors, and (5) one leakage
or interpretation risk at each stage. Flag any claim in the materials that exceeds what a
synthetic development exercise can establish. Cite file paths and line numbers where possible.''',
        '''
# Do not run code for this task. Paste the prompt into a coding agent with read-only
# repository access, then inspect the cited file paths yourself.
''',
        "A useful agent response cites the generator, the CSV, this notebook, and the resampling code. It does not make clinical claims or edit the project.",
    ),
]


def build(starter):
    cells = [md(HEADER_STARTER if starter else HEADER_SOLUTION), md("## Setup\n\nRun this cell first."), code(SETUP)]
    for title, goal, prompt, solution, checkpoint in TASKS:
        cells.append(md(f"---\n## {title}\n\n{goal.strip()}"))
        if starter:
            cells.append(md("Copy this prompt into your AI assistant:\n\n```\n" + prompt.strip() + "\n```"))
            cells.append(code("# paste the AI's code here, then press Shift+Enter to run it\n"))
            cells.append(md(f"> Checkpoint: {checkpoint}"))
        else:
            cells.append(code(solution))
            cells.append(md(f"> {checkpoint}"))
    return {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }


here = pathlib.Path(__file__).parent
for name, starter in [
    ("02_advanced_recovery_starter.ipynb", True),
    ("02_advanced_recovery_solution.ipynb", False),
]:
    (here / name).write_text(json.dumps(build(starter), indent=1))
    print("wrote", name)
