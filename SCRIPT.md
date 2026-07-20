# Expanded facilitator notes

Use [SCRIPT_1HR.md](SCRIPT_1HR.md) as the live, word-for-word script. This file supplies
the analytic rationale, fallback language, and route decisions that do not belong on a
participant-facing slide or in a spoken prompt.

## What the workshop establishes

The workshop does not establish that one AI system is reliable or unreliable in general. It
demonstrates a reproducible workflow on synthetic data: specify the data structure, request a
defined operation, run the returned code, and check the output against the intended analysis.

Each teaching point has a local source:

| Teaching point | Source in this repository |
|---|---|
| One record per participant; 60 records, two groups | `data/transcripts.csv` and Python Task 1 |
| Transparent transcript measures | Python Task 3 and `data/features.csv` |
| Repeated observations within participant | `data/transcripts_long.csv` and R Task 6 |
| Correct and incorrect uncertainty estimates | `r/02_r_solution.R`, `summary(long_model)`, and the deliberate `lm()` comparison |
| Resampled development-model comparison | `python/02_advanced_recovery_solution.ipynb` |

Do not generalize a result from these constructed data to clinical aphasia, clinical prediction,
or a particular commercial model.

## Core instructional sequence

The hour follows one argument. A prompt cannot substitute for study design. The participant
therefore provides the design information, checks that the code encodes it, and traces the
written interpretation to the resulting output.

### Prompt specification

The first prompt is intentionally underspecified. Do not characterize the returned answer as a
failure. Say:

> The request leaves the unit of observation, variable names, outcome, and analytic target
> unspecified. The response must choose among several possibilities. We will now provide the
> information that determines the operation.

The five elements in `PROMPTS.md` are a practical checklist, not a prompt formula that
guarantees correct code. The checkpoint remains necessary.

### Transcript measures

Python Task 3 introduces four operations: word count, unique-word count, type-token ratio, and
mean word length. Say:

> The code defines quantities; it does not establish that each quantity is a valid construct for
> a clinical question. Here, type-token ratio changes with transcript length. We inspect that
> limitation before deciding what the measure represents.

Do not call the measures "NLP" without specifying the operation. They are deterministic counts
on tokenized text.

### Repeated measures

R Task 6 is the primary statistical demonstration. Say:

> The longitudinal file contains 60 records from 30 participants. The repeated records belong to
> the same people, so the model must encode participant-level dependence. In this exercise, the
> random intercept supplies that structure.

The correct model and deliberately incorrect model estimate the same mean acute-to-chronic
change. Their standard errors differ because they use different assumptions about the two records
per participant. The values used in the live script derive from the checked R solution.

### Fact-checking a result paragraph

The AI receives copied model output, not a request to recover statistics from memory. Say:

> A results sentence is acceptable only when each numerical statement and each description of
> the model can be located in the output or in the code that produced it.

If the assistant supplies a value not in the displayed output, remove it. If it uses a metric not
returned by the model, ask it to revise the paragraph without that metric.

## Route selection

At minute 5, choose one route using [ADVANCED_PATHS.md](ADVANCED_PATHS.md).

- **Core route:** participants need practice moving from a prompt to executable Python and R.
- **Experienced-room route:** participants already manage basic prompting and coding. Use the
  recovery-prediction notebook, which moves the emphasis to predictor timing, preprocessing
  inside resampling, out-of-fold error, and bounded interpretation.
- **Mixed room:** the shared screen uses the core route. Participants who move ahead work through
  one advanced task and return with one output or one question.

Do not run both routes in one hour.

## Advanced recovery-prediction language

The advanced notebook uses a constructed acute-to-12-month cohort. Say:

> We will compare two predictor sets using data that are available at the acute assessment. The
> 12-month score is the outcome. The exercise tests whether the code preserves this time order and
> evaluates prediction on held-out folds. It does not estimate clinical utility or establish a
> causal contribution of any predictor.

When `cv_summary` appears, use only the reported mean and SD values. A lower resampled mean
absolute error identifies the better-performing model in this synthetic development exercise. It
does not demonstrate transportability to another hospital, calibration for clinical decisions, or
benefit from using the model.

## Agents

The advanced agent task is deliberately read-only. An agent can inventory inputs, code paths, and
stated risks. It cannot decide whether the predictor set answers the clinical question, whether a
resampling design is sufficient, or whether an interpretation is warranted. Participants verify
its file citations before using the inventory.

## When a machine fails

Address the first failure that prevents progress.

1. Confirm the setup cell completed and the expected file exists.
2. Copy the complete error into the same AI conversation.
3. Request the smallest correction and run only that correction.
4. After one unsuccessful repair, use the solution notebook or script to restore the room.

Do not diagnose a participant's environment in front of the whole room for more than two minutes.
The exercise is the workflow, not one participant's installation.

## What not to claim

- Do not claim that an assistant "knew" a better model but withheld it.
- Do not promise that any prompt will produce correct code.
- Do not describe the synthetic classifier or recovery model as clinically validated.
- Do not describe a non-significant comparison as proof of no effect.
- Do not use real patient data, transcripts, or identifiers in a public AI service. Institutional
  approval, the applicable agreement, and the approved tool determine what is permitted for real
  data.

## Close

Use the close in `SCRIPT_1HR.md`. If additional time remains, ask participants to name (i) the
unit of observation in their own current project, (ii) one variable that cannot enter a model at
their chosen time point, and (iii) the output they would need before writing a result sentence.
