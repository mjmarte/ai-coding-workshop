# Statistics guardrails for neuro & rehab research

*A field guide to the mistakes an AI assistant will make for you, cheerfully, without a warning.*

An AI coding assistant runs the test you name. It does not know your **design** — that
your 60 rows are 30 people measured twice, that your controls are pinned at ceiling, that
you enrolled the most-impaired patients and they'll drift upward no matter what you do. It
has read every paper describing these traps and will still walk you straight into them,
because you asked for code, not for judgement.

This file is the judgement. Every trap below is documented in the literature, and most of
them are **live in this workshop's own synthetic data** — the numbers in the examples are
real, computed from `data/`. If you learn to catch these eleven, you have caught most of
what damages a rehab-research paper.

**How to read each entry:** what it is → how it shows up in neuro/rehab → *how the AI
commits it* → **the catch** (a prompt + a manual check) → the fix → the source.

---

## The one question under all of them

> **What is my unit of analysis, and does every row in this model earn its place as
> independent evidence?**

Nearly every trap below is a violation of that one sentence. Print it above your desk.

---

## The master rubric — answer these BEFORE you trust any analysis

Copy this into your AI chat and make it answer, in order:

1. **Unit of analysis.** What is one independent observation — a patient, or a
   measurement? How many *independent* units do I actually have?
2. **Design.** Is this between-groups, repeated-measures, or nested? Where is the
   non-independence?
3. **The test's assumptions.** List them. For *my* data, which are met, which are
   doubtful, and how would I check each one?
4. **The comparison I actually care about.** Am I testing the difference I claim, or two
   separate tests I'm eyeballing?
5. **Scope.** Who is in this model? Did any filter, `dropna`, or subgroup silently change
   `n`? (Print `n` before and after every filter.)
6. **What would make this wrong?** Name the top three threats to this specific inference.

The AI answers all of these well — *once you ask*. It volunteers none of them.

---

## 1. Pseudoreplication — treating repeated measures as independent
**The single most important one for rehab data.**

- **What it is.** Multiple observations from the same participant (two visits, twenty
  discourse samples, hundreds of trials) counted as independent, inflating your degrees of
  freedom and your false-positive rate.
- **In rehab.** "30 patients × 2 timepoints = 60 observations" fed to a t-test or a plain
  `lm()`. The unit is the *patient*; you have 30, not 60.
- **How the AI commits it.** You paste a 60-row long-format file and say "test whether
  scores improved." It writes `lm(wab_aq ~ timepoint)` or `t.test()`. It runs. It looks
  right.
- **The catch — this is live in `data/transcripts_long.csv`:**
  - Correct model: `lmer(wab_aq ~ timepoint + (1 | participant_id))` → chronic is
    **+7.1 WAB points, t = 5.2**. A clear, real improvement.
  - Naive model: `lm(wab_aq ~ timepoint)` → **p = .056**. "No significant improvement."
  - **Same data. The wrong model didn't invent an effect — it *hid* one.** Throwing away
    the pairing threw away the power to see it.
  - Ask the AI: *"These are repeated measures — two visits per participant. Does this model
    account for the within-person correlation? What's my unit of analysis?"*
- **The fix.** Linear mixed-effects models with a random intercept per participant (and a
  random slope if the effect can vary by person): `lme4::lmer` in R,
  `statsmodels.MixedLM` in Python. Or aggregate to one value per participant first.
- **Sources.** Lazic (2010), *The problem of pseudoreplication in neuroscientific
  studies*, **BMC Neuroscience 11:5** — audited neuro papers: ~12% clearly
  pseudoreplicated, ~36% more suspected. Aarts et al. (2014), *A solution to dependency*,
  **Nature Neuroscience 17:491** — ignoring nesting inflates the false-positive rate to as
  high as ~80%.

---

## 2. The interaction fallacy — "significant" vs "not significant" is not a comparison
**How almost everyone accidentally claims a treatment worked.**

- **What it is.** Concluding two effects *differ* because one is significant and the other
  isn't — without testing the difference (the interaction) directly.
- **In rehab.** "The treatment group improved (p = .02); the control group did not
  (p = .09) — so treatment helped." You have not compared the groups. You compared each to
  zero and eyeballed the p-values.
- **How the AI commits it.** Ask it to "test whether each group improved" and it dutifully
  runs two within-group tests and reports both — structurally inviting the fallacy. It will
  not spontaneously fit the `group × time` interaction unless you ask for the comparison.
- **The catch.** Ask: *"I want to know whether the groups differ in how much they changed.
  Is that the interaction term, and have you actually tested it?"* The comparison you want
  is a single term, with its own p-value.
- **The fix.** Fit `outcome ~ group * time` (mixed model for repeated measures) and read
  the **interaction**. For two correlations, test the difference between them, not each
  against zero.
- **Sources.** Nieuwenhuis, Forstmann & Wagenmakers (2011), *Erroneous analyses of
  interactions in neuroscience*, **Nature Neuroscience 14:1105** — of 157 papers with the
  opportunity, ~50% made the error. Gelman & Stern (2006), *The difference between
  "significant" and "not significant" is not itself statistically significant*, **The
  American Statistician 60:328**.

---

## 3. Ceiling/floor effects — pooling manufactures correlations out of thin air
**Live in this workshop's data.**

- **What it is.** Correlating a measure across a pooled sample when one group sits at
  ceiling (no variance) and the other is spread out. The "correlation" is really the
  between-group mean difference wearing a correlation's clothes.
- **In rehab.** Controls score ~99 on the WAB (ceiling); patients range 26–99. Pool them
  and *any* language measure "predicts" WAB — because it separates the two clusters, not
  because it tracks severity within anyone.
- **How the AI commits it.** "Model wab_aq from n_words" across all 60 people. It never
  asks who's at ceiling.
- **The catch — real numbers from `data/`:**
  - `n_words` vs `wab_aq`, **aphasia group only: R² = .36**.
  - Same relationship, **all 60 pooled: R² = .70**.
  - Half your "explained variance" is just group membership. **Only you know the controls
    are at ceiling.** Ask: *"Are any of my groups at a ceiling or floor on the outcome? If
    so, is this correlation real or an artifact of pooling?"* And always **plot it** — two
    clouds joined by a line is the signature.
- **The fix.** Model *within* the group that has variance (here, aphasia only), or test the
  group difference explicitly instead of dressing it as a continuous relationship.
- **Source.** Makin & Orban de Xivry (2019), *Ten common statistical mistakes*, **eLife
  8:e48175**, mistake #4 (spurious correlations) — their figure shows two clusters
  manufacturing a line. This is a restriction-of-range / aggregation artifact (Simpson's
  paradox family).

---

## 4. Regression to the mean — the rehab-specific ghost
**Not in most "common mistakes" lists. Belongs at the top of yours.**

- **What it is.** Enroll patients *because* they scored extreme at baseline, and they'll
  drift toward the mean at retest — through measurement noise alone, with no treatment and
  no true change.
- **In rehab.** "The most severe patients gained the most from therapy." That is the exact
  signature of regression to the mean, and it compounds with **spontaneous recovery** in
  the months after stroke.
- **How the AI commits it.** Ask it to "compare change scores across severity subgroups"
  and it computes them without a word about RTM or the baseline-selection that created it.
- **The catch.** Ask: *"I selected these patients on their baseline scores. How much of
  this apparent change could be regression to the mean plus spontaneous recovery rather
  than my intervention?"*
- **The fix.** A concurrent (ideally randomized) control group; ANCOVA adjusting for
  baseline rather than analyzing change scores in a baseline-selected subgroup; model RTM
  at the design stage.
- **Source.** Barnett, van der Pols & Dobson (2005), *Regression to the mean: what it is
  and how to deal with it*, **International Journal of Epidemiology 34:215**.

---

## 5. No control group — pre/post gains ≠ treatment effect

- **What it is.** A within-group improvement attributed to your intervention when nothing
  rules out the things that improve outcomes anyway.
- **In rehab.** Post-stroke, the two biggest rivals to "my therapy worked" are
  **spontaneous recovery** and RTM (#4). A pre/post gain is consistent with all three.
- **The catch.** Ask: *"What besides my intervention could produce this pre-to-post change,
  and does my design rule it out?"*
- **The fix.** A concurrent control/comparison group; randomization where possible.
- **Source.** Makin & Orban de Xivry (2019), mistake #1 (absence of an adequate control).

---

## 6. Multiple comparisons — the dead salmon

- **What it is.** Many simultaneous tests (voxels, electrodes, a dozen language outcomes,
  many time bins) without correcting for the number of tests. At α = .05, false positives
  are guaranteed at scale.
- **In rehab.** "We ran all our subtests against outcome and three were significant." How
  many did you run?
- **How the AI commits it.** Hand it a wide dataframe and ask "which variables predict
  outcome"; it happily reports the significant ones and stays silent about the count.
- **The catch.** Ask: *"How many tests am I running here, and how should I control the
  family-wise error or FDR?"* State your **primary** outcome in advance.
- **The fix.** FWER (Bonferroni/permutation) or FDR control; pre-specify one primary
  outcome; treat the rest as exploratory.
- **Source.** Bennett et al. (2010), the post-mortem Atlantic salmon "fMRI" — 16 "active"
  voxels uncorrected, **zero** after correction. (Ig Nobel, 2012.)

---

## 7. Small samples — low power hurts even when you "win"

- **What it is.** Underpowered designs don't just miss real effects. When a small study
  *does* hit significance, the effect size is **inflated** (the winner's curse), and the
  result is less likely to be true.
- **In rehab.** Aphasia N is chronically small. An exciting effect from n = 8 is exactly
  the kind most likely to be an overestimate that won't replicate.
- **The catch.** Ask: *"What effect size could this sample actually detect, and how much
  should I discount a significant result at this N?"* Report the **confidence interval** —
  its width tells the honest story.
- **The fix.** A-priori power/precision planning; report CIs; favor within-subject designs;
  pool across sites / registered reports; interpret single small studies cautiously.
- **Source.** Button et al. (2013), *Power failure*, **Nature Reviews Neuroscience 14:365**
  — median power in neuroscience estimated at ~8–31%.

---

## 8. Researcher degrees of freedom — the AI will fish until it catches something

- **What it is.** Undisclosed flexibility — which outcome, which covariates, which
  exclusions, whether to drop the outlier, when to stop collecting — inflates false
  positives far above 5%, *even when you're being honest*, because the analysis you chose
  was contingent on the data you saw (the "garden of forking paths").
- **In rehab.** "Try it with and without the outlier / with age as a covariate / on the
  subtest that moved." Each fork is defensible; the *set* of forks is a hidden
  multiple-comparisons problem.
- **How the AI commits it — and why it's worse with AI.** It costs nothing to ask a chatbot
  "try another model that makes this significant," and it will. That is p-hacking with a
  friendly interface. **The tool that lowers the cost of analysis raises the cost of
  discipline.**
- **The catch.** Decide your analysis *before* you see the result. Ask: *"If I'd made
  slightly different but equally reasonable choices here, would the conclusion hold?"*
  Report every measure, exclusion, and model you tried.
- **The fix.** Pre-register or write an analysis plan; report all outcomes and exclusions;
  multiverse / specification-curve analysis for robustness.
- **Sources.** Simmons, Nelson & Simonsohn (2011), *False-positive psychology*,
  **Psychological Science 22:1359**. Gelman & Loken (2014), *The statistical crisis in
  science*, **American Scientist 102:460**.

---

## 9. Circular analysis — double dipping

- **What it is.** Using the same data to *select* (voxels, an ROI, responders, a
  time-window, features) and then to *test* the effect. Selection captures noise; the test
  is no longer independent of it.
- **In rehab.** Define "responders" as the patients who improved most, then run a test
  showing the responders improved. You built the result into the selection.
- **The catch.** Ask: *"Did I use the same data to choose what to test and to test it? Is
  my selection independent of the effect under the null?"*
- **The fix.** Select on independent data (split-half, hold-out, cross-validation), or use
  a non-selective whole-sample analysis with proper correction.
- **Source.** Kriegeskorte et al. (2009), *Circular analysis in systems neuroscience: the
  dangers of double dipping*, **Nature Neuroscience 12:535**. Related: Vul et al. (2009),
  the "voodoo correlations" paper.

---

## 10. Confounded measures — lexical diversity depends on sample length
**A 40-year-old known problem, live in this workshop's data, and the AI won't mention it.**

- **What it is.** Type-Token Ratio (unique words ÷ total words) falls mechanically as a
  language sample gets longer — more words means more repetition. So TTR is confounded with
  transcript length.
- **In rehab.** Impaired speakers produce **shorter** transcripts. So TTR is fighting
  itself: lower severity → more words → lower TTR, even as vocabulary is objectively richer.
  Any TTR group difference may be a length difference in disguise.
- **The catch — real numbers from `data/`:** within the aphasia group, `r(TTR, n_words) =
  −0.41`, and patients average 68 words vs controls' 110. Ask the AI: *"Is this measure
  confounded with sample length? What's the standard fix in my field?"* It gives a good
  answer — **only because you asked.**
- **The fix.** Standardize token count before computing; or use length-robust measures —
  **MATTR** (moving-average TTR), **vocd-D**, or **MTLD**.
- **Source.** Richards (1987), *Type/token ratios: what do they really tell us?*, **Journal
  of Child Language 14:201** — the canonical statement of the length confound. Modern
  length-robust alternatives are standard in TalkBank/AphasiaBank workflows.

---

## 11. Correlation is not causation (still, forever)

- **What it is.** An observational association read as a causal mechanism.
- **In rehab.** "Patients who talk more recover better" → "getting patients to talk more
  will improve recovery." Maybe. Or milder aphasia causes both.
- **The catch.** Ask: *"Is this associational or causal, given my design? What would I need
  to claim causation?"*
- **The fix.** Design (randomization), or explicit causal caveats in the prose.
- **Source.** Makin & Orban de Xivry (2019), mistake #10.

---

## Reporting hygiene (do this every time)

- **Report effect sizes and confidence intervals, not just p-values.** A p-value is not the
  probability your hypothesis is true, is not an effect size, and is not a yes/no gate.
  *Source: Wasserstein & Lazar (2016), the ASA Statement on p-values, **The American
  Statistician 70:129**.*
- **p > .05 does not mean "no effect."** It means "not enough evidence, given this
  (possibly underpowered) design." Never write "there was no difference" from a bare
  non-significant p. Use CIs or equivalence tests if you want to argue *for* the null.
- **"p = .07, a trend toward significance" is not a thing.** Neither is "p = .04, highly
  significant." Report the number and the interval; let the reader judge.
- **Never report a number you cannot point to in a model object.** (See the fact-check
  exercise — the AI *will* write a beautiful Results paragraph containing an F, a df, and an
  R² that appear nowhere in your output.)
- **Follow the reporting checklist for your design.** **CONSORT** for randomized trials,
  **STROBE** for observational studies (most aphasia-recovery datasets are STROBE),
  **PRISMA** for systematic reviews. All at [equator-network.org](https://www.equator-network.org).

---

## The pocket version — five prompts that catch most of it

Paste these into your AI chat, in this order, on any analysis:

1. *"What is my unit of analysis, and does this model treat any repeated measurements as
   independent when they aren't?"*
2. *"Is any group at a ceiling or floor on the outcome, and is this relationship an artifact
   of pooling?"*
3. *"Am I comparing two effects by their difference, or just eyeballing two separate
   p-values?"*
4. *"List this test's assumptions and tell me, for my data, which are doubtful and how to
   check them."*
5. *"What are the three most likely reasons this specific conclusion is wrong?"*

---

*Sourcing note: entries were compiled from the primary literature cited inline. The anchor
review is Makin & Orban de Xivry (2019), eLife — its ten mistakes map onto most of this
file. The workshop's synthetic dataset was engineered so that traps #1, #3, and #10
reproduce to two decimals against `data/`; those numbers were verified, not asserted.*
