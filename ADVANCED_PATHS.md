# Advanced workshop routes

The acute-to-chronic recovery-prediction route is the primary option for a room that already
uses AI to write and run research code. Its complete 45-minute facilitator script is
[SCRIPT_ADVANCED_45.md](SCRIPT_ADVANCED_45.md). The shorter branches below are alternatives,
not material to compress into the same session.

## Make the route decision at minute 5

Ask: "Have you already used an AI assistant to write and run R or Python code for your own
research?"

- If most hands are down, use the core route in [SCRIPT_1HR.md](SCRIPT_1HR.md).
- If most hands are up, use [SCRIPT_ADVANCED_45.md](SCRIPT_ADVANCED_45.md). It includes Tasks A1
  through A4, with predictor timing, resampling, held-out predictions, and output-constrained
  writing.
- If experience is mixed, use the mixed-room table in `SCRIPT_ADVANCED_45.md`. The advanced route
  remains on the shared screen; newer participants complete the specified core checkpoints.

In an experienced room, all participants follow the advanced notebook. Do not divide the shared
screen between two full analyses.

## Branch A: narrative discourse and automated measurement

**Use when:** the room works with transcripts, discourse, naturalistic language samples, or
automated scoring.

**Open:** [Python Task 7](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/01_python_starter.ipynb), then scroll to “Narrative-content proxy against a reference description.”

Say:

> This task calculates TF-IDF overlap with one reference description. Each operation is inspectable. It is not a validated main-concept analysis, an embedding model, or a substitute for a human scoring protocol.

**Ask participants to do:** run Task 7, then ask the AI:

```text
List three reasons this lexical-overlap score could disagree with clinician-scored main concepts.
For each reason, state whether it is a measurement limitation, a reference-text limitation, or
a property of the transcript. Do not propose a clinical interpretation from this synthetic data.
```

Debrief question: "What would need to be specified before this became a defensible outcome
measure in a study?"

Expected answers: scoring target, reference set, preprocessing decisions, human benchmark,
reliability, validation sample, and the population in which it will be used.

## Branch B: acute prediction of 12-month language outcome

**Use when:** the room already understands basic R/Python prompting and wants a model-development
exercise.

**Open:** [advanced recovery-prediction notebook](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/02_advanced_recovery_starter.ipynb).

Say:

> The synthetic cohort defines an acute-to-chronic prediction question. Only variables available
> at the acute assessment enter the predictor matrix. The 12-month WAB-AQ is the outcome.

Use [SCRIPT_ADVANCED_45.md](SCRIPT_ADVANCED_45.md), which runs Tasks A1 through A4 in sequence.

Debrief question: "What does a lower cross-validated mean absolute error establish here, and
what does it not establish?"

Answer: It indicates lower error under the specified resampling procedure in this synthetic
development dataset. It does not establish external validity, calibration in a new hospital,
clinical usefulness, or a causal contribution of an imaging feature.

**Advanced fact-check prompt:**

```text
Here is my cross-validation summary table:

[PASTE cv_summary HERE]

Write two Results sentences for a synthetic model-development exercise. Report only numbers in
the table. State which model had lower resampled MAE. Do not call the model clinically useful,
externally validated, calibrated, causal, or ready for deployment.
```

Read the response against `cv_summary`. If it adds a claim beyond the table or beyond a
synthetic development exercise, remove it.

## Branch C: agents for a bounded project audit

**Use when:** participants already code independently and want to see a bounded use of Codex or a
similar coding agent.

**Open:** Task A5 in the advanced recovery notebook.

Say:

> The agent receives an inspection task and no authority to edit data, run analysis, or make
> clinical claims. Its output is an inventory that requires file-level checking.

**Do:** Paste the Task A5 prompt into Codex with the workshop repository open. Read the returned
table against the files it cites. Ask the room to identify one place where the agent’s response
must be checked by a person.

For a discourse-focused room, use Branch A followed by Python Task 8 and the final output
fact-check. Do not merge that route with the recovery-prediction script.
