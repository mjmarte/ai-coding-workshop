# Advanced mixed-effects workshop: 45-minute facilitator script

Use this as the primary route when the room already knows the basic prompt-to-code workflow.
Participants work in Posit Cloud, `r/02_r_starter.R`, and an AI chat. Keep this file,
`r/02_r_solution.R`, and a timer on the private display.

## Before the session

- Share an AI chat, the Posit Cloud project, and `PROMPTS.md`.
- Open `r/02_r_starter.R` in the shared project. Participants make a permanent copy before editing.
- Confirm that `readr`, `dplyr`, `ggplot2`, and `lme4` load, then run `r/02_r_solution.R` once on
  the private display.
- Keep the advanced Colab notebook closed. It is an ML extension after the mixed-effects route,
  not the opening exercise.

The data are synthetic. The route demonstrates how model structure follows the repeated-measures
design; it does not estimate clinical recovery or a treatment effect.

## 0:00-0:05 | Establish the model question

**ON SCREEN:** Posit, `r/02_r_starter.R`, Task 6.

**SAY:**

> The analytic question is whether WAB-AQ differs between acute and chronic observations in the
> same 30 participants. The file has 60 rows, but the independent units are 30 people. The model
> must represent the dependence introduced when each person contributes two observations.
>
> The route proceeds in sequence. We first fit a model that represents participant-level
> dependence. We then fit an ordinary linear model that omits it. Finally, we compare a categorical
> timepoint model with a continuous-time model and identify the assumption each one adds.

**DO:** Ask participants to open the Posit project, select "Save a Permanent Copy," open
`r/02_r_starter.R`, and confirm the `data/` directory exists:

```r
stopifnot(dir.exists("data"))
```

## 0:05-0:14 | Task 6: categorical timepoint model

**ON SCREEN:** Task 6 prompt, then AI chat.

**DO:** Participants copy the complete Task 6 prompt into an AI chat. Before running returned
code, check that it (i) reads the file into `long`, (ii) creates `long_model`, (iii) uses `lmer`,
and (iv) includes `(1 | participant_id)`.

**SAY:**

> The fixed effect for `timepointchronic` estimates the mean chronic-minus-acute WAB-AQ difference.
> The random intercept allows each participant to have a different baseline level. It does not
> assert that every participant follows the same observed trajectory.

**DO:** Paste the returned code below Task 6, select only that code, and run it. The prompt also
creates a participant-trajectory plot.

**SAY, AFTER THE OUTPUT APPEARS:**

> The checked synthetic-data solution estimates a chronic-minus-acute difference of 7.060 WAB
> points, with a standard error of 1.363, a t value of 5.178, and a Wald 95% interval from 4.388 to
> 9.732. The interval describes uncertainty around the mean change represented by this model.
>
> `lme4::lmer` does not return a p value in this output. Do not ask an AI assistant to supply one
> from memory or to convert the t value into a result the model did not report.

## 0:14-0:21 | Compare the independent-rows model

**ON SCREEN:** Posit Console.

**DO:** Run:

```r
summary(lm(wab_aq ~ timepoint, data = long))
```

**SAY:**

> The two models estimate the same mean acute-to-chronic difference because both use the same
> timepoint means. Their uncertainty differs because only the mixed-effects model represents the
> pairing within participant.
>
> Here, the ordinary linear model returns a standard error of about 3.62 and p = .056. The mixed
> model returns a standard error of 1.36. Neither output is interpreted by asking which model is
> more elaborate. The study design determines which dependence structure belongs in the formula.

**ASK:**

> What changed between the two models: the average timepoint difference, or the assumption about
> the 60 records?

**PAUSE, THEN SAY:**

> The assumption about the records. The 60 observations are not measurements from 60 unrelated
> people.

## 0:21-0:31 | Task 6B: continuous time model

**ON SCREEN:** Task 6B prompt.

**SAY:**

> The categorical model estimates one contrast: chronic relative to acute. It does not state what
> occurs during the interval between those visits. We can instead model months since onset as a
> continuous predictor, but that model introduces a new assumption: WAB-AQ changes linearly with
> time over the observed range.

**DO:** Participants copy the Task 6B prompt, paste returned code below its `# YOUR CODE:` line,
and run it. Check that the model is named `month_model` and includes
`wab_aq ~ months_post_onset + (1 | participant_id)`.

**SAY, AFTER THE OUTPUT APPEARS:**

> The continuous-time model estimates an increase of 0.641 WAB points per month, with a Wald 95%
> interval from 0.394 to 0.889. This is a model-based description of these two-visit synthetic
> records. It does not establish that recovery follows a linear monthly course, because the data do
> not observe the intervening months.

**ASK:**

> Which model answers the question, "What is the mean difference between the acute and chronic
> visits?" Which model answers the question, "What linear association with months since onset is
> imposed by the model?"

**PAUSE, THEN SAY:**

> The categorical model answers the first question. The continuous model answers the second.

## 0:31-0:38 | Read the formula as an analysis plan

**ON SCREEN:** AI chat and the two model formulas.

**DO:** Send this prompt:

```text
I have repeated WAB-AQ observations from 30 participants at acute and chronic visits.

Model 1: lmer(wab_aq ~ timepoint + (1 | participant_id), data = long)
Model 2: lmer(wab_aq ~ months_post_onset + (1 | participant_id), data = long)

Explain, in a compact table, the estimand, time assumption, and primary limitation of each model.
Do not choose a model without first stating the research question it answers. Do not infer a p
value that is not in the output.
```

**SAY:**

> Read the answer against the formulas, not against its fluency. The relevant distinction is not
> categorical versus continuous coding in the abstract. It is whether the estimand and time-course
> assumption answer the stated question.

## 0:38-0:43 | Fact-check the result statement

**ON SCREEN:** `summary(long_model)`, `confint(long_model, method = "Wald")`, and AI chat.

**DO:** Copy the output into this prompt:

```text
I fit a linear mixed-effects model of WAB-AQ predicted by timepoint, with a random intercept for
participant ID. Here is the fixed-effect and Wald confidence-interval output:

[PASTE OUTPUT]

Write two Results sentences. Report only values present in the output. State what the timepoint
estimate represents and that the model accounts for repeated observations within participant. Do
not invent a p value, R-squared, F statistic, degrees of freedom, or a treatment effect.
```

**SAY:**

> A suitable statement reports the chronic-minus-acute estimate and its Wald interval, and it
> names the repeated-measures structure. Any added p value, causal language, or treatment claim is
> removed.

## 0:43-0:45 | Close and direct the ML extension

**SAY:**

> The model did not begin with R syntax. It began with the repeated-measures structure. The
> categorical model and continuous-time model then answered different questions because they made
> different assumptions about time.
>
> The optional ML extension applies the same discipline to acute-to-chronic prediction: define the
> time boundary, protect held-out observations during resampling, and restrict the claim to the
> evaluation output.

**DO:** Direct participants who want the extension to [SCRIPT_ML_EXTENSION.md](SCRIPT_ML_EXTENSION.md)
and the advanced recovery-prediction notebook. Ask everyone else to name one design feature from
their own project that must appear in a model prompt.

## Mixed-room version within a 60-minute workshop

Use the mixed-effects route on the shared screen when it serves most participants. Newer
participants complete a small core sequence in parallel; do not attempt two full narrated routes.

| Minutes | Shared screen and advanced participants | Newer participants |
|---:|---|---|
| 0-5 | Repeated-measures question and Posit setup | Same opening and setup |
| 5-14 | R Task 6 categorical mixed model | Core Python Task 1: load, inspect, count groups |
| 14-21 | Compare the ordinary linear model | Core Python Task 3: construct text measures |
| 21-31 | R Task 6B continuous-time mixed model | Core R Task 1: join participant and feature files |
| 31-43 | Formula audit and output-constrained writing | Compare output with the Task 1 checkpoint; begin Task 6 prompt if ready |
| 43-55 | Whole-room fact-check and questions | Join the whole-room fact-check |
| 55-60 | Close: state one design constraint | Same |

The core participants' required outputs are (i) 60 rows and 8 columns after Python loading,
(ii) four text measures added to `df`, and (iii) 60 rows and 14 columns after the R join.
