"""Generates 01_python_starter.ipynb and 01_python_solution.ipynb."""
import json, pathlib

REPO = "mjmarte/ai-coding-workshop"

# Notebook cell sources are concatenated without separators. Keep line endings
# when building each source list so that adjacent lines remain separate.
def md(t):   return {"cell_type": "markdown", "metadata": {},
                     "source": t.strip().splitlines(keepends=True)}
def code(t): return {"cell_type": "code", "metadata": {}, "execution_count": None,
                     "outputs": [], "source": t.strip("\n").splitlines(keepends=True)}

SETUP = f'''
# =====================================================================
#  RUN FIRST. Wait for the "Ready." line below.
# =====================================================================
# Click the play button or press Shift+Enter. Continue only after "Ready.".
import os, sys, subprocess

REPO = "{REPO}"

# 1. Download the workshop files, or update a copy from an earlier session.
if os.path.isdir(".git"):
    r = subprocess.run(["git", "pull", "--ff-only", "-q"])
elif os.path.isdir("ai-coding-workshop"):
    os.chdir("ai-coding-workshop")
    r = subprocess.run(["git", "pull", "--ff-only", "-q"])
elif not os.path.exists("data"):
    r = subprocess.run(["git", "clone", "-q", f"https://github.com/{{REPO}}.git"])
    if r.returncode == 0:
        os.chdir("ai-coding-workshop")
else:
    r = subprocess.run(["git", "status"], capture_output=True)
if r.returncode != 0:
    raise SystemExit(
        "Could not download or update the workshop files. Check the GitHub link "
        "and tell the facilitator.")

# 2. Download the small English model spaCy needs for Task 4
subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm", "-q"])
os.makedirs("outputs", exist_ok=True)

# 3. Confirm the data is present before proceeding
missing = [f for f in ("data/transcripts.csv", "data/features.csv", "data/recovery_prediction.csv")
           if not os.path.exists(f)]
if missing:
    raise SystemExit(f"Setup incomplete. Missing {{missing}}. Ask the facilitator.")
print("Ready. Data files:", os.listdir("data"))
'''

# (title, goal_md, prompt, solution_code, checkpoint)
TASKS = [
    (
        "Task 1 - Open and inspect the data",
        """
Goal: load the CSV, check its dimensions, and count participants per group.

Record the dimensions, columns, and group counts before writing an analysis request.
""",
        f"""I'm a researcher using Python in a Google Colab notebook. I am a beginner.

I have a CSV file at `data/transcripts.csv` with these columns:
participant_id, group, age, sex, education_years, months_post_onset, wab_aq, transcript

Each row is one person describing a picture out loud. `group` is either "control" or
"aphasia". `wab_aq` is an aphasia severity score from 0-100 (higher = less impaired).
`transcript` is what they said.

Write Python using pandas to:
1. load the file into a DataFrame called `df`
2. print how many rows and columns it has
3. show the first 3 rows
4. count how many people are in each group

Give me just the code, with short comments. Don't explain it afterwards.""",
        '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load the data
df = pd.read_csv("data/transcripts.csv")

print("rows, columns:", df.shape)
print(df["group"].value_counts())
df.head(3)
''',
        "Expected: 60 rows, 8 columns, and 30 participants per group.",
    ),
    (
        "Task 2 - Read the transcript data",
        """
Goal: print one control transcript and one transcript from the most impaired participant.

Read the source text before constructing quantitative measures from it.
""",
        """Using the same `df`, print the transcript of one control participant, and the
transcript of the participant with aphasia who has the LOWEST wab_aq score.
Label each one clearly so I can tell them apart.""",
        '''
print("--- CONTROL ---")
print(df.query("group == 'control'")["transcript"].iloc[0])

print("\\n--- APHASIA (most impaired) ---")
print(df.query("group == 'aphasia'").sort_values("wab_aq")["transcript"].iloc[0])
''',
        "Compare the source text with the measures constructed in the next task.",
    ),
    (
        "Task 3 - Transparent transcript measures",
        """
Goal: for every transcript compute number of words, number of unique words,
type-token ratio (unique / total), and mean word length.

These measures are defined operations on text. Their interpretation remains an
analytic decision rather than a property of the code.
""",
        """Add four new columns to `df`, one row per participant, computed from the `transcript` column:

- `n_words`: total number of words
- `n_unique_words`: number of unique words
- `type_token_ratio`: n_unique_words / n_words
- `mean_word_length`: average number of characters per word

Lowercase the text and strip periods before splitting on whitespace. Use a function
plus `.apply()` so it's readable. Then show me participant_id, group, wab_aq, n_words
and type_token_ratio for the first 5 rows.""",
        '''
def simple_features(text):
    words = text.lower().replace(".", " ").split()
    return pd.Series({
        "n_words": len(words),
        "n_unique_words": len(set(words)),
        "type_token_ratio": len(set(words)) / max(len(words), 1),
        "mean_word_length": np.mean([len(w) for w in words]),
    })

df = df.join(df["transcript"].apply(simple_features))
df[["participant_id", "group", "wab_aq", "n_words", "type_token_ratio"]].head()
''',
        "Expected group means: control about 110 words and aphasia about 70 words.",
    ),
    (
        "Task 4 - Part-of-speech tagging with spaCy",
        """
Goal: classify words by type, including content words (nouns, verbs, adjectives,
adverbs) versus fillers ("uh", "um", "well").

This task introduces an NLP library. In this workshop, `content_word_ratio` is a
specified token-based measure, not a clinical outcome measure.
""",
        """Now use spaCy (the `en_core_web_sm` model, already downloaded) to add two more
columns to `df`:

- `content_word_ratio`: proportion of tokens tagged NOUN, PROPN, VERB, ADJ or ADV,
  excluding anything in this filler list: uh, um, well, hmm, okay, alright, so
- `filler_rate`: proportion of tokens that ARE in that filler list

Ignore punctuation and whitespace tokens when counting. Then show me the mean of both
columns for each group.""",
        '''
import spacy
nlp = spacy.load("en_core_web_sm")

FILLERS = {"uh", "um", "well", "hmm", "okay", "alright", "so"}
CONTENT_POS = {"NOUN", "PROPN", "VERB", "ADJ", "ADV"}

def pos_features(text):
    doc = nlp(text)
    toks = [t for t in doc if not t.is_punct and not t.is_space]
    n = max(len(toks), 1)
    content = [t for t in toks
               if t.pos_ in CONTENT_POS and t.text.lower() not in FILLERS]
    fillers = [t for t in toks if t.text.lower() in FILLERS]
    return pd.Series({
        "content_word_ratio": len(content) / n,
        "filler_rate": len(fillers) / n,
    })

df = df.join(df["transcript"].apply(pos_features))
df.groupby("group")[["content_word_ratio", "filler_rate"]].mean().round(3)
''',
        "Expected means: controls have content-word ratio about 0.41 and near-zero filler rate; "
        "the aphasia group has content-word ratio about 0.39 and a higher filler rate.",
    ),
    (
        "Task 5 - Plot the group distributions",
        """
Goal: three side-by-side boxplots comparing the groups on words produced,
content-word ratio, and filler rate.

The analytic requirements, rather than plotting syntax, determine whether the figure answers
the intended question.
""",
        """Make one matplotlib figure with three side-by-side boxplots comparing the "control"
and "aphasia" groups on: n_words, content_word_ratio, and filler_rate.

Requirements:
- one subplot per measure, with a readable title on each
- overlay the individual data points with a little horizontal jitter
- colour the control boxes green and the aphasia boxes pink
- remove the top and right spines
- give the whole figure a title
- save it to outputs/python_figure.png at dpi=150

Use `ax.set_xticks` / `ax.set_xticklabels` for the group labels rather than the
`labels=` argument to boxplot, which is deprecated.""",
        '''
fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
for ax, col, label in zip(
    axes,
    ["n_words", "content_word_ratio", "filler_rate"],
    ["Words produced", "Content-word ratio", "Filler rate"],
):
    data = [df.loc[df["group"] == g, col] for g in ["control", "aphasia"]]
    bp = ax.boxplot(data, patch_artist=True, widths=0.55,
                    medianprops=dict(color="black"))
    ax.set_xticks([1, 2]); ax.set_xticklabels(["control", "aphasia"])
    for patch, c in zip(bp["boxes"], ["#4C9F70", "#B5446E"]):
        patch.set_facecolor(c); patch.set_alpha(0.6)
    for i, g in enumerate(["control", "aphasia"], start=1):
        y = df.loc[df["group"] == g, col]
        ax.scatter(np.random.normal(i, 0.05, len(y)), y, s=12, c="black", alpha=0.4, zorder=3)
    ax.set_title(label, fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)

fig.suptitle("Discourse measures by group (synthetic data)", fontsize=13)
fig.tight_layout()
fig.savefig("outputs/python_figure.png", dpi=150)
plt.show()
''',
        "If the first version does not meet the stated requirements, describe the discrepancy and "
        "request a revision. Recheck the revised figure.",
    ),
    (
        "Task 6 - Examine associations within the aphasia group",
        """
Goal: correlate every measure with WAB-AQ within the aphasia group only.

Controls cluster near the upper end of WAB-AQ in this synthetic dataset. Restricting the
analysis to aphasia participants aligns the association with the stated question.
""",
        """Within the aphasia group only, compute the correlation between wab_aq and each of
these five measures: n_words, type_token_ratio, mean_word_length, content_word_ratio,
filler_rate. Print them sorted from most negative to most positive, rounded to 2 dp.""",
        '''
feature_cols = ["n_words", "type_token_ratio", "mean_word_length",
                "content_word_ratio", "filler_rate"]

aph = df.query("group == 'aphasia'")
corrs = aph[feature_cols].corrwith(aph["wab_aq"]).round(2).sort_values()
print("Correlation with WAB-AQ, aphasia group only:")
print(corrs)
''',
        "Expected correlations: `filler_rate` about -0.83 and `n_words` about +0.60. "
        "`type_token_ratio` is close to zero in this synthetic dataset.",
    ),
    (
        "Task 7 (advanced) - Lexical-overlap proxy against a reference description",
        """
Goal: score lexical overlap between each transcript and a complete description of the
picture. This is a transparent proxy for discourse content, not a validated main-concept
analysis.

TF-IDF plus cosine similarity requires no downloads and illustrates one way to compare
texts as vectors. It is not interchangeable with an embedding model or a clinician-scored
discourse measure.
""",
        """I want a measure of how semantically close each transcript is to a complete
description of the scene.

Here is my reference description:

"a boy is standing on a stool reaching into the cookie jar taking cookies the stool is
tipping over his sister reaches up for a cookie the mother stands at the sink washing
dishes the sink is overflowing and water is running onto the floor she does not notice"

Using scikit-learn's TfidfVectorizer (with English stop words removed) and
cosine_similarity, add a column `semantic_similarity` to `df` giving each transcript's
cosine similarity to that reference.

Then print the group means, and the correlation with wab_aq within the aphasia group.""",
        '''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

REFERENCE = (
    "a boy is standing on a stool reaching into the cookie jar taking cookies "
    "the stool is tipping over his sister reaches up for a cookie the mother "
    "stands at the sink washing dishes the sink is overflowing and water is "
    "running onto the floor she does not notice"
)

vec = TfidfVectorizer(stop_words="english")
X = vec.fit_transform(list(df["transcript"]) + [REFERENCE])
df["semantic_similarity"] = cosine_similarity(X[:-1], X[-1]).ravel()

print(df.groupby("group")["semantic_similarity"].mean().round(3))
aph = df.query("group == 'aphasia'")
print("r with WAB-AQ:", round(aph["semantic_similarity"].corr(aph["wab_aq"]), 2))
''',
        "Expected means: control about 0.50 and aphasia about 0.24; the within-aphasia correlation "
        "with WAB-AQ is about +0.82. Interpret this as lexical overlap with this reference, not validated semantic scoring.",
    ),
    (
        "Task 8 (advanced) - Development-only classification from language measures",
        """
Goal: a resampled logistic-regression classifier predicting group from five language
measures. This is a development exercise, not diagnostic-model validation.

The prompt requires resampling because training accuracy is not an evaluation of out-of-sample
performance.
""",
        """Fit a logistic regression that predicts `group` (aphasia = 1, control = 0) from these
five features: n_words, type_token_ratio, mean_word_length, content_word_ratio, filler_rate.

Important: I want a resampled estimate, not training accuracy. Use repeated stratified
5-fold cross-validation. Standardise the features inside a Pipeline so no information
leaks across folds. Report balanced accuracy and ROC-AUC, each as mean (SD), and state
the majority-class chance level.

Print the mean CV accuracy, the standard deviation, and the chance level.""",
        '''
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X = df[feature_cols]
y = (df["group"] == "aphasia").astype(int)

clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=202607)
scores = cross_validate(
    clf, X, y, cv=cv,
    scoring={"balanced_accuracy": "balanced_accuracy", "roc_auc": "roc_auc"},
)

for metric in ["balanced_accuracy", "roc_auc"]:
    values = scores[f"test_{metric}"]
    print(f"{metric}: {values.mean():.2f} (SD {values.std():.2f})")
print("Chance level:", round(max(y.mean(), 1 - y.mean()), 2))
''',
        "Performance should exceed a 0.50 majority-class baseline. The repeated folds are not "
        "an external validation cohort. Ask: *'Which claims would require an independent cohort?'*",
    ),
    (
        "Task 9 - Export features for R",
        """
Goal: write the feature set to a CSV so the R half of the workshop can model it.

This workshop uses Python for text processing and R for the subsequent statistical tasks.
""",
        """Save participant_id plus the five feature columns and semantic_similarity to
`outputs/my_features.csv` (no index column). Print the first few rows to confirm.""",
        '''
out = df[["participant_id"] + feature_cols + ["semantic_similarity"]]
out.to_csv("outputs/my_features.csv", index=False)
print(out.head())
''',
        "`data/features.csv` already ships with the same measures, so the R half "
        "works even if this task wasn't finished. Compare the two files for agreement.",
    ),
]

HEADER_STARTER = f'''
# Part 1 - Python: text measures and a picture-description dataset

### How this notebook works

Minimal Python typing is required. For each task:

1. A goal that specifies the target output
2. A prompt to copy into an AI assistant
3. An empty cell for returned code
4. A checkpoint for verification

On error, copy the full error message and traceback into the same AI conversation. Request the
immediate cause and the smallest correction, then run that correction before continuing.

The data are synthetic and generated by a script. Do not treat the workshop as permission to
enter real participant data into an AI service.
'''

HEADER_SOLUTION = f'''
# Part 1 - Python solution / reference

Working code for every task. Use it to get unstuck, not to bypass the exercise.
'''


def build(starter: bool):
    cells = [md(HEADER_STARTER if starter else HEADER_SOLUTION),
             md("## Setup\n\nRun this cell first."),
             code(SETUP)]
    for title, goal, prompt, sol, check in TASKS:
        cells.append(md(f"---\n## {title}\n\n{goal.strip()}"))
        if starter:
            cells.append(md("Copy this prompt into your AI assistant:\n\n```\n"
                            + prompt.strip() + "\n```"))
            cells.append(code("# paste the AI's code here, then press Shift+Enter to run it\n"))
            cells.append(md(f"> Checkpoint: {check}"))
        else:
            cells.append(code(sol))
            cells.append(md(f"> {check}"))
    if starter:
        cells.append(md(
            "---\n## Done with Python\n\nThis pipeline covered: lexical measures, "
            "POS tagging, a semantic measure, a plot, and a classifier.\n\n"
            "Continue to R for the statistics. Open `r/02_r_starter.R` in Posit Cloud.\n\n"
            "Use `PROMPTS.md` for the verification workflow. The `guardrails/` folder contains "
            "background resources; audit its literature-linked claims before reusing them in a "
            "manuscript, grant, protocol, or methods document."))
    return {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4, "nbformat_minor": 0,
    }


here = pathlib.Path(__file__).parent
for name, is_starter in [("01_python_starter.ipynb", True),
                         ("01_python_solution.ipynb", False)]:
    (here / name).write_text(json.dumps(build(is_starter), indent=1))
    print("wrote", name)
