# The cheat sheet

Print this and keep it. The rest of the workshop is practice applying what's on this page.

---

## 1. The recipe for a prompt that works

An effective prompt functions as a brief, not a request. It has five parts:

| Part | What it does | Example |
|---|---|---|
| **Who you are** | Sets the level of the answer | *"I'm a researcher using R in RStudio. I'm a beginner."* |
| **What the data is** | Stops it inventing columns | *"A CSV at data/x.csv with columns: id, group, age, score"* |
| **The one task** | One thing. Not five. | *"Fit a linear model predicting score from age"* |
| **The constraints** | Keeps it in your world | *"Use dplyr, not base R. Don't install anything new."* |
| **The output you want** | Stops the essay | *"Just the code with short comments. No explanation."* |

Paste in your **actual column names**. Hallucinated variable names arise from the
model guessing at a structure you never showed it.

**Template:**

```
I'm a [role] using [language] in [tool]. I'm a beginner.

My data: [file path], one row per [unit]. Columns:
[paste the actual column names and what they mean]

Task: [one specific thing]

Constraints: [libraries, style, what not to do]

Give me just the code with short comments.
```

---

## 2. The debugging loop

This accounts for roughly 80% of working with these tools. It is the normal
mode of use, not a sign that something has gone wrong.

```
Here is my code:
[paste the WHOLE code block]

Here is the error:
[paste the WHOLE error message, all of it, including the traceback]

I'm running [R 4.4 / Python 3.11] with [package versions if you know them].

What is wrong and how do I fix it?
```

- **Paste the whole error**, not a summary — line numbers and traceback detail matter.
- **Address one error at a time.** Fix, re-run, repeat.
- **Three-strikes rule:** if the same error persists after three attempts, the model
  is likely stuck on a fixed (incorrect) diagnosis. Start a *new chat*, restate the
  goal from scratch, and omit the failed attempts — fresh context outperforms continued
  argument.

---

## 3. Prompts that surface errors the model won't volunteer

This section is the central practical content of the workshop.

| Say this | Because |
|---|---|
| *"What is this code assuming about my data?"* | Surfaces assumptions made silently |
| *"What would make this analysis wrong?"* | The model can identify failure modes but does not raise them unprompted |
| *"Is this the right test? What is it assuming, and does my design meet it?"* | Catches t-tests applied to repeated measures |
| *"Explain what line 7 does, as if to someone who's never coded."* | If the explanation doesn't hold up, the code shouldn't run |
| *"You used a package I don't recognise. Is `[name]` real, and is it on CRAN/PyPI?"* | Hallucinated packages are common |
| *"Rewrite this so a reviewer could reproduce it exactly."* | Forces explicit seeds, versions, and steps |
| *"Give me two different ways to do this and tell me the trade-offs."* | Avoids anchoring on the first plausible answer |

---

## 4. The five most common failure modes, by frequency

1. **Hallucinated functions and packages.** The model calls a nonexistent function,
   e.g. `tidystats::auto_model()`, with full confidence. → *Does this package exist?
   Show me the docs.*
2. **The wrong test for the design.** Repeated measures fed to an independent-samples
   test. The model does not know your design unless told. → **State your design
   explicitly.**
3. **Silent scope errors.** The model fits a model on the full sample when a subgroup
   was intended, drops NAs without reporting it, or filters a different row set than
   specified. → *Print `nrow()` before and after every filter.*
4. **Fabricated numbers in prose.** A requested Results paragraph can contain a df,
   an F, and an R² that appear nowhere in the actual output. → **Check every number
   against the model object, every time.**
5. **Plausible-but-wrong statistical interpretation.** p = .07 described as
   "significant"; a negative coefficient described as a positive effect. → **Read
   the output directly.**

---

## 5. The rules that don't bend

**Never paste real patient data into a chatbot.** This includes transcripts, MRNs,
dates of birth, and "de-identified" text that hasn't been verified as such. Chat
interfaces are not covered by your institution's BAA unless confirmed in writing.
For AI help on real data: **share the schema, not the rows.** Column names, types,
and a fabricated example row are sufficient to get working code.

**Run it, read it, then trust it — in that order.** Code that runs without error
can still answer a different question than the one asked.

**If you can't explain it, you can't publish it.** This is a practical constraint,
not a moral one: you are the person who defends the analysis at committee, in
review, and afterward.

**Disclose AI use.** Journals increasingly require disclosure of AI use in analysis.
One sentence in the methods suffices. Retain the chat log.

---

## 6. Prompts worth stealing

**Starting a new analysis**
> I have [describe the data and design]. My research question is [X]. Before writing any
> code, tell me what analysis approach you'd recommend and what its assumptions are.
> Don't write code yet.

**Understanding inherited code**
> Here's a script I inherited. Walk me through what it does, step by step, in plain
> language. Flag anything that looks like a bug or a questionable choice.

**Making a figure publication-ready**
> Make this ggplot publication-quality: clear axis labels with units, a title, a
> colourblind-safe palette, theme_minimal, and save at 300 dpi. Tell me what you changed.

**The one to end every session with**
> Summarise everything we did in this conversation as a numbered list of the analysis
> steps, so I can paste it into my methods section.

---

## 7. Bad vs. good, side by side

Four real cases from this workshop's dataset. Same question, same model, different
prompt. The gap is not phrasing — it's how much of your own knowledge you put in.

**Case 1 — a two-group comparison**

| | Prompt | What comes back |
|---|---|---|
| Bad | *"Compare word count between my two groups."* | An independent-samples t-test on all 60 rows, controls and patients pooled with no mention of the ceiling effect. |
| Good | *"Compare word count between my two groups. Note: the control group is at ceiling on the severity measure by design — flag if that limits what a group comparison on word count can tell me, and check the variance in each group before choosing a test."* | The model flags the ceiling issue unprompted, checks variance ratios, and recommends a test suited to unequal variance — or recommends restricting the comparison. |

**Case 2 — repeated measures**

| | Prompt | What comes back |
|---|---|---|
| Bad | *"I have 30 patients measured at 1 month and 12 months. Did their scores improve? Give me the R code."* | A paired test roughly half the time; an independent-samples test or unpaired `lm()` the other half — see §4 in `SCRIPT.md` for the live version of this failure. |
| Good | *"I have 30 patients, each measured twice (1 month, 12 months post-stroke) — repeated measures, not independent observations. Fit a model that accounts for the within-person correlation and tell me why a plain two-sample test would be wrong here."* | A mixed-effects or paired approach on the first attempt, with the independence assumption named explicitly instead of surfaced only on follow-up. |

**Case 3 — a multi-predictor model**

| | Prompt | What comes back |
|---|---|---|
| Bad | *"Build a regression predicting severity from my language measures."* | A model with all predictors dumped in, no mention that two of them are collinear, no report of what happens to each one's p-value when the others are added. |
| Good | *"Build a regression predicting severity from these language measures: [list]. Two of these (content-word ratio, word count) are likely correlated with each other. Report each predictor's p-value in the single-predictor model and in the full model side by side, so I can see if anything changes."* | The same fit, but with the vanishing-effect problem (§5 in `STATISTICS_GUARDRAILS.md`) visible in the output instead of buried in it. |

**Case 4 — acute prediction of 12-month outcome**

| | Prompt | What comes back |
|---|---|---|
| Bad | *"Use machine learning to predict 12-month WAB-AQ."* | A model that may use variables collected after the acute assessment, report training performance, or scale the full dataset before cross-validation. |
| Good | *"I want to estimate 12-month WAB-AQ from variables available at the acute assessment only. Define the outcome and predictor sets before modeling. Compare a clinical baseline model with a clinical-plus-imaging model using repeated cross-validation; put imputation, scaling, and model fitting inside each resampling fold. Report MAE and R-squared with their fold-to-fold variability. Do not make clinical or causal claims from this development dataset."* | A time-bounded, leakage-safe evaluation with an interpretation matched to a development exercise rather than a clinical validation study. |

**The pattern.** The AI has the statistical knowledge — it demonstrates that the moment
you ask a follow-up (§3, §4 in `SCRIPT.md`). It does not spend that knowledge unless
your prompt gives it a reason to. **A good prompt is not cleverer wording. It's your
own domain and statistical knowledge, written into the request instead of left in your
head.** The AI can write the code. It cannot supply the part of the question you didn't ask.

---

## 8. Go deeper (the sourced versions of this page)

This page is the one-pager. When you're back on your real research and want the *why*, with
citations, it's all in [`guardrails/`](guardrails/):

- **[AI_CODING_RULES.md](guardrails/AI_CODING_RULES.md)** — how to work with the AI, and the
  evidence behind every rule here.
- **[STATISTICS_GUARDRAILS.md](guardrails/STATISTICS_GUARDRAILS.md)** — the eleven statistical
  traps it walks you into, each with a catch-prompt.
- **[DATA_PRIVACY.md](guardrails/DATA_PRIVACY.md)** — what you may and may not paste, in
  detail.
- **[ANALYSIS_REVIEW_RUBRIC.md](guardrails/ANALYSIS_REVIEW_RUBRIC.md)** — a printable
  scorecard for any AI analysis.
- **[RESEARCH_PROJECT_RULES.md](guardrails/RESEARCH_PROJECT_RULES.md)** — a rules file that
  makes the AI follow all of this itself.
