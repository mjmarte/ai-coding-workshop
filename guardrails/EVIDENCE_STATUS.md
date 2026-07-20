# Evidence status for the guardrail documents

## Scope of this audit

This repository contains inline citations in the guardrail documents, but it contains no source
PDFs, reference manager export, or claim-by-claim evidence ledger. The citation checks required
for scholarly reuse cannot therefore be completed from this project alone.

This file distinguishes executable teaching facts from external claims. It does not certify the
external claims below.

## Verified against this repository

| Workshop claim | Evidence in the repository | Verification route |
|---|---|---|
| The baseline transcript file has 60 rows and 8 columns | `data/transcripts.csv` | Python Task 1 checkpoint |
| The feature join has 60 rows and 14 columns | `data/transcripts.csv`, `data/features.csv` | R Task 1 checkpoint |
| Longitudinal data contain 30 participants measured twice | `data/transcripts_long.csv` | R Task 6 prompt and `participant_id` count |
| Mixed-model estimate is 7.060 WAB points for chronic relative to acute | `r/02_r_solution.R` | `summary(long_model)` |
| Mixed-model Wald interval is 4.388 to 9.732 | `r/02_r_solution.R` | `confint(long_model, method = "Wald")` |
| Advanced notebook uses repeated resampling and pipelines | `python/_build_advanced_notebook.py` | generated notebook source |

These are facts about constructed data and code, not clinical findings.

## Not source-audited in this repository

The following documents include factual claims, numerical rates, legal or policy statements, or
literature interpretations that require retrieval and claim-level verification before reuse:

- `AI_CODING_RULES.md`
- `STATISTICS_GUARDRAILS.md`
- `DATA_PRIVACY.md`
- `REPRODUCIBILITY.md`
- `ANALYSIS_REVIEW_RUBRIC.md`
- `RESEARCH_PROJECT_RULES.md`

Examples include package-hallucination rates, paper-audit percentages, reproducibility rates,
AI-product guidance, privacy obligations, and statistics-literature summaries. An inline link or
parenthetical citation does not establish that the cited source supports the exact wording.

## Required gate before scholarly or policy reuse

1. Obtain the full primary source or official policy text.
2. Record the exact claim, source location, and wording permitted by the source.
3. Check whether the cited study population, tool version, legal jurisdiction, and date match the
   intended use.
4. Revise or remove claims that exceed the source, then retain the completed ledger with the
   project.

For privacy decisions, institutional policy, agreements, and the approved technical environment
govern. This workshop repository is not a policy determination.
