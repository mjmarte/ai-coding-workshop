# Working with an AI coding assistant: the rules

*The deep version of [PROMPTS.md](../PROMPTS.md). The cheat sheet tells you what to do; this
tells you why, with the evidence, so you believe it at 2am when the code looks fine and
isn't.*

---

## The one finding that should reframe everything

In a controlled study at Stanford (47 participants, real security tasks, Python/JS/C),
people **with** an AI assistant wrote **less secure** code than people without one — **and
were more likely to believe their code was secure.** The participants who did best were the
ones who **trusted the AI least and refined their prompts most.**

Sit with that. The danger isn't that the AI is wrong sometimes — you'd catch that. The
danger is that it makes you *confident* while it's wrong. For a researcher who can't yet
read the code fluently, that confidence is the whole risk.

> **The correct default posture toward a confident AI answer is more skepticism, not less.**

*Source: Perry, Srivastava, Kumar & Boneh (2023), "Do Users Write More Insecure Code with
AI Assistants?", ACM CCS '23. [arXiv:2211.03622](https://arxiv.org/abs/2211.03622).*

---

## Three mental models to hold at once

**1. It's a brilliant new employee with no context.** It has read everything and knows
nothing about *your* project, *your* data, or *your* design. Anthropic's own golden rule
for prompting: *show your prompt to a colleague with minimal context; if they'd be
confused, the AI will be too.* Most bad output is a context problem, not an intelligence
problem. Give it the context a new hire would need.

**2. Generation is easy; verification is the bottleneck.** The AI writes code faster than
you can check it — and checking, not writing, is now the job. "Blind trust is a
vulnerability." Every workflow in this file exists to close the gap between *plausible* and
*verified*. *(Addy Osmani, "The Trust-but-Verify pattern"; corroborated across O'Reilly and
Anthropic's own engineering guidance.)*

**3. The knowledge paradox: AI helps experts more than beginners.** Experienced people
steer the AI and catch its 30% of mistakes; beginners accept flawed solutions they can't
diagnose, then hit a "two steps back" spiral on the hard last stretch. **You are the
audience this paradox warns about.** The way out is not to avoid AI — it's to build exactly
the checking habits below, which is what turns a beginner into a good supervisor.
*(Osmani, "The 70% problem.")*

---

## Prompting well (the recipe, and why each part earns its place)

Both Anthropic and OpenAI's official guides independently land on the same handful of
rules. That convergence is why these and not others:

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

## The debugging loop (this is 80% of the job — it's not failure)

1. Paste the **whole** code and the **whole** error (traceback and all — the line numbers
   matter). Not your summary of the error.
2. Fix **one** error, re-run, repeat.
3. **Three strikes:** if it fails three times on the same error, it's stuck in a groove.
   Start a **new chat**, describe the goal from scratch, and **don't** paste the failed
   attempts. Fresh context beats more arguing — and a clean session also reviews code
   better, because the AI isn't defending what it just wrote.

---

## The failure modes, with the receipts

Know these five and you know where the bodies are buried.

**1. Hallucinated packages → real malware ("slopsquatting").** The largest study to date
(576,000 code samples, 16 models) found suggested packages that **don't exist** 5–22% of
the time — commercial models ≥5.2%, open-source ~21.7%, over 205,000 unique fake names.
The supply-chain attack writes itself: someone registers a name the AI predictably invents,
and the next person to run the AI's `pip install` gets malware.
→ **Never blind-install.** Confirm every suggested package on PyPI/CRAN (real project page,
downloads, recent maintenance) before installing. *(Spracklen et al., USENIX Security 2025,
[arXiv:2406.10279](https://arxiv.org/abs/2406.10279).)*

**2. Fabricated citations and numbers.** An audit of 636 ChatGPT-generated references found
**GPT-3.5 fabricated 55%** of them and **GPT-4 18%** — and many of the *real* ones cited
the wrong source. Fabrication drops with newer models but never hits zero.
→ **Resolve every DOI, find every paper.** And for any statistic the AI states in prose,
regenerate it by running code (see failure #4). *(Walters & Wilder, 2023, Scientific
Reports.)*

**3. The wrong test for your design.** It runs what you name. It does not know your 60 rows
are 30 people until you tell it. → This is its own document:
[STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md).

**4. Made-up numbers in prose.** Ask for a Results paragraph and it will produce beautiful
APA prose with an F, a df, and an R² that appear **nowhere in your output.** This is the
workshop's punchline for a reason. → **Check every number against the model object. Every
time.** A number in prose is a claim, not a result.

**5. Silent scope errors.** It models everyone when you meant a subgroup; it drops NAs
without saying so; it fits on 47 of your 60 rows and never mentions it. → **Print `n`
before and after every filter, join, and drop.**

Two more the AI does by temperament, per Anthropic's own guidance: it will **hard-code to
pass your example** instead of solving the general problem (test it on *different* inputs),
and it will **over-engineer** — extra files, needless abstractions — unless told *"keep it
simple and only do what I asked."*

---

## Prompts that catch it lying to you

The whole point of the workshop is this list. Keep it somewhere you'll actually use it.

- *"What is this code assuming about my data?"* — surfaces silent assumptions
- *"What would make this analysis wrong?"* — it knows; it just doesn't volunteer
- *"Is this the right test? What does it assume, and does my design meet it?"* — catches
  the repeated-measures error
- *"Explain what line 7 does as if to someone who's never coded."* — if you can't follow the
  explanation, don't run the code
- *"You used a package I don't recognize. Is `[name]` real, and is it on CRAN/PyPI?"*
- *"Give me two different ways to do this and the trade-offs."* — breaks it out of the first
  plausible answer
- *"Rewrite this so a reviewer could reproduce it exactly."* — forces seeds, versions,
  explicit steps

---

## The non-negotiables

1. **Never paste real patient data into a consumer chatbot.** Schema, not rows. See
   [DATA_PRIVACY.md](DATA_PRIVACY.md).
2. **Run it. Read it. Then trust it.** In that order. Code that runs can still be answering
   a different question than you asked.
3. **If you can't explain it, you can't publish it.** Not a moral rule — a practical one.
   You defend it at committee, in review, and in your own head at 2am.
4. **Verify before you ship: does it run on *my* data, do the functions exist, did I read it
   or just its summary, did I regenerate every number?** The one-line test, from Anthropic's
   engineering guide: *have the AI show evidence, not assert success.*
5. **Say what you did.** Disclose AI use in your methods; keep the chat log. See
   [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

> **You are now the senior author on everything the AI writes for you. Act like it.**

---

*Sources inline. The framing study (Perry et al., CCS '23), the package-hallucination rates
(Spracklen et al., USENIX Security '25), and the citation-fabrication audit (Walters &
Wilder, Scientific Reports '23) are peer-reviewed / archival primaries; the prompting rules
are from Anthropic's and OpenAI's official documentation; the "70%/verify" framing is Addy
Osmani's engineering essays.*
