# Advanced paths: choose one when the room moves quickly

The core one-hour route is for participants new to AI-assisted research coding. Do not run
every advanced task in the same hour. Choose one branch after the opening prompt exercise.

## Make the route decision at minute 5

Ask: “Have you already used an AI assistant to write and run R or Python code for your own
research?”

- If most hands are down, use the core route in [SCRIPT_1HR.md](SCRIPT_1HR.md).
- If most hands are up, use an advanced branch as the shared-screen route. The recovery-prediction
  branch replaces the basic R sequence; it retains explicit checks for leakage, resampling, and
  interpretation.
- If experience is mixed, demonstrate the core task once, then let experienced participants use
  an advanced notebook while you help newer participants complete the core task.

In a mixed room, the shared screen follows the core route and experienced participants work
independently from the prompts below. In an experienced room, the facilitator shares the
selected branch and the whole room follows it.

## Branch A: narrative discourse and automated measurement

**Use when:** the room works with transcripts, discourse, naturalistic language samples, or
automated scoring.

**Open:** [Python Task 7](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/01_python_starter.ipynb), then scroll to “Narrative-content proxy against a reference description.”

**Say:**

> We are moving from counts to a content-sensitive measure. This is TF-IDF overlap with one reference description. It is useful because every operation is inspectable. It is not a validated main-concept analysis, an embedding model, or a substitute for a human scoring protocol.

**Ask participants to do:** run Task 7, then ask the AI:

```text
List three reasons this lexical-overlap score could disagree with clinician-scored main concepts.
For each reason, state whether it is a measurement limitation, a reference-text limitation, or
a property of the transcript. Do not propose a clinical interpretation from this synthetic data.
```

**Debrief question:** “What would have to be specified before this became a defensible outcome
measure in a study?”

Expected answers: scoring target, reference set, preprocessing decisions, human benchmark,
reliability, validation sample, and the population in which it will be used.

## Branch B: acute prediction of 12-month language outcome

**Use when:** the room already understands basic R/Python prompting and wants an applied model
development exercise.

**Open:** [advanced recovery-prediction notebook](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/02_advanced_recovery_starter.ipynb).

**Say:**

> This synthetic cohort resembles an acute-to-chronic recovery question. The model may use only variables available during the acute assessment. The 12-month WAB-AQ is the outcome. The first error to prevent is temporal leakage: placing a later variable in the predictor matrix.

Run Tasks A1 and A2. If time remains, run A3.

**Debrief question:** “What does a lower cross-validated mean absolute error establish here, and
what does it not establish?”

**Answer:** It establishes better resampled performance in this synthetic development dataset.
It does not establish external validity, calibration in a new hospital, clinical usefulness,
or a causal contribution of an imaging feature.

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

**Use when:** participants already code independently and want to see a safe use of Codex or a
similar coding agent.

**Open:** Task A5 in the advanced recovery notebook.

**Say:**

> The agent receives a defined inspection task and no authority to edit data, run analysis, or make clinical claims. Its output is an inventory for us to check, not a decision made on our behalf.

**Do:** Paste the Task A5 prompt into Codex with the workshop repository open. Read the returned
table against the files it cites. Ask the room to identify one place where the agent’s response
must be checked by a person.

## Time box for the experienced-room fast-track route

| Minutes | Shared screen | Advanced participants |
|---:|---|---|
| 0-10 | Opening and prompt-quality demonstration | Same |
| 10-18 | Advanced notebook Task A1 | Identify the time boundary and predictor sets |
| 18-38 | Advanced notebook Task A2 | Compare the two resampled models |
| 38-50 | Advanced notebook Task A3 | Inspect out-of-fold predictions and error |
| 50-56 | Advanced fact-check prompt below | Match every claim to `cv_summary` |
| 56-60 | Close | Report one constraint they added to a prompt |

For a discourse-focused room, replace Tasks A1-A3 with Python Task 7, the Branch A follow-up
prompt, and Task 8. Retain the final output fact-check.
