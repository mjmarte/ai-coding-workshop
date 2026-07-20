# The data

All files are synthetic. `make_data.py` generates each transcript from sentence templates;
no person produced these utterances. The workshop data contain no participant records. This
does not determine whether a real dataset may be entered into an AI service.

The files were constructed for specific teaching exercises: group differences in discourse
measures, longitudinal within-participant observations, and a length-sensitive lexical-diversity
measure. They are not a clinical cohort or an empirical model of aphasia.

## transcripts.csv - 60 rows, one per participant

| Column | Type | Meaning |
|---|---|---|
| `participant_id` | chr | `C###` control, `A###` aphasia |
| `group` | chr | `control` or `aphasia` |
| `age` | int | years |
| `sex` | chr | `F` / `M` |
| `education_years` | int | years of formal education |
| `months_post_onset` | dbl | months since stroke; `NA` for controls |
| `wab_aq` | dbl | Synthetic Aphasia Quotient, 0-100. Higher values indicate less impairment in this exercise. |
| `transcript` | chr | synthetic picture description |

## transcripts_long.csv - 60 rows, 30 participants x 2 visits

The aphasia group only, measured at `acute` (about 1 month post-onset) and `chronic`
(about 12 months). The file adds `timepoint`. The 60 rows are repeated measurements from 30
participants, so analyses of timepoint must represent the within-participant pairing.

## features.csv - 60 rows, precomputed Python measures

The NLP measures pre-computed, so the R half works even if you never finished the Python
half. Columns: `n_words`, `n_unique_words`, `type_token_ratio`, `mean_word_length`,
`content_word_ratio`, `filler_rate`.

## Constructed associations used in the workshop

Within the aphasia group, correlations with WAB-AQ:

| Measure | r |
|---|---|
| `filler_rate` | -0.83 |
| `n_words` | +0.60 |
| `content_word_ratio` | +0.51 |
| `mean_word_length` | +0.46 |
| `type_token_ratio` | +0.17 |

These correlations are properties of the generated dataset. The workshop uses the
type-token-ratio result to require participants to inspect transcript length before assigning
substantive meaning to the measure.

## recovery_prediction.csv - 90 synthetic acute-stroke participants

This file supports the advanced Python notebook. Each row is one participant assessed
in the acute phase. The outcome is `outcome_wab_aq_12m`, a synthetic 12-month WAB-AQ.
The other variables are available at the acute assessment:

| Column | Meaning |
|---|---|
| `acute_wab_aq` | acute WAB-AQ |
| `acute_discourse_score` | synthetic acute narrative-discourse score (0-10) |
| `lesion_volume_ml` | synthetic lesion volume in millilitres |
| `cortical_lesion_pct` | synthetic cortical lesion burden (%) |
| `dorsal_disconnection_pct` | synthetic dorsal-stream disconnection proportion |
| `ventral_disconnection_pct` | synthetic ventral-stream disconnection proportion |

The file is an exercise in prediction workflow: define predictors available at baseline,
keep the 12-month outcome out of the predictor matrix, and evaluate models with resampling.
It is not a clinical prediction model, a representation of a trial cohort, or evidence for
any clinical association.
