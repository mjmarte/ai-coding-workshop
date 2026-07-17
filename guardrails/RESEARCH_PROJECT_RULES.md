# A rules file for your own research project

*A project rules file gives the AI standing instructions it reads before every response,
shifting some of the self-checking burden onto the tool itself.*

Modern AI coding tools read a project rules file automatically:

- **Claude Code** → save it as `CLAUDE.md` in your project root.
- **Cursor** → save it as `.cursorrules` (or a `.mdc` file under `.cursor/rules/`).
- **GitHub Copilot** → `.github/copilot-instructions.md`.
- **Plain chat (ChatGPT/Claude web)** → paste it as your **first message** in a new
  analysis chat, then work below it. (Or save it as a Claude Project / Custom GPT
  instruction so it applies every time.)

**Keep it short.** Anthropic's stated test for each line: would removing this cause the AI
to make a mistake? If not, cut it. An overlong rules file tends to be ignored. The
template below is deliberately lean and research-specific, stating only what a general
model would not already know about the work. Adapt the bracketed parts and delete what
does not apply.

---

## Copy from here ↓

```markdown
# Project rules — [your study name]

You are helping a researcher who is a beginner programmer. Follow these rules in every
response. When a rule conflicts with what I asked, follow the rule and tell me why.

## About this project
- Field: neuro / rehabilitation research. Language: [R 4.x / Python 3.11].
- Data: one row per [participant / observation]. Key columns: [id, group, timepoint,
  outcome, ...]. NEVER invent column names — if you need one I haven't given you, ask.
- Design: [e.g. 30 participants, each measured at 2 timepoints — these are REPEATED
  MEASURES; the unit of analysis is the participant, not the row].

## How to write code for me
- Always give **runnable code with all imports/libraries included**. Never assume a library
  is already loaded.
- Keep it **simple**: only do what I asked; no extra files or abstractions I didn't request.
- Add **short comments** explaining each step in plain language.
- Prefer [tidyverse / pandas]; do not introduce a new package without telling me and
  confirming it exists on [CRAN / PyPI]. **Ask before any install.**
- After any filter, join, or dropped-NA step, **print the row count before and after.**
- Set a **random seed** for anything stochastic (splits, bootstraps, cross-validation).

## Statistics discipline (this is where I need you most)
- Before recommending a test, state its **assumptions** and whether my design meets them.
- For repeated measures / multiple observations per participant, use a **mixed-effects
  model** (random intercept per participant), never a plain lm/t-test that treats rows as
  independent.
- If a group is at a **ceiling or floor** on the outcome, warn me before pooling it into a
  correlation.
- If I claim two groups **differ**, test the **interaction**, not two separate p-values.
- Flag **multiple comparisons**, **regression to the mean** (pre/post rehab data), and any
  **length-/count-confounded** language measure (e.g. type-token ratio).
- **Never state a statistic (p, F, df, R², CI) in prose.** Give me code that prints it from
  the model object, so I read the real number myself.

## Data privacy — hard rule
- This chat may contain only **synthetic or schema-level** data. If I ever paste something
  that looks like real patient data (names, dates, MRNs, transcripts, recordings), **stop
  and warn me** instead of proceeding.

## When you're unsure
- Say so. A hedge I can check beats a confident answer I can't. If you're guessing about my
  data or design, ask me rather than assuming.
```

## ↑ Copy to here

---

### Rationale for each block

- **"About this project" / never invent columns** — hallucinated column names are a
  leading source of code that runs correctly on data that does not exist. Pinning the
  schema addresses this at the source.
- **"print the row count before and after"** — makes silent scope errors (a model fit on
  47 of 60 rows) visible rather than invisible.
- **"Never state a statistic in prose"** — pre-empts the fabricated-Results-paragraph
  failure: an invented p-value cannot be handed over if the AI is instructed to print only
  real ones.
- **The statistics block** compresses [STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md)
  into instructions the AI applies before the error needs to be caught downstream.
- **The privacy rule** gives the assistant a role in preventing a career-ending data
  disclosure.

A rules file does not substitute for the [review rubric](ANALYSIS_REVIEW_RUBRIC.md); it
improves the AI's first draft, but the result still requires verification.
