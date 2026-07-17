# Working with an AI coding assistant: the rules

*Extended version of [PROMPTS.md](../PROMPTS.md), with the supporting evidence for each
rule.*

---

## The central finding

In a controlled study at Stanford (47 participants, real security tasks, Python/JS/C),
participants **with** an AI assistant wrote **less secure** code than those without one,
and were **more likely to believe their code was secure.** Participants who trusted the AI
least and refined their prompts most performed best.

The risk is not that the AI is occasionally wrong — that is catchable. The risk is that
wrong output is delivered with the same confidence as correct output. For a researcher who
cannot yet read the code fluently, that confidence gap is the primary hazard.

> **A confident AI answer warrants more scrutiny, not less.**

*Source: Perry, Srivastava, Kumar & Boneh (2023), "Do Users Write More Insecure Code with
AI Assistants?", ACM CCS '23. [arXiv:2211.03622](https://arxiv.org/abs/2211.03622).*

---

## Three working models

**1. A capable new hire with no context.** The model has broad general knowledge and none
of the specifics of your project, data, or design. Anthropic's prompting guidance states
the test directly: show the prompt to a colleague with minimal context — if they would be
confused, the model will be too. Most poor output reflects a context gap, not a
capability gap. Supply the context a new hire would need.

**2. Generation outpaces verification.** The model produces code faster than it can be
checked, which makes verification, not writing, the primary task. Every workflow below is
designed to close the gap between plausible output and verified output. *(Addy Osmani,
"The Trust-but-Verify pattern"; consistent with O'Reilly and Anthropic engineering
guidance.)*

**3. AI assistance benefits experienced users more than beginners.** Experienced users
steer the model and catch a substantial share of its errors; beginners are more likely to
accept flawed output they cannot diagnose, producing a "two steps back" pattern on
difficult tasks. This document is written for the audience at risk of that pattern. The
mitigation is not avoiding AI use but building the checking habits below.
*(Osmani, "The 70% problem.")*

---

## Prompting practices

Anthropic and OpenAI's official guides converge independently on the same set of rules,
which is the basis for including them here:

| Rule | Do this | Why |
|---|---|---|
| **Be specific** | Language + version + libraries + the exact shape of your data + what "done" looks like | The model fills every blank you leave with a guess; specificity removes the guessing |
| **Say what TO do** | *"use snake_case names"* beats *"don't use camelCase"* | Positive instructions generalize; negative ones leave the space of alternatives open |
| **Give the "why"** | *"this will be read by a screen reader, so…"* | The model generalizes from the reason to cases you didn't list |
| **Show an example** | Paste one input row and the output you want | One good example beats a paragraph of description |
| **Put data first, question last** | Long data/spec at top, the ask at the bottom | Anthropic: this ordering can improve quality by up to ~30% on long inputs |
| **Give it a role** | *"You are a careful statistician working in R"* | Even one sentence measurably focuses the output |
| **Ask it to self-check** | *"Before you finish, verify this against [criterion]"* | "Catches errors reliably, especially for coding and math" |

The full five-part template lives in [PROMPTS.md](../PROMPTS.md). Use it.

---

## The debugging loop

Debugging is the majority of the work, not a sign of failure.

1. Paste the **whole** code and the **whole** error, including the traceback and line
   numbers — not a summary of the error.
2. Fix **one** error, re-run, repeat.
3. **Three strikes:** after three failures on the same error, start a **new chat**,
   restate the goal from scratch, and do not paste the failed attempts. Fresh context
   outperforms continued argument, and a clean session reviews code more critically
   because the model is not defending output it just produced.

---

## Failure modes and evidence

**1. Hallucinated packages ("slopsquatting").** The largest study to date (576,000 code
samples, 16 models) found suggested packages that do not exist in 5–22% of cases —
commercial models ≥5.2%, open-source models ~21.7%, over 205,000 unique fake names. This
enables a predictable supply-chain attack: an attacker registers the name the model
reliably invents, and the next user who runs the suggested `pip install` gets malware.
→ Confirm every suggested package on PyPI/CRAN (real project page, download activity,
recent maintenance) before installing. *(Spracklen et al., USENIX Security 2025,
[arXiv:2406.10279](https://arxiv.org/abs/2406.10279).)*

**2. Fabricated citations and numbers.** An audit of 636 ChatGPT-generated references
found GPT-3.5 fabricated 55% of them and GPT-4 18%, with many of the remaining "real"
citations attached to the wrong source. Fabrication rates decline with newer models but
do not reach zero.
→ Resolve every DOI and locate every paper. For any statistic stated in prose, regenerate
it by running code (see failure #4). *(Walters & Wilder, 2023, Scientific Reports.)*

**3. Wrong test for the design.** The model runs the test named in the prompt; it does
not infer that 60 rows are 30 people unless told. See
[STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md).

**4. Invented numbers in prose.** A requested Results paragraph can contain a well-formed
F, df, and R² that do not appear anywhere in the actual output.
→ Check every number against the model object, every time. A number in prose is a claim,
not a result.

**5. Silent scope errors.** The model may run on the full sample when a subgroup was
intended, drop NAs without reporting it, or fit on 47 of 60 rows without mention.
→ Print `n` before and after every filter, join, and drop.

Two additional tendencies, noted in Anthropic's own guidance: the model will hard-code to
pass the specific example given rather than solving the general problem (test on
different inputs to catch this), and it will over-engineer — adding files or
abstractions not requested — unless explicitly told to keep the solution minimal.

---

## Prompts for verification

Prompts that surface what the model would not otherwise volunteer.

- *"What is this code assuming about my data?"* — surfaces silent assumptions
- *"What would make this analysis wrong?"* — the model can answer this but does not
  volunteer it
- *"Is this the right test? What does it assume, and does my design meet it?"* — catches
  the repeated-measures error
- *"Explain what line 7 does as if to someone who's never coded."* — if the explanation
  cannot be followed, do not run the code
- *"You used a package I don't recognize. Is `[name]` real, and is it on CRAN/PyPI?"*
- *"Give me two different ways to do this and the trade-offs."* — avoids anchoring on the
  first plausible answer
- *"Rewrite this so a reviewer could reproduce it exactly."* — forces seeds, versions,
  explicit steps

---

## Non-negotiable rules

1. **Never paste real patient data into a consumer chatbot.** Schema, not rows. See
   [DATA_PRIVACY.md](DATA_PRIVACY.md).
2. **Run it. Read it. Then trust it.** In that order. Code that runs without error can
   still answer a different question than the one asked.
3. **If it cannot be explained, it should not be published.** This is a practical
   constraint, not a moral one: the analysis must be defensible at committee and in
   review.
4. **Verify before use:** does it run on the actual data, do the functions exist, was the
   code read (not just its summary), was every number regenerated? Anthropic's engineering
   guidance states the standard directly: have the AI show evidence, not assert success.
5. **Disclose use.** Report AI use in the methods section; retain the chat log. See
   [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

> The researcher is the senior author on everything the AI produces, and is accountable
> for it accordingly.

---

*Sources inline. The framing study (Perry et al., CCS '23), the package-hallucination rates
(Spracklen et al., USENIX Security '25), and the citation-fabrication audit (Walters &
Wilder, Scientific Reports '23) are peer-reviewed / archival primaries; the prompting rules
are from Anthropic's and OpenAI's official documentation; the "70%/verify" framing is Addy
Osmani's engineering essays.*
