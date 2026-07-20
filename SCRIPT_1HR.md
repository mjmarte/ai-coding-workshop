# Coding with AI: one-hour guided mini-lab

Participants work on their own laptops. They use three tabs: an AI assistant, Google Colab for
Python, and Posit Cloud for R. You share the primary display. Keep this file, the solution files,
and a timer on the private display.

The core route below is for participants new to AI-assisted coding. At minute 5, move an
experienced room to [ADVANCED_PATHS.md](ADVANCED_PATHS.md). Do not attempt both routes in one
hour.

## Before participants arrive

- Open a new AI conversation, the core Colab notebook, the shared Posit project, and `PROMPTS.md`
  on the shared display.
- Run the Colab setup cell. Confirm `Ready.`.
- Open `r/02_r_starter.R` in Posit and confirm the required packages load.
- On the private display, open `python/01_python_solution.ipynb`, `r/02_r_solution.R`, and this
  script.
- Confirm the public Colab link and the Posit permanent-copy flow after the final repository push.

The data are synthetic. Do not treat this workshop as permission to enter real participant data,
transcripts, or identifiers into an AI service.

## 0:00-0:05 | Establish the working environment

**ON SCREEN:** AI assistant, Colab, then Posit.

**SAY:**

> This is a working session. You will specify an analytic task, ask an AI assistant for code, run
> that code, and compare the result with a checkpoint. The assistant is a separate tab. Colab
> executes Python. Posit executes R.
>
> The relevant skill is not memorizing syntax. It is specifying the data and design well enough
> that the code can be checked against the question it is meant to answer.
>
> Raise your hand if you have already used an AI assistant to write and run R or Python code for a
> research analysis.

**DO:** If most participants raise a hand, open `ADVANCED_PATHS.md` and use the experienced-room
route. Otherwise continue. Ask everyone to confirm that Colab displays `Ready.` and Posit displays
`r/02_r_starter.R`.

## 0:05-0:10 | Specify the request

**ON SCREEN:** AI assistant.

**DO:** Type, but do not send participants this prompt:

```text
Write code to analyse my aphasia data.
```

**SAY:**

> This request does not identify the file, the rows, the outcome, the design, or the required
> output. The assistant must supply those details itself. We will instead state the details that
> determine the analysis.

**ON SCREEN:** `PROMPTS.md`, first table.

**SAY:**

> A usable request names the environment, the unit of observation, the files and variables, one
> analytic task, the design constraints, and the expected return. This is an analysis
> specification, not a guarantee that the returned code is correct. The checkpoint remains part
> of the work.

## 0:10-0:20 | Python Task 1: inspect the participant data

**ON SCREEN:** Colab, Task 1.

**DO:** Paste this into the AI assistant, then copy the returned code into the empty cell below
Task 1. Run the cell with Shift+Enter. Pause while participants repeat the process.

```text
I'm a researcher using Python in a Google Colab notebook. I am a beginner.

I have a CSV file at `data/transcripts.csv` with these columns:
participant_id, group, age, sex, education_years, months_post_onset, wab_aq, transcript

Each row is one person describing a picture out loud. `group` is either "control" or
"aphasia". `wab_aq` is an aphasia severity score from 0-100 (higher = less impaired).
`transcript` is what they said.

Write Python using pandas to:
1. load the file into a DataFrame called `df`
2. print how many rows and columns it has
3. show the first 3 rows
4. count how many people are in each group

Give me just the code, with short comments. Don't explain it afterwards.
```

**SAY:**

> The checkpoint is 60 rows, 8 columns, and 30 participants in each group. Confirm those values
> before proceeding. They establish the available variables, the unit of observation, and the
> group structure used in later tasks.

**IF CODE ERRORS:**

> Paste the complete error and traceback into the same conversation. Ask for the immediate cause
> and the smallest correction. Run the correction before requesting another change.

## 0:20-0:28 | Python Task 3: construct transparent transcript measures

**ON SCREEN:** Colab, Task 3.

**DO:** Send the prompt below. Paste the returned code into the next empty cell and run it.

```text
Add four new columns to `df`, one row per participant, computed from the `transcript` column:
- `n_words`: total number of words
- `n_unique_words`: number of unique words
- `type_token_ratio`: n_unique_words / n_words
- `mean_word_length`: average number of characters per word

Lowercase the text and strip periods before splitting on whitespace. Use a function plus
`.apply()` so the steps are readable. Then show me participant_id, group, wab_aq, n_words, and
type_token_ratio for the first 5 rows.
```

**SAY:**

> These are defined operations on text. The code calculates them; it does not establish what each
> quantity represents clinically. Type-token ratio, for example, depends on transcript length.
> Any interpretation therefore requires attention to how much language each person produced.

**SAY, AFTER THE CELL RUNS:**

> Confirm that `df` now contains the four requested columns. If the assistant replaced `df` or
> removed earlier variables, specify the existing columns and ask it to add only the requested
> measures.

## 0:28-0:36 | R Task 1: join features to participant records

**ON SCREEN:** Posit, `r/02_r_starter.R`, Task 1.

**DO:** Run these lines in the Console if they have not already been run:

```r
stopifnot(dir.exists("data"))
dir.create("outputs", showWarnings = FALSE)
```

Then send the Task 1 prompt from the R script. Paste the returned code below `# YOUR CODE:`.
Select only that code and press Cmd+Enter or Ctrl+Enter. Do not source the entire script.

**SAY:**

> The feature file is provided so that the R analysis does not depend on every Python task being
> completed. The join should preserve one record per participant. The checkpoint is 60 rows and
> 14 columns, with `group` stored as a factor whose reference level is `control`. If the row count
> changes, inspect the join before fitting a model.

## 0:36-0:50 | R Task 6: encode repeated observations

**ON SCREEN:** Posit, Task 6. Keep the prompt visible in the AI tab briefly, then return to Posit.

**SAY:**

> The longitudinal file contains 60 records from 30 participants. Each participant contributes an
> acute and a chronic observation. The model must represent that dependence rather than treating
> the two records as unrelated people.

**DO:** Send the Task 6 prompt from the R script. Check that the returned code (i) reads the data
into `long`, (ii) creates `long_model`, (iii) uses `lmer`, and (iv) includes
`(1 | participant_id)`. Paste the code below Task 6, select only the pasted code, and run it.

**SAY, AFTER THE MODEL RUNS:**

> The checked solution estimates a chronic-minus-acute change of 7.060 WAB points, with a t value
> of 5.178 and a Wald 95% interval from 4.388 to 9.732. The estimate is positive, and this
> interval excludes zero.

**DO:** Run the deliberately inappropriate comparison in the Console:

```r
summary(lm(wab_aq ~ timepoint, data = long))
```

**SAY:**

> Both models estimate the same mean change because they use the same group means. Their
> uncertainty differs. The ordinary linear model treats the 60 records as unrelated and returns a
> standard error near 3.62 with p = .056. The mixed model uses the participant pairing, returns a
> standard error near 1.36, and yields the interval we just examined.
>
> The question is not which model appears more sophisticated. The question is whether the formula
> represents the data-generating structure that the study design specifies.

**ASK:**

> What is the independent unit here: 60 records or 30 participants?

**PAUSE, THEN SAY:**

> Thirty participants.

## 0:50-0:56 | Verify an AI-written result statement

**ON SCREEN:** Posit Console and AI assistant.

**DO:** Copy the fixed-effect and Wald interval output from `summary(long_model)` and
`confint(long_model, method = "Wald")`. Insert it into this prompt:

```text
I fit a linear mixed-effects model of WAB-AQ predicted by timepoint, with a random intercept for
participant ID. Here is the relevant output:

[PASTE THE FIXED-EFFECT AND CONFIDENCE-INTERVAL OUTPUT HERE]

Write a two-sentence Results statement. Report only values present in the output. Do not invent a
p value, R-squared, F statistic, or degrees of freedom. State that the model accounts for repeated
measurements within participant.
```

**SAY:**

> Check the response line by line. Locate the timepoint estimate, confidence interval, t value,
> and model description in the displayed output or code. Delete any value or claim that cannot be
> located.

## 0:56-1:00 | Close

**ON SCREEN:** `PROMPTS.md` and the `guardrails/` folder.

**SAY:**

> The workflow is concise: specify the data and design, request one analytic operation, run the
> code, inspect the output, and trace the written interpretation to that output.
>
> For real research data, the approved service and data agreement determine what may be shared.
> For every result, the investigator remains responsible for the code, the model, and the written
> claim.

**DO:** Take questions.

## If timing changes

- Remove Python Task 3 before removing the output-verification exercise.
- Use `r/02_r_solution.R` to restore the room after an R error. Do not source it as a participant
  exercise.
- If most participants are already comfortable with the core workflow, use the experienced-room
  route in `ADVANCED_PATHS.md` rather than accelerating through both Python and R tasks.
