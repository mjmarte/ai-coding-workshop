# Guardrails

Reference documents for checking AI-assisted research workflows after the workshop.

The documents contain inline citations, but the repository does not include the cited PDFs,
reference library, or a claim-by-claim evidence ledger. They are therefore not source-audited
materials for scholarly reuse. See [EVIDENCE_STATUS.md](EVIDENCE_STATUS.md) before carrying a
claim, number, or citation into a manuscript, grant, protocol, or policy document.

| File | What it's for | Read it when |
|---|---|---|
| File | Purpose | Use it when |
| [AI_CODING_RULES.md](AI_CODING_RULES.md) | Prompting and verification practices | Before relying on generated code |
| [STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md) | Statistical-design questions and catch prompts | Before interpreting an analysis |
| [DATA_PRIVACY.md](DATA_PRIVACY.md) | Privacy review questions and schema-first workflow | Before working with real data |
| [ANALYSIS_REVIEW_RUBRIC.md](ANALYSIS_REVIEW_RUBRIC.md) | Analysis review checklist | Before reporting an analysis |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | Reproducibility workflow | At project setup and before submission |
| [RESEARCH_PROJECT_RULES.md](RESEARCH_PROJECT_RULES.md) | Project-level instructions for an AI assistant | When setting up an AI-assisted project |

---

## Priority reading

1. [DATA_PRIVACY.md](DATA_PRIVACY.md), then confirm the applicable institutional policy and
   approved environment.
2. [STATISTICS_GUARDRAILS.md](STATISTICS_GUARDRAILS.md), then inspect whether the model reflects
   the study design.
3. [ANALYSIS_REVIEW_RUBRIC.md](ANALYSIS_REVIEW_RUBRIC.md), then retain the output that supports
   every reported value.

## Summary

The common workflow is to specify the design, run the analysis, inspect the resulting objects,
and trace each reported statement to code and output. These documents support that workflow;
they do not replace source review or institutional approval.
