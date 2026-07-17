# Data privacy: what you may and may not paste into a chatbot

*The one rule in this workshop that, if you break it, can end a career and breach a
patient's trust. Read it once, properly.*

The workshop data is **synthetic** — nobody said those words, there is no protocol, no
consent, no PHI. That is deliberate, and it is the whole reason you can spend the day
pasting it into an AI. The moment you go back to your own data, everything changes.

---

## The rule

> **Never paste real patient data into a consumer AI chat interface.** Not transcripts,
> not MRNs, not dates, not "de-identified" text you have not actually verified. When you
> want AI help on real data, **share the schema, not the rows.**

Column names, types, and a *fabricated* example row are enough to get working code. The AI
does not need to see a single real value to write your analysis.

---

## Why — the part people skip

When you type into a consumer chat tool (the free/personal tiers of ChatGPT, Claude,
Gemini, Copilot), what you send **may be stored, retained, human-reviewed, or used to
improve the model.** For ordinary text that's fine. For protected health information it is
an **unauthorized disclosure** — a HIPAA and IRB violation — and it is **irreversible**:
you cannot un-send a prompt, and deletion later does not undo the disclosure that already
happened.

Consumer chat interfaces are **not covered by your institution's Business Associate
Agreement (BAA)** unless someone has told you, *in writing*, that a specific deployment is.
"We have an enterprise license" is not the same as "this tool is cleared for PHI." Ask your
IT/compliance office which specific tools are approved, and get it in writing.

---

## What actually counts as PHI (it's more than names)

"De-identified" is a **legal definition, not a vibe.** Under the HIPAA Safe Harbor method
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

Two things researchers routinely miss:

- **A raw voice recording is biometric — it is PHI even with the name removed.** So is a
  full-face photo. "I took out the name" does not de-identify a `.wav` file.
- **Free-text clinical narrative re-identifies.** A picture-description transcript can name
  a spouse, a hometown, an employer, a rare diagnosis. You cannot eyeball a paragraph and
  declare it clean. This is exactly the kind of text this workshop is about — treat it with
  suspicion.

---

## The safe workflow: schema in, synthetic twin, code out

This is the pattern the whole workshop is built to teach. Use it on real data:

1. **Describe, don't paste.** Give the AI your column names, their types, and units, plus
   **one row of invented, plausible values** — never a real one. That is enough for it to
   write correct code.

   > *My data is one row per patient. Columns: `patient_id` (string), `group`
   > ("aphasia"/"control"), `age` (int), `wab_aq` (0–100), `transcript` (string). Here is
   > one fabricated example row: A001, aphasia, 64, 58.2, "the boy is uh reaching for the
   > cookie". Write R to…*

2. **Build a synthetic twin.** Generate fake data shaped like the real thing and develop
   against it. This workshop's `data/make_data.py` is a worked example; in practice, Python
   `faker`/`numpy` or R `synthpop`/`simstudy` do it. Prototype and debug with the AI on the
   synthetic twin.

3. **Run the reviewed code on the real data locally, with no AI in the loop.** Once the
   code is correct and you understand it, run it where the real data lives — your approved
   environment — and never send the real values anywhere.

   *Caveat worth teaching: synthetic ≠ automatically safe. High-fidelity synthetic data can
   leak information about the real people it was modeled on. Keep synthetic data
   low-fidelity enough to be clearly non-real, and don't publish a synthetic set built from
   sensitive data without thought.*

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

## Disclose your AI use

Journals and reporting bodies now expect it. AI **cannot be an author** (it cannot be
accountable), and you must **disclose** where and how you used it — see
[REPRODUCIBILITY.md](REPRODUCIBILITY.md). Keep your chat logs; they are your provenance.

---

*Sources: HIPAA de-identification standard, 45 CFR §164.514(b) (Cornell LII /
[hhs.gov](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html));
Giuffrè & Shung (2023), "Harnessing the power of synthetic data in healthcare," *npj
Digital Medicine*. Confirm your own institution's approved-tools list in writing before
using any AI tool on real data.*
