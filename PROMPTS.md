# The cheat sheet

Print this. Keep it. Everything else in the workshop is practice for what's on this page.

---

## 1. The recipe for a prompt that works

A bad prompt is a wish. A good prompt is a **brief**. Five parts:

| Part | What it does | Example |
|---|---|---|
| **Who you are** | Sets the level of the answer | *"I'm a researcher using R in RStudio. I'm a beginner."* |
| **What the data is** | Stops it inventing columns | *"A CSV at data/x.csv with columns: id, group, age, score"* |
| **The one task** | One thing. Not five. | *"Fit a linear model predicting score from age"* |
| **The constraints** | Keeps it in your world | *"Use dplyr, not base R. Don't install anything new."* |
| **The output you want** | Stops the essay | *"Just the code with short comments. No explanation."* |

Paste in your **actual column names**. Every hallucinated variable name traces
back to an AI guessing at a structure you never showed it.

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

This is 80% of using these tools. It is not a failure state. It is the normal state.

```
Here is my code:
[paste the WHOLE code block]

Here is the error:
[paste the WHOLE error message, all of it, including the traceback]

I'm running [R 4.4 / Python 3.11] with [package versions if you know them].

What is wrong and how do I fix it?
```

- **Paste the whole error.** Not your summary of it. The line numbers matter.
- **One error at a time.** Fix, re-run, repeat.
- **Three strikes rule:** if it fails three times on the same error, it is stuck in a
  groove. Start a *new chat*, describe the goal from scratch, and don't paste the
  failed attempts. Fresh context beats more argument.

---

## 3. Prompts that catch it lying to you

The whole workshop is really about this section.

| Say this | Because |
|---|---|
| *"What is this code assuming about my data?"* | Surfaces the assumptions it silently made |
| *"What would make this analysis wrong?"* | It knows. It just doesn't volunteer. |
| *"Is this the right test? What is it assuming, and does my design meet it?"* | Catches t-tests on repeated measures |
| *"Explain what line 7 does, as if to someone who's never coded."* | If you can't follow the explanation, don't run the code |
| *"You used a package I don't recognise. Is `[name]` real, and is it on CRAN/PyPI?"* | Hallucinated packages are extremely common |
| *"Rewrite this so a reviewer could reproduce it exactly."* | Forces seeds, versions, explicit steps |
| *"Give me two different ways to do this and tell me the trade-offs."* | Breaks it out of the first plausible answer |

---

## 4. The five things it gets wrong, in order of how often

1. **Hallucinated functions and packages.** Confidently calls `tidystats::auto_model()`.
   No such thing. → *Does this package exist? Show me the docs.*
2. **The wrong test for your design.** Repeated measures fed to an independent-samples
   test. It does not know your design unless you tell it. → **Tell it your design.**
3. **Silent scope errors.** It models everyone when you meant a subgroup, drops NAs
   without saying so, or filters a row set you didn't intend.
   → *Print `nrow()` before and after every filter.*
4. **Made-up numbers in prose.** Ask for a Results paragraph and it will produce
   beautiful APA prose containing a df, an F, and an R² that appear nowhere in your
   output. → **Check every number against the model object. Every time.**
5. **Plausible-but-wrong statistics.** p = .07 described as "significant". A negative
   coefficient described as a positive effect. → **Read the output yourself.**

---

## 5. The rules that don't bend

**Never paste real patient data into a chatbot.** Not transcripts, not MRNs, not dates
of birth, not "de-identified" text you haven't actually checked. Chat interfaces are not
covered by your institution's BAA unless someone has told you in writing that they are.
When you want AI help on real data: **share the schema, not the rows.** Column names,
types, and a fabricated example row are enough to get working code.

**Run it. Read it. Then trust it.** In that order. Code that runs without error can
still be answering a different question than the one you asked.

**If you can't explain it, you can't publish it.** Not a moral point, a practical one:
you are the person who has to defend it at your committee, in review, and in your own
head at 2am.

**Say what you did.** Journals increasingly require disclosure of AI use in analysis.
One sentence in the methods. Keep the chat log.

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

## 7. Go deeper (the sourced versions of this page)

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
