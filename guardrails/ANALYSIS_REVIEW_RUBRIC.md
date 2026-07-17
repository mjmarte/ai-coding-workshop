# The analysis review rubric

*Run any AI-generated analysis through this checklist before reporting a number. It takes
approximately five minutes.*

Score each item **✓ (pass)**, **✗ (fail)**, or **? (can't tell yet)**. A single **✗** in a
GATE section means **stop** — fix it before anything else. A **?** is a task, not a pass.

---

## GATE 0 — Privacy (if this fails, nothing else matters)

- [ ] No real patient data was pasted into the AI — only **schema + a fabricated row**.
- [ ] If real data was involved, the code was run **locally / in an approved BAA-covered
      tool**, with no consumer chatbot in the loop.
- [ ] No names, dates, MRNs, locations, **voice recordings, or face images** were exposed.

*One ✗ here is a reportable incident, not a bug. See [DATA_PRIVACY.md](DATA_PRIVACY.md).*

---

## GATE 1 — Does it actually run, and do what I asked?

- [ ] It **runs on MY data**, top to bottom in a fresh session — not just on a toy example.
- [ ] All **imports/libraries are included** (the AI often assumes `import pandas`,
      `library(dplyr)` are already there).
- [ ] `n` is **printed before and after every filter, join, and `dropna`** — and the
      numbers are what I expect. No silent scope change.
- [ ] It answers the question I actually asked, not a nearby easier one.
- [ ] It solves the **general** problem, not just my one example row (test it on different
      input).

---

## SECTION A — Are the packages and functions real?

- [ ] Every package it wants to install **exists** on PyPI/CRAN (real project page, recent
      maintenance) — I checked before running `pip install` / `install.packages()`.
- [ ] No function was invented. If I don't recognize one, I asked *"is `[name]` real, show
      me the docs."*

*5–22% of AI-suggested packages do not exist; installing one without verification is a
known malware vector.*

---

## SECTION B — Is the statistics right for MY design? *(the heart of it)*

- [ ] **Unit of analysis** is correct — repeated measurements from one participant are
      **not** treated as independent rows. (Mixed-effects model, not a plain `lm`/t-test,
      for repeated measures.)
- [ ] **No ceiling/floor artifact** — I'm not pooling a group at ceiling with a spread-out
      group and calling the result a correlation.
- [ ] If I'm claiming two groups **differ**, I tested the **difference (interaction)** — not
      two separate p-values eyeballed side by side.
- [ ] **Assumptions** of the test are listed and checked for my data.
- [ ] **Multiple comparisons** are accounted for; my **primary outcome** was named in
      advance.
- [ ] For rehab pre/post: **regression to the mean** and **spontaneous recovery** are ruled
      out or acknowledged.
- [ ] Any length-/count-confounded measure (e.g. type-token ratio) is flagged or replaced.

*Full detail and the catch-prompts: [STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md).*

---

## SECTION C — Is every reported number real?

- [ ] **Every number in any prose/Results paragraph traces to a model object** I can point
      to (`tidy()`, `glance()`, `summary()`, `.summary()`). I regenerated them myself.
- [ ] Degrees of freedom, F, R², and p-values were **read from the output**, not from the
      AI's prose.
- [ ] The **direction** of every effect matches the sign in the output (no flipped sign
      reported as a positive effect).
- [ ] No **p = .07 called "significant"**, no "trend toward significance," no significance
      claimed for a predictor with p > .05.

*An AI-written Results paragraph can be well-composed and contain an invented df in the
same sentence.*

---

## SECTION D — Can I explain it and reproduce it?

- [ ] I can **explain what every line does** in plain language. (If I can't follow the AI's
      own explanation of line 7, I don't run it.)
- [ ] A **seed is set** for anything random (splits, bootstraps, CV, permutations).
- [ ] **Versions/environment** are captured (`sessionInfo()` / `requirements.txt`).
- [ ] Paths are **relative**; it would run on a colleague's machine.
- [ ] The result comes from a **script I can rerun**, not a manual step I'll forget.

---

## Verdict

| Result | Meaning |
|---|---|
| All GATES ✓, Sections mostly ✓ | The analysis has been adequately supervised. |
| Any GATE ✗ | Stop. Fix the gate before continuing. |
| Section B has a ✗ | The statistics are wrong despite the code running without error — the most dangerous case, since nothing signals the failure. |
| Any ? | Not done. Resolve the open question. |

---

### Minimum checklist, one line per section

1. **Privacy:** schema, not rows.
2. **Runs:** on the actual data, with `n` printed around every filter.
3. **Packages:** verified real, checked before install.
4. **Stats:** correct unit of analysis for the design.
5. **Numbers:** every one traced back to the output.
6. **Explain:** if it cannot be explained, it cannot be published.

> Code that runs without error can still answer a different question than the one asked.
> Run it. Read it. Then trust it — in that order.
