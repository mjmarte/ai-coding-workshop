"""Generates 01_python_starter.ipynb and 01_python_solution.ipynb."""
import json, pathlib

REPO = "mjmarte/ai-coding-workshop"   # <- find/replace after you create the repo

# NOTE: Jupyter/Colab concatenate the `source` list with NO separator, so every
# element must keep its own trailing "\n". splitlines(keepends=True) does exactly
# that (the final line correctly has no trailing newline). Using a plain
# split("\n") here silently fuses every line onto one — the bug that used to make
# the setup cell an inert comment and the solution code a SyntaxError.
def md(t):   return {"cell_type": "markdown", "metadata": {},
                     "source": t.strip().splitlines(keepends=True)}
def code(t): return {"cell_type": "code", "metadata": {}, "execution_count": None,
                     "outputs": [], "source": t.strip("\n").splitlines(keepends=True)}

SETUP = f'''
# =====================================================================
#  RUN FIRST. Takes ~30 seconds. Wait for the "Ready." line below.
# =====================================================================
# Understanding this cell is not required. Click the play button on the
# left (or press Shift+Enter) and wait. "Ready." confirms setup is complete.
import os, sys, subprocess

REPO = "{REPO}"   # facilitator fills this in before the workshop

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
    raise SystemExit(f"Setup incomplete — missing {{missing}}. Ask the facilitator.")
print("Ready. Data files:", os.listdir("data"))
'''

# (title, goal_md, prompt, solution_code, checkpoint)
TASKS = [
    (
        "Task 1 — Open the data and look at it",
        """
**Goal:** load the CSV, check its dimensions, and count participants per group.

Never model data you haven't looked at. This is step one of every analysis.
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
        "Expected: **60 rows, 8 columns**, 30 participants per group.",
    ),
    (
        "Task 2 — Read some actual transcripts",
        """
**Goal:** print one control transcript and one transcript from the most impaired participant.

Before building measures of *language*, read the language itself.
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
        "Note the fillers, repeated words, and vague nouns — these are what "
        "the next task quantifies.",
    ),
    (
        "Task 3 — Your first NLP measures (no fancy library needed)",
        """
**Goal:** for every transcript compute: number of words, number of unique words,
type-token ratio (unique / total), and mean word length.

These four measures are arithmetic, not machine learning — much of useful
research NLP is. Reserve heavier tools for when they're actually needed.
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
        "Controls should average around 110 words; the aphasia group, around 70.",
    ),
    (
        "Task 4 — Part-of-speech tagging with spaCy",
        """
**Goal:** classify words by type — content words (nouns, verbs, adjectives,
adverbs) versus fillers ("uh", "um", "well").

This is the first measure requiring a proper NLP library. `content_word_ratio`
is a standard index of speech informativeness.
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
        "Controls: content-word ratio ≈ 0.41, near-zero fillers. "
        "Aphasia: content ≈ 0.39, filler rate substantially higher.",
    ),
    (
        "Task 5 — Plot it",
        """
**Goal:** three side-by-side boxplots comparing the groups on words produced,
content-word ratio, and filler rate.

A good task for AI assistance — matplotlib syntax is rarely worth memorizing.
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
        "If the first attempt is ugly, don't fix it by hand — describe the problem "
        "to the AI and ask again. That iteration is the skill being practiced.",
    ),
    (
        "Task 6 — Which measure actually tracks severity?",
        """
**Goal:** correlate every measure with WAB-AQ, **within the aphasia group only**.

Controls sit near ceiling (~99) on the WAB. Pooling groups would manufacture a
correlation out of the group difference rather than a real severity relationship.
An AI assistant will not flag this — the analyst has to.
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
        "`filler_rate` should come out around **-0.83** and `n_words` around **+0.60**. "
        "`type_token_ratio` is nearly flat — this returns in the R portion.",
    ),
    (
        "Task 7 (advanced) — Narrative-content proxy against a reference description",
        """
**Goal:** score lexical overlap between each transcript and a complete description of the
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
        "Controls ≈ 0.50, aphasia ≈ 0.24, and r ≈ **+0.82** with WAB-AQ. "
        "Interpret this as lexical overlap with this reference, not as validated semantic scoring.",
    ),
    (
        "Task 8 (advanced) — Development-only classification from language measures",
        """
**Goal:** a resampled logistic-regression classifier predicting group from five language
measures. This is a development exercise, not diagnostic-model validation.

An AI assistant will readily produce a model with **no cross-validation** and a
suspiciously high accuracy, without flagging the omission.
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
        "Task 9 — Hand off to R",
        """
**Goal:** write the feature set to a CSV so the R half of the workshop can model it.

A common research pattern: Python for text processing, R for statistics.
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
# Part 1 — Python: text, NLP, and a picture-description dataset

### How this notebook works

Minimal Python typing is required. For each task:

1. **A goal** — the target output
2. **A prompt** — copy it into your AI assistant (Claude, ChatGPT, or Colab's built-in Gemini)
3. **An empty cell** — paste the code it returns, run it, check the result
4. **A checkpoint** — the expected output, for verification

On error: **copy the full error message back to the AI** and say
*"this is the error I got, fix it."* That loop accounts for most of the workflow.

The data is **synthetic**, generated by a script, not drawn from real patients.
Nothing entered into a chatbot today is protected health information.
'''

HEADER_SOLUTION = f'''
# Part 1 — Python — SOLUTION / REFERENCE

Working code for every task. Use it to get unstuck, not to bypass the exercise.
'''


def build(starter: bool):
    cells = [md(HEADER_STARTER if starter else HEADER_SOLUTION),
             md("## Setup\n\nRun this cell first."),
             code(SETUP)]
    for title, goal, prompt, sol, check in TASKS:
        cells.append(md(f"---\n## {title}\n\n{goal.strip()}"))
        if starter:
            cells.append(md("**Copy this prompt into your AI assistant:**\n\n```\n"
                            + prompt.strip() + "\n```"))
            cells.append(code("# paste the AI's code here, then press Shift+Enter to run it\n"))
            cells.append(md(f"> **Checkpoint.** {check}"))
        else:
            cells.append(code(sol))
            cells.append(md(f"> {check}"))
    if starter:
        cells.append(md(
            "---\n## Done with Python\n\nThis pipeline covered: lexical measures, "
            "POS tagging, a semantic measure, a plot, and a classifier.\n\n"
            "**Continue to R** for the statistics — open `r/02_r_starter.R` in Posit Cloud.\n\n"
            "Retain the `guardrails/` folder: the sourced rules, the statistics rubric, "
            "the data-privacy guide, and a one-page review checklist for vetting any AI "
            "analysis before trusting its numbers. Consult it when working with real data."))
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
