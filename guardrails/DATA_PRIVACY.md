# Data privacy: what you may and may not paste into a chatbot

*A violation of this rule can constitute a HIPAA/IRB breach with career and legal
consequences.*

The workshop data is synthetic: no protocol, no consent process, and no PHI apply to it.
This is deliberate — it is what makes pasting it into an AI tool safe during the workshop.
The rules below apply the moment real data is involved.

---

## The rule

> **Never paste real patient data into a consumer AI chat interface.** Not transcripts,
> not MRNs, not dates, not "de-identified" text you have not actually verified. When you
> want AI help on real data, **share the schema, not the rows.**

Column names, types, and a *fabricated* example row are enough to get working code. The AI
does not need to see a single real value to write your analysis.

---

## Rationale

Input to a consumer chat tool (the free/personal tiers of ChatGPT, Claude, Gemini,
Copilot) may be stored, retained, reviewed by humans, or used to improve the model. For
ordinary text this is inconsequential. For protected health information it constitutes an
unauthorized disclosure — a HIPAA and IRB violation — and it is irreversible: a sent
prompt cannot be recalled, and later deletion does not undo the disclosure.

Consumer chat interfaces are not covered by an institution's Business Associate Agreement
(BAA) unless a specific deployment has been confirmed in writing. An enterprise license is
not equivalent to PHI clearance. Confirm approved tools with IT/compliance in writing
before use.

---

## What counts as PHI

"De-identified" is a legal definition, not an informal judgment. Under the HIPAA Safe
Harbor method
(45 CFR §164.514(b)), data is de-identified only when **all 18 identifier types** are
removed *and* you have no actual knowledge the remainder could re-identify someone:

1. Names
2. Geographic subdivisions smaller than a state (street, city, county; ZIP beyond its
   first three digits)
3. **All date elements** except year — admission, discharge, visit, **date of birth**; and
   all ages over 89
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and license plates
13. Device identifiers and serial numbers
14. URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voiceprints)
17. Full-face photographs and comparable images
18. Any other unique identifying number, characteristic, or code

Two commonly overlooked points:

- **A raw voice recording is biometric and is PHI even with the name removed**, as is a
  full-face photograph. Removing the name does not de-identify a `.wav` file.
- **Free-text clinical narrative can re-identify.** A picture-description transcript may
  name a spouse, a hometown, an employer, or a rare diagnosis. A paragraph cannot be
  certified clean by visual inspection; treat transcript text — the material central to
  this workshop — with the same caution.

---

## Workflow: schema in, synthetic twin, code out

Apply this pattern to real data:

1. **Describe, don't paste.** Give the AI your column names, their types, and units, plus
   **one row of invented, plausible values** — never a real one. That is enough for it to
   write correct code.

   > *My data is one row per patient. Columns: `patient_id` (string), `group`
   > ("aphasia"/"control"), `age` (int), `wab_aq` (0–100), `transcript` (string). Here is
   > one fabricated example row: A001, aphasia, 64, 58.2, "the boy is uh reaching for the
   > cookie". Write R to…*

2. **Build a synthetic twin.** Generate fake data with the same structure as the real
   data and develop against it. This workshop's `data/make_data.py` is a worked example;
   in practice, Python `faker`/`numpy` or R `synthpop`/`simstudy` serve this purpose.
   Prototype and debug with the AI on the synthetic twin.

3. **Run the reviewed code on the real data locally, with no AI in the loop.** Once the
   code is correct and understood, run it in the approved environment where the real data
   resides, and do not transmit real values elsewhere.

   *Synthetic data is not automatically safe: high-fidelity synthetic data can leak
   information about the real individuals it was modeled on. Keep synthetic data
   low-fidelity enough to be clearly non-real, and do not publish a synthetic dataset
   derived from sensitive data without review.*

---

## Quick decision table

| You want to… | Do this |
|---|---|
| Get code for an analysis | Paste the **schema + a fake row**, never real rows |
| Debug an error on real data | Reproduce it on the **synthetic twin**, paste that |
| Summarize/clean clinical free text | Assume it's PHI; do it in an **approved, BAA-covered** tool only |
| Use a voice recording or photo | It's **biometric PHI** — never a consumer tool |
| Use an "enterprise" AI tool for PHI | Only with **written** confirmation it's BAA-covered for your data |

---

## Disclosure of AI use

Journals and reporting bodies expect disclosure. AI cannot be an author, since authorship
requires accountability, and where AI was used it must be disclosed — see
[REPRODUCIBILITY.md](REPRODUCIBILITY.md). Retain chat logs as a provenance record.

---

*Sources: HIPAA de-identification standard, 45 CFR §164.514(b) (Cornell LII /
[hhs.gov](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html));
Giuffrè & Shung (2023), "Harnessing the power of synthetic data in healthcare," *npj
Digital Medicine*. Confirm your own institution's approved-tools list in writing before
using any AI tool on real data.*
