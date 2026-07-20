# Prompt and verification guide

Use this page beside an AI chat and the environment where the code will run. A prompt is an
analysis specification in compact form. It does not validate the returned code.

## Build the request from the analysis

| Include | State it concretely |
|---|---|
| Environment | `I am using R in Posit Cloud` or `Python in Colab` |
| Unit of observation | `One row is one participant` |
| Files and variables | Exact paths, column names, and variable meanings |
| Analytic task | One operation or model |
| Design constraints | Repeated records, subgroup, time boundary, required packages |
| Requested return | Code only, imports included, short comments |

```text
I am a [role] using [language] in [environment].

My file is [path]. One row is [unit]. The columns are [names and meanings].

I need [one analytic task]. The design constraint is [constraint].

Use [packages]. Create [object name]. Return code only, with short comments and all imports.
```

Compare the code against the request before running it. A returned object with a different name,
a changed row set, or an added analysis answers a different question.

## Debug one failure at a time

```text
Here is the complete code I ran:
[paste the code]

Here is the complete error, including the traceback:
[paste the error]

I am using [R/Python version if known]. Identify the immediate cause and give the smallest
correction. Do not rewrite the analysis.
```

Run the correction before requesting another change. If the same diagnosis fails twice, begin a
new conversation with the original task, code, and error. The old conversation may be committed
to an incorrect explanation.

## Prompts that inspect assumptions

| Ask | Check in the answer or output |
|---|---|
| `What does this code assume about the rows and groups?` | Unit of observation, exclusions, and joins |
| `What design feature determines this model?` | Pairing, clustering, time order, or outcome type |
| `Show the row count before and after each filter or join.` | Silent scope change |
| `Explain this formula term by term.` | Whether the model encodes the design |
| `What output supports each reported number?` | Values added in prose without a source |
| `Give two plausible analytic approaches and their assumptions.` | Whether the first approach is being accepted by default |
| `Is this package real? Link its CRAN or PyPI page.` | A package or function name before installation |

## Verification rules

1. Inspect the data before modeling: dimensions, column types, missingness, and group counts.
2. Inspect the row count after every filter, join, or missing-data exclusion.
3. Read the model formula. The formula must encode the intended outcome, predictors, and
   dependence structure.
4. Keep model output visible while writing a result sentence. Report only values returned by the
   fitted model or a named post-fit calculation.
5. Treat a fluent explanation as a draft. Verify its direction, numbers, sample, and model against
   the code and output.

## Data boundary

The workshop data are synthetic. For a real project, use the institutionally approved service and
the applicable data agreement. When requesting coding help, provide the schema, variable types,
and fabricated example rows unless permission for actual data has been confirmed in writing.

## Prompt comparisons from this workshop

### Two-group comparison

| Request | What you must inspect |
|---|---|
| `Compare word count between my groups.` | Whether the comparison addresses the research question, the groups are appropriate, and the requested test's assumptions are met. |
| `Compare word count by group. Controls are near the upper range of WAB-AQ by construction. Show group sizes and distributions before selecting a test, and explain whether a pooled association with WAB-AQ would answer a within-aphasia question.` | Whether the returned analysis distinguishes a group contrast from a within-group association. |

### Repeated measurements

| Request | What you must inspect |
|---|---|
| `I measured participants at 1 and 12 months. Did they improve?` | Whether each participant's two records are treated as related. |
| `Thirty participants were each assessed at acute and chronic timepoints. Fit WAB-AQ from timepoint with a random intercept for participant ID. Explain why this term is in the formula and show the model summary and confidence interval.` | `participant_id` appears in the random-effects term and the time reference level is stated. |

### Acute-to-chronic prediction

| Request | What you must inspect |
|---|---|
| `Use machine learning to predict 12-month WAB-AQ.` | Whether later variables, outcome leakage, training performance, or preprocessing outside resampling enter the workflow. |
| `Estimate 12-month WAB-AQ from acute variables only. Define the outcome and predictor sets before fitting. Compare a clinical predictor set with a clinical-plus-imaging set using repeated cross-validation. Keep imputation, scaling, and fitting inside the pipeline. Report resampled MAE and R-squared, then state what this synthetic development exercise does not establish.` | Predictor timing, resampling, and the interpretation boundary. |

## End every session with a record

```text
Summarize the analysis steps completed in this conversation. For each step, name the input,
output object or file, model formula if applicable, and unresolved decision. Do not write Methods
prose or add results that are not in the displayed output.
```

`guardrails/` contains background resources. Their literature references are not a substitute for
a source audit when a claim enters a manuscript, grant, protocol, or methods document.
