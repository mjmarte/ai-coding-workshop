# Advanced recovery-prediction workshop: 45-minute facilitator script

Use this as the primary route when the room already knows the basic prompt-to-code workflow.
Participants work in the advanced Colab notebook and an AI chat. The route does not use Posit.
Keep this file, `python/02_advanced_recovery_solution.ipynb`, and a timer on the private display.

## Before the session

- Share the advanced Colab notebook, a new AI conversation, and `PROMPTS.md`.
- Run the notebook setup cell and confirm `Ready.`.
- On the private display, run the advanced solution once. Retain the output from Tasks A2 and A3.
- Participants open the [advanced notebook](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/02_advanced_recovery_starter.ipynb), run setup, and open an AI chat.

The cohort is synthetic. The workshop demonstrates an analysis workflow, not a clinical prediction
model or a recommendation for patient-level decisions.

## 0:00-0:04 | State the prediction question

**ON SCREEN:** advanced notebook header and Task A1.

**SAY:**

> The question is deliberately narrow. We will estimate a synthetic 12-month WAB-AQ from data
> available at the acute assessment. The time boundary determines the predictor matrix. A variable
> measured at 12 months cannot enter a model intended to predict the 12-month outcome.
>
> The analysis has three linked requirements. We first define the outcome and predictor sets. We
> then estimate performance without allowing held-out observations to influence preprocessing or
> model fitting. Finally, we inspect individual held-out predictions and limit the written claim to
> what the resampling output supports.

**DO:** Ask participants to confirm that the notebook displays `Ready.`. Tell them to paste prompts
into a separate AI chat, then paste returned code only into the empty notebook cells.

## 0:04-0:10 | Task A1: define the outcome and predictor sets

**ON SCREEN:** Task A1 prompt.

**DO:** Participants copy the prompt into their AI chat, paste returned code into the empty cell,
and run it. Check that the code creates `recovery`, `outcome`, `clinical_features`, and
`multimodal_features`.

**SAY, AFTER THE CELL RUNS:**

> The dataset contains 90 synthetic participants, one row per participant, with no missing values.
> `outcome_wab_aq_12m` is the outcome. The clinical set contains age, education, acute WAB-AQ, and
> an acute discourse score. The second set adds lesion and disconnection measures available at the
> same acute assessment.
>
> Sex is retained for the descriptive error audit in Task A3. Its exclusion from these predictor
> sets is a workshop decision, not evidence that sex is irrelevant to an actual recovery model.
> In a study, predictor selection follows the clinical question, measurement time, sample size,
> and an analysis plan defined before model fitting.

**CHECK:** `participant_id` and the 12-month outcome do not appear in either predictor list.

## 0:10-0:25 | Task A2: compare two resampled models

**ON SCREEN:** Task A2 prompt, then the returned code before it is run.

**SAY:**

> The comparison is between predictor sets, not between individual variables. The clinical model
> uses acute clinical and discourse information. The clinical-plus-imaging model adds acute lesion
> and disconnection measures. The model is fit repeatedly on one portion of the synthetic cohort
> and evaluated on records omitted from that fit.
>
> Inspect the code before running it. The `Pipeline` must contain imputation, scaling, and Ridge
> regression. The repeated cross-validation object must appear in `cross_validate`. If scaling
> occurs before resampling, information from held-out participants enters the training procedure.

**DO:** Participants send the Task A2 prompt, paste returned code, and run it. While it runs, ask:

> Which operation would leak information if it were completed before the data were split into
> training and held-out folds?

**SAY, AFTER THE TABLE APPEARS:**

> In the supplied synthetic cohort, the clinical model has mean absolute error of 5.25 WAB points
> across repeated folds, with an SD of 0.71. The clinical-plus-imaging model has mean absolute
> error of 4.85, with an SD of 0.84. On average, the second predictor set is 0.40 WAB points closer
> to the synthetic 12-month outcome under this resampling procedure.
>
> Mean R-squared is 0.81 for the clinical model and 0.82 for the clinical-plus-imaging model. The
> SDs describe variation across the repeated resampling folds. They are not 95% confidence
> intervals, and the table does not establish that any individual imaging variable is causally
> responsible for the difference.

**CHECK:** `cv_summary` contains two rows, with MAE and R-squared reported as mean and SD.

## 0:25-0:36 | Task A3: inspect held-out predictions

**ON SCREEN:** Task A3 prompt.

**SAY:**

> The cross-validation table summarizes average performance. It does not show where predictions
> depart from observations or whether errors cluster in a descriptive subgroup. We therefore make
> one held-out prediction per participant and inspect the errors.
>
> This five-fold out-of-fold display is a diagnostic view, not a second estimate that must equal
> the repeated cross-validation summary from Task A2. The procedures differ.

**DO:** Participants run Task A3. Ask them to identify the identity line in the left panel and one
point that falls far from it.

**SAY, AFTER THE OUTPUT APPEARS:**

> The overall out-of-fold MAE is 4.84 WAB points. Each plotted prediction was generated without
> fitting that participant. The error summary gives 37 synthetic female participants with mean
> absolute error of 4.13 and 53 synthetic male participants with mean absolute error of 5.34.
> Those values are a descriptive audit. They do not establish a subgroup difference, fairness, or
> transportability.

**CHECK:** `oof_pred` has 90 values and the left panel includes the identity line.

## 0:36-0:42 | Task A4: constrain the written result

**ON SCREEN:** `cv_summary`, then the AI chat.

**DO:** Copy the table into the Task A4 prompt. Participants compare the response against the
table before accepting it.

**SAY:**

> The result statement may report the resampled MAE and R-squared values in the displayed table.
> It may state that the clinical-plus-imaging model had lower resampled MAE in this synthetic
> development exercise. It may not claim clinical usefulness, external validation, calibration,
> causal contribution, or readiness for deployment.

**IF THE RESPONSE ADDS A CLAIM:**

> Delete the unsupported clause. Ask the assistant to rewrite using only the displayed table and
> the stated scope of the data.

## 0:42-0:45 | Close

**SAY:**

> The prediction workflow had three dependencies. Predictor timing came first. Resampling then
> protected the performance estimate from training-set optimism. The final prose was restricted to
> the output and to the scope of a synthetic development exercise.
>
> In an actual study, the next requirements would include a prespecified predictor set, an
> appropriate cohort, external evaluation, calibration assessment, and a clinical decision context.

**DO:** Ask participants to write one constraint from their own project that must appear in a
future model prompt, for example the time at which a predictor is measured, the independent unit,
or the required held-out evaluation.

## Optional extension after minute 45

Use Task A5 only when time remains and participants want to inspect a repository with a coding
agent. The agent task is read-only and does not replace the model-development route above.

## Mixed-room version within a 60-minute workshop

Keep the advanced route on the shared display when it serves most participants. Newer participants
work in the core notebook while the advanced group proceeds; do not attempt to narrate two full
analyses at once.

| Minutes | Shared screen and advanced participants | Newer participants |
|---:|---|---|
| 0-5 | Opening, data boundary, and prompt requirements | Same opening |
| 5-12 | Advanced Task A1 | Core Python Task 1: load, inspect, count groups |
| 12-27 | Advanced Task A2 | Core Python Task 3: construct transparent text measures |
| 27-38 | Advanced Task A3 | Core R Task 1: join participant and feature files |
| 38-45 | Advanced Task A4 | Compare their output with the Task 1 checkpoint |
| 45-55 | Advanced close and questions | Core R Task 6 prompt, paired with an advanced participant or facilitator check |
| 55-60 | Whole-room close: identify one design constraint | Same |

For the mixed route, the core participants need not complete every code cell. Their required
outputs are (i) the 60-row, 8-column Python table, (ii) the four transcript measures, and (iii)
the 60-row, 14-column R join. The repeated-measures prompt is the bridge to the whole-room close.
