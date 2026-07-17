# Guardrails

*Reference documents intended for continued use after the workshop, on real research
projects.*

Every claim is sourced to the primary literature or to official vendor documentation,
cited inline, and written for a neuro/rehab researcher who is a beginner programmer, not
for an engineer.

| File | What it's for | Read it when |
|---|---|---|
| **[AI_CODING_RULES.md](AI_CODING_RULES.md)** | How to work with an AI assistant — the mental models, prompt patterns, and documented failure modes, with the evidence | Before you rely on AI for anything that matters |
| **[STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md)** | The eleven statistical traps an AI walks you into without warning — each with a catch-prompt and a fix, several verified live in this workshop's data | Before you trust any analysis it wrote |
| **[DATA_PRIVACY.md](DATA_PRIVACY.md)** | What you may and may not paste into a chatbot; HIPAA's 18 identifiers; the schema-not-rows workflow | Before you touch real patient data — read once, properly |
| **[ANALYSIS_REVIEW_RUBRIC.md](ANALYSIS_REVIEW_RUBRIC.md)** | A printable scorecard to run any AI analysis through before you trust a number | Every time, on every analysis. Print it. |
| **[REPRODUCIBILITY.md](REPRODUCIBILITY.md)** | Good-enough practices so your result re-runs in six months; notebook hygiene; disclosing AI use | When you set up a project, and before you submit |
| **[RESEARCH_PROJECT_RULES.md](RESEARCH_PROJECT_RULES.md)** | A ready-to-paste `CLAUDE.md` / `.cursorrules` that makes the AI follow these guardrails itself | When you start a real project with an AI tool |

---

## Priority reading

1. **[DATA_PRIVACY.md](DATA_PRIVACY.md)** — the error it prevents is unrecoverable.
2. **[STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md)** — these errors run without
   crashing and publish wrong.
3. **[ANALYSIS_REVIEW_RUBRIC.md](ANALYSIS_REVIEW_RUBRIC.md)** — a checklist to run before
   trusting any output.

## Summary

AI removes the burden of typing code but not the requirement of knowing what the code
should do. It is possible to skip that knowledge without noticing. These documents are
the check against that.
