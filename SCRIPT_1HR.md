# Coding with AI: 60-minute guided mini-lab

## What this session is

Participants work on their own laptops. You share your primary screen and complete each action first. They then repeat the action in their own three tabs:

1. an AI assistant, e.g., ChatGPT, Claude, or an institutionally approved tool;
2. Google Colab, where they run Python; and
3. Posit Cloud, where they run R.

The AI assistant is a separate tab. Participants copy a prompt from Colab or RStudio into the assistant, then copy the returned code into the relevant coding environment. This is the workflow being taught.

The data are synthetic. No participant should paste real patient data, transcripts, or identifiers into an AI tool.

## Before participants arrive

On the shared screen, have these tabs open in this order:

1. your AI assistant, signed in and in a new conversation;
2. the Colab starter notebook, with the setup cell already run and `Ready.` visible;
3. your Posit permanent copy, with `r/02_r_starter.R` open;
4. `PROMPTS.md` in the GitHub repository.

On your private second screen, open the Python and R solution files, this script, and a 60-minute timer. Do not share this screen.

Before the workshop, verify that `library(readr)`, `library(dplyr)`, `library(ggplot2)`, and `library(lme4)` all load in Posit. If a package does not load, run `r/install_packages.R` in the shared Posit project before participants make their permanent copies.

## Minute-by-minute script

### 0:00-0:05 | Opening and setup check

**ON SCREEN:** Your AI assistant tab, then Colab and Posit tabs. Share your full primary screen, not a single application window.

**SAY:**

> Today is a working session. You will ask an AI assistant for code, run that code yourself, and compare the output against a stated checkpoint. We are using synthetic aphasia data, which is why it is appropriate to place these examples in an AI chat. The same workflow does not authorize placing real participant data, transcripts, or identifiers in a public tool.
>
> You should have three tabs open: an AI assistant, Colab, and Posit Cloud. The assistant writes or explains code. Colab runs Python. Posit runs R. Keep the same AI conversation open as we move through the tasks so that it retains the objects and decisions already established.

**DO:** Ask participants to show a neighbor or raise a hand once (i) Colab prints `Ready.`, and (ii) Posit shows `r/02_r_starter.R`. Give them two minutes. Help only with the first failing step: Colab setup cell, Posit permanent copy, or sign-in.

**SAY:**

> The goal is not to become fluent in Python or R syntax in one hour. The goal is to become specific about what the code must do, then to verify what it did.

### 0:05-0:12 | What the prompt contributes

**ON SCREEN:** AI assistant tab.

**DO:** Type this prompt. Do not ask participants to copy it.

```text
Write code to analyse my aphasia data.
```

**SAY, while the response appears:**

> This request gives the assistant no data structure, no outcome, no unit of observation, no design, and no definition of success. It will fill those omissions with plausible assumptions. The resulting code may be syntactically valid and still be unusable for the question at hand.

**DO:** Open `PROMPTS.md`, section 1, or keep the following five items visible on screen.

**SAY:**

> A useful request has five components: who is asking, what the data contain, one task, the relevant constraints, and the requested output. The point is not ornate language. The point is to state the information that determines the analysis.
>
> Statistical knowledge enters at the same point. A statement that each participant was measured twice is not decoration. It determines whether the observations can be treated as independent. A statement that controls are at ceiling is not decoration. It determines whether a pooled association answers the question of interest.

**SAY:**

> We will now use the first Python prompt exactly as written in the notebook. Copy it, run the returned code, and compare the result to the checkpoint. If your code errors, paste the full error back into the same AI conversation. Do not summarize the error and do not attempt five changes at once.

### 0:12-0:22 | Python Task 1: inspect the data

**ON SCREEN:** Colab starter notebook, Task 1.

**DO:** Scroll to Task 1. Type or paste this exact prompt into the AI assistant:

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

When code returns, point to the request for `df`, dimensions, first rows, and group counts.

**SAY:**

> The prompt specifies one row per person, the exact column names, the meaning of the clinical variable, and the output needed before any model is fitted. The result should therefore be code that creates an object called `df`, not a guessed data set with guessed variable names.

**DO:** Copy the returned code into the empty Colab cell beneath Task 1. Run it with Shift+Enter. Pause while participants do the same.

**SAY, once the output appears:**

> The checkpoint is 60 rows, 8 columns, and 30 participants in each group. Confirm all three before moving on. This is not a ceremonial first step. The later analyses depend on the unit of observation, the available variables, and the group structure being what the prompt said they were.

**IF A PARTICIPANT GETS AN ERROR:**

> Paste the entire error, including the traceback, into the same AI conversation and ask: “This is the full error I received. Identify the immediate cause and give me the smallest correction.” Then run only the correction it provides.

### 0:22-0:30 | Python Task 3: create transparent measures

**ON SCREEN:** Colab Task 3.

**DO:** Type or paste this exact prompt into the same AI conversation. Paste the returned code in the next empty Colab cell and run it.

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

> These measures are intentionally simple. Word count, unique-word count, type-token ratio, and mean word length are transparent operations on the transcript. The AI saves the syntax work, but the construct still needs to be understood. Type-token ratio, for example, changes with transcript length, which limits what it can be taken to represent across speakers who produce very different amounts of language.

**SAY, after the cell runs:**

> The output should add four columns to `df`: `n_words`, `n_unique_words`, `type_token_ratio`, and `mean_word_length`. Check that they are present. If the assistant overwrote `df` or removed earlier variables, tell it explicitly which columns already exist and ask it to add only the requested columns.

### 0:30-0:38 | R Task 1: join precomputed features to the participant data

**ON SCREEN:** Posit Cloud, `r/02_r_starter.R`, Task 1.

**DO:** In the R Console, run the two setup lines at the top of the script if they have not already been run:

```r
stopifnot(dir.exists("data"))
dir.create("outputs", showWarnings = FALSE)
```

**SAY:**

> We are now using R for the statistical half of the workflow. The feature file is already provided, so this section works even if a participant did not finish every Python task. The handoff is deliberate: Python is often useful for text processing; R is often useful for modeling and figures.

**DO:** Type or paste this exact prompt into the same AI conversation. Paste the returned code below `# YOUR CODE:`. Select only the code just pasted, then press Cmd+Enter (Ctrl+Enter on Windows) to run the selection. Do not source the entire script. Pause while participants run it.

```text
I'm a researcher using R in RStudio. I am a beginner. I use the tidyverse.

I have two CSV files:
  data/transcripts.csv - one row per participant. Columns: participant_id,
    group ("control" or "aphasia"), age, sex, education_years,
    months_post_onset, wab_aq (aphasia severity, 0-100, higher = less
    impaired), transcript (what they said describing a picture).
  data/features.csv - one row per participant. Columns: participant_id,
    n_words, n_unique_words, type_token_ratio, mean_word_length,
    content_word_ratio, filler_rate.

Write R code (readr + dplyr) that reads both files, left-joins them by
participant_id into a tibble called `df`, makes `group` a factor with
"control" as the reference level, and then shows me the structure with
glimpse(). Just the code with short comments, no explanation afterwards.
```

**SAY:**

> The checkpoint is 60 rows and 14 columns, with `group` stored as a factor and `control` as the reference level. The code should have joined the two files by `participant_id`. If the number of rows changed, stop there. A join that unexpectedly changes the number of participants requires inspection before any analysis proceeds.

### 0:38-0:50 | R Task 6: repeated measures and the unit of independence

**ON SCREEN:** Posit Task 6. Keep the AI assistant visible long enough for participants to see the exact prompt, then switch back to Posit.

**SAY:**

> The next task contains the central statistical decision in this workshop. The longitudinal file has 60 rows, but it does not contain 60 independent people. It contains 30 people measured twice. The independent unit is the person; the two observations within person are correlated.

**DO:** Type or paste this exact prompt into the same AI conversation. Confirm that the returned code (i) reads the data into an object called `long`, (ii) stores the fitted model as `long_model`, (iii) uses `lmer`, and (iv) includes `(1 | participant_id)`.

```text
Read data/transcripts_long.csv into a data frame named `long`. It has 60 rows: 30 participants
with aphasia, each measured at two timepoints ("acute" and "chronic"). Columns:
participant_id, timepoint, months_post_onset, age, sex, education_years, wab_aq, transcript.

These are repeated measures, so I need a mixed-effects model, not a plain lm. Using lme4, fit
wab_aq predicted by timepoint with a random intercept for participant_id. Store the fitted model
as `long_model`. Include all required library() calls. Make timepoint a factor with "acute" as
the reference. Show me the summary and Wald confidence intervals.

Then make a spaghetti plot: one grey line per participant across the two timepoints, with the
group mean overlaid as a thicker coloured line. Give me only code with short comments.
```

**SAY:**

> Do not run code because it looks technically elaborate. Read the model formula. `wab_aq ~ timepoint` asks whether language score changes across time. `(1 | participant_id)` tells the model that each participant contributes a pair of observations rather than two unrelated records.

**DO:** Paste the returned code below Task 6. Select only the code just pasted, then press Cmd+Enter (Ctrl+Enter on Windows) to run the selection. Do not source the entire script. Pause while participants do the same.

**SAY, once the model summary appears:**

> The fixed effect for chronic relative to acute assessment should be about 7.06 WAB points, with a t value of about 5.18 and a 95% interval from about 4.39 to 9.73. The estimated mean change is therefore positive, and the interval excludes zero.

**DO:** In the Console, run the deliberately wrong model:

```r
summary(lm(wab_aq ~ timepoint, data = long))
```

**SAY, once the output appears:**

> Both models estimate the same average change, about 7.06 WAB points. The difference is the uncertainty assigned to that estimate. The ordinary linear model treats the 60 rows as unrelated observations, placing stable differences between participants into the residual error. Its standard error is about 3.62 and its p value is .056, which is marginal.
>
> The mixed-effects model incorporates the pairing through participant ID. Its standard error is about 1.36, and its 95% interval for the mean change excludes zero. The model choice therefore changes the conclusion because the study design changes the information available to the analysis.
>
> The assistant can write both models. It cannot infer the repeated-measures structure from a generic request. The design must be stated in the prompt and checked in the model formula.

**ASK THE ROOM:**

> What is the independent unit in this analysis: 60 rows, or 30 people?

**PAUSE, THEN SAY:**

> Thirty people.

### 0:50-0:56 | Fact-check the output the model actually produced

**ON SCREEN:** Posit Console with the mixed-model output, then AI assistant.

**DO:** Copy the following prompt into the AI assistant. Before sending it, paste the actual fixed-effect rows and the Wald confidence interval from the `summary(long_model)` and `confint(long_model, method = "Wald")` output. Replace the bracketed section with the copied output.

```text
I fit a linear mixed-effects model of WAB-AQ predicted by timepoint, with a random intercept for participant ID. Here is the relevant output:

[PASTE THE FIXED-EFFECT AND CONFIDENCE-INTERVAL OUTPUT HERE]

Write a two-sentence Results statement. Report only values present in the output. Do not invent a p value, R-squared, F statistic, or degrees of freedom. State that the model accounts for repeated measurements within participant.
```

**SAY:**

> The model has now been given the values it is allowed to report. The verification task is not to assume that the paragraph is false. It is to establish whether every number and every claim can be traced to the visible output.

**DO:** Read the AI response line by line against the Console. Ask participants to identify each of the following: the timepoint estimate, its confidence interval, the t value, and the statement about repeated measurements.

**SAY:**

> A fluent paragraph is not evidence. The model output is evidence. If a value is not in the output, it does not enter the Results section.

### 0:56-1:00 | Close

**ON SCREEN:** `PROMPTS.md`, then the `guardrails/` folder.

**SAY:**

> The transferable workflow is short. State the data structure and study design. Ask for one analytic task. Run the code. Inspect the output. Compare the written result against the output that generated it.
>
> Two rules remain fixed. First, do not place real patient data in a chatbot unless institutional approval and the applicable data agreement explicitly permit it. Share the schema, not the rows. Second, if you cannot identify what the model did and why it was appropriate, the result is not ready to report.
>
> Agents and reusable project rules can make multi-step work faster. They do not remove the need to specify the design or verify the analysis. The person whose name appears on the abstract remains responsible for both.

**DO:** Take questions.

## If the timing slips

- Do not cut R Task 6. It provides the clearest demonstration of why research design must enter the prompt.
- Cut Python Task 3 before cutting R Task 6. Show the pre-run Python solution if needed.
- Do not ask participants to install packages during the session. Keep a pre-run Posit solution open as your fallback.
- If the AI returns code with an error, demonstrate the full-error debugging loop once, then move on. Do not let one machine consume the session.
