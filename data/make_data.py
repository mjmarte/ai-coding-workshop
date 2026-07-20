"""Build the synthetic dataset used in the workshop.

Each transcript is generated from templates in this file. The resulting files
support reproducible teaching exercises and are not participant data.

Run:  python data/make_data.py
Makes: transcripts.csv, transcripts_long.csv, features.csv, recovery_prediction.csv
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260713)

# ---------------------------------------------------------------- content units
# Each scene element is rendered at three constructed severity levels.
# Index 0 = intact, 1 = reduced, 2 = limited.
UNITS = [
    ("boy_stool",  ["a little boy is standing on a wooden stool",
                    "the boy is on the stool",
                    "boy uh the... the chair thing"]),
    ("stool_fall", ["the stool is tipping over and he is about to fall",
                    "the stool is falling",
                    "it's uh falling falling over"]),
    ("boy_cookie", ["he is reaching into the cookie jar to take a cookie",
                    "he is taking cookies",
                    "the uh cookie... he take the... that one"]),
    ("girl_reach", ["his sister is standing below him reaching up for a cookie",
                    "the girl wants one too",
                    "and the girl uh... she want it"]),
    ("mother_dish",["the mother is standing at the sink washing the dishes",
                    "the mother is washing dishes",
                    "the lady... the uh... washing the things"]),
    ("sink_over",  ["the sink is overflowing and water is running onto the floor",
                    "the water is spilling on the floor",
                    "water uh water everywhere on the... the floor"]),
    ("mother_obl", ["she does not seem to notice what is happening behind her",
                    "she is not looking at them",
                    "she uh she don't see it"]),
    ("window",     ["through the window you can see the garden and a path outside",
                    "there is a window behind her",
                    "and the uh window there"]),
    ("dishes",     ["there are dishes and a cup on the counter beside her",
                    "some dishes are on the counter",
                    "dishes and uh stuff"]),
    ("curtains",   ["the curtains are open and it looks like a bright day",
                    "the curtains are open",
                    "the uh curtain thing"]),
]

FILLERS = ["uh", "um", "well", "you know", "let's see"]
EMPTY = ["thing", "stuff", "that one", "whatchamacallit", "the whatsit"]
OPENERS = ["okay", "alright", "so", "let me see", "hmm"]


FUNCTION_PAD = ["the", "a", "and", "it's", "is", "that", "there"]


def degrade(sentence, severity, rng):
    """Insert constructed fillers, vague words, and repetitions by severity level."""
    words = sentence.split()
    out = []
    for w in words:
        # Repeat a word.
        if rng.random() < 0.14 * severity:
            out.append(w)
        # Replace a content word with a vague word.
        if rng.random() < 0.06 * severity and len(w) > 4:
            out.append(rng.choice(EMPTY))
        else:
            out.append(w)
        # Add a filler.
        if rng.random() < 0.24 * severity:
            out.append(rng.choice(FILLERS))
        # Add a function-word fragment.
        if rng.random() < 0.12 * severity:
            out.append(rng.choice(FUNCTION_PAD))
    return " ".join(out)


def make_transcript(severity, rng):
    """severity: 0 = unimpaired, 1 = severe."""
    parts = []
    if rng.random() < 0.3 + 0.5 * severity:
        parts.append(rng.choice(OPENERS))
    for _name, variants in UNITS:
        # Higher severity yields fewer constructed scene elements.
        if rng.random() > (1.0 - 0.72 * severity):
            continue
        if severity < 0.25:
            level = 0
        elif severity < 0.60:
            level = int(rng.choice([0, 1], p=[0.35, 0.65]))
        else:
            level = int(rng.choice([1, 2], p=[0.3, 0.7]))
        parts.append(degrade(variants[level], severity, rng))
    if not parts:  # very severe: at least say something
        parts = ["uh", rng.choice(EMPTY), "the uh", rng.choice(EMPTY)]
    if rng.random() < 0.25 + 0.35 * severity:
        parts.append(rng.choice(["that's it", "i think that's all", "that's about it"]))
    return " . ".join(parts).replace(" .", ".").replace("..", ".") + "."


def demographics(n, rng, aphasia):
    return pd.DataFrame({
        "age": np.clip(rng.normal(64 if aphasia else 61, 11, n), 35, 88).round(0).astype(int),
        "sex": rng.choice(["F", "M"], n),
        "education_years": np.clip(rng.normal(15, 2.6, n), 8, 22).round(0).astype(int),
    })


# ------------------------------------------------------------------ build rows
def build():
    n_ctrl, n_aph = 30, 30

    # Controls are constructed with low severity values.
    ctrl_sev = np.clip(RNG.normal(0.04, 0.03, n_ctrl), 0, 0.12)
    ctrl = demographics(n_ctrl, RNG, aphasia=False)
    ctrl["participant_id"] = [f"C{i:03d}" for i in range(1, n_ctrl + 1)]
    ctrl["group"] = "control"
    ctrl["months_post_onset"] = np.nan
    ctrl["wab_aq"] = np.clip(100 - 8 * ctrl_sev + RNG.normal(0, 0.8, n_ctrl), 96, 100).round(1)
    ctrl["transcript"] = [make_transcript(s, RNG) for s in ctrl_sev]

    # Aphasia group at acute assessment, about 1 month post-onset.
    aph_sev = np.clip(RNG.beta(2.2, 2.4, n_aph), 0.08, 0.95)
    aph = demographics(n_aph, RNG, aphasia=True)
    aph["participant_id"] = [f"A{i:03d}" for i in range(1, n_aph + 1)]
    aph["group"] = "aphasia"
    aph["months_post_onset"] = np.clip(RNG.normal(1.1, 0.35, n_aph), 0.4, 2.2).round(1)
    aph["wab_aq"] = np.clip(100 - 66 * aph_sev + RNG.normal(0, 3.5, n_aph), 26, 99).round(1)
    aph["transcript"] = [make_transcript(s, RNG) for s in aph_sev]

    cols = ["participant_id", "group", "age", "sex", "education_years",
            "months_post_onset", "wab_aq", "transcript"]
    baseline = pd.concat([ctrl[cols], aph[cols]], ignore_index=True)

    # ---- longitudinal: the same 30 aphasia participants about 12 months post-onset
    recovery = RNG.uniform(0.45, 0.92, n_aph)           # constructed severity change
    sev_t2 = np.clip(aph_sev * recovery, 0.02, 0.95)
    t1 = aph[["participant_id", "age", "sex", "education_years", "wab_aq",
              "months_post_onset", "transcript"]].copy()
    t1["timepoint"] = "acute"
    t2 = t1.copy()
    t2["timepoint"] = "chronic"
    t2["months_post_onset"] = np.clip(RNG.normal(12.2, 0.9, n_aph), 10, 14).round(1)
    t2["wab_aq"] = np.clip(100 - 66 * sev_t2 + RNG.normal(0, 3.5, n_aph), 28, 100).round(1)
    t2["transcript"] = [make_transcript(s, RNG) for s in sev_t2]
    long = pd.concat([t1, t2], ignore_index=True).sort_values(
        ["participant_id", "months_post_onset"])
    long = long[["participant_id", "timepoint", "months_post_onset", "age", "sex",
                 "education_years", "wab_aq", "transcript"]]

    return baseline, long


def build_recovery_prediction():
    """Synthetic acute stroke cohort for the advanced prediction exercise.

    One row represents one participant. All predictors are available at the
    acute assessment; the 12-month WAB-AQ is the outcome and is excluded from
    the predictor matrix. The values are illustrative, not a clinical model.
    """
    rng = np.random.default_rng(20260714)
    n = 90
    severity = np.clip(rng.beta(2.2, 2.0, n), 0.04, 0.96)

    age = np.clip(rng.normal(64, 10, n), 38, 86).round().astype(int)
    education = np.clip(rng.normal(15, 2.8, n), 8, 22).round().astype(int)
    sex = rng.choice(["F", "M"], n)
    acute_wab = np.clip(100 - 74 * severity + rng.normal(0, 5.5, n), 18, 98).round(1)
    acute_discourse = np.clip(10 - 8.5 * severity + rng.normal(0, 0.9, n), 0, 10).round(1)
    lesion_volume = np.clip(12 + 185 * severity + rng.normal(0, 24, n), 3, 300).round(1)
    cortical_burden = np.clip(8 + 68 * severity + rng.normal(0, 9, n), 0, 100).round(1)
    dorsal_disconnection = np.clip(0.03 + 0.78 * severity + rng.normal(0, 0.10, n), 0, 1).round(3)
    ventral_disconnection = np.clip(0.04 + 0.58 * severity + rng.normal(0, 0.12, n), 0, 1).round(3)

    outcome = (
        20
        + 0.46 * acute_wab
        + 1.25 * acute_discourse
        + 0.20 * education
        - 0.10 * age
        - 0.035 * lesion_volume
        - 5.5 * dorsal_disconnection
        + rng.normal(0, 6.5, n)
    )
    outcome = np.clip(outcome, 20, 100).round(1)

    return pd.DataFrame({
        "participant_id": [f"R{i:03d}" for i in range(1, n + 1)],
        "age": age,
        "sex": sex,
        "education_years": education,
        "acute_wab_aq": acute_wab,
        "acute_discourse_score": acute_discourse,
        "lesion_volume_ml": lesion_volume,
        "cortical_lesion_pct": cortical_burden,
        "dorsal_disconnection_pct": dorsal_disconnection,
        "ventral_disconnection_pct": ventral_disconnection,
        "outcome_wab_aq_12m": outcome,
    })


# -------------------------------------------------- features (the Python answer)
def extract_features(df):
    """Match the feature definitions in python/01_python_starter.ipynb."""
    import spacy
    nlp = spacy.load("en_core_web_sm")
    fillers = {"uh", "um", "well", "hmm", "okay", "alright", "so"}
    content_pos = {"NOUN", "PROPN", "VERB", "ADJ", "ADV"}
    rows = []
    for _, r in df.iterrows():
        text = r["transcript"]
        # Plain whitespace features, matching the notebook.
        words = text.lower().replace(".", " ").split()
        n = max(len(words), 1)
        # Part-of-speech features, matching the notebook.
        doc = nlp(text)
        toks = [t for t in doc if not t.is_punct and not t.is_space]
        m = max(len(toks), 1)
        content = [t for t in toks
                   if t.pos_ in content_pos and t.text.lower() not in fillers]
        fill = [t for t in toks if t.text.lower() in fillers]
        rows.append({
            "participant_id": r["participant_id"],
            "n_words": len(words),
            "n_unique_words": len(set(words)),
            "type_token_ratio": round(len(set(words)) / n, 4),
            "mean_word_length": round(float(np.mean([len(w) for w in words])), 3),
            "content_word_ratio": round(len(content) / m, 4),
            "filler_rate": round(len(fill) / m, 4),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    baseline, long = build()
    recovery = build_recovery_prediction()
    feats = extract_features(baseline)

    # Do not replace any derived file until feature extraction has completed.
    # A missing NLP dependency should leave the existing teaching dataset intact.
    baseline.to_csv("data/transcripts.csv", index=False)
    long.to_csv("data/transcripts_long.csv", index=False)
    recovery.to_csv("data/recovery_prediction.csv", index=False)
    feats.to_csv("data/features.csv", index=False)

    chk = baseline.merge(feats, on="participant_id")
    print(f"{len(baseline)} baseline rows, {len(long)} longitudinal rows")
    print(f"{len(recovery)} acute-to-12-month prediction rows")
    print("\nCorrelations with WAB-AQ in the constructed dataset:")
    for c in ["content_word_ratio", "type_token_ratio", "n_words", "filler_rate"]:
        print(f"  {c:22s} r = {chk['wab_aq'].corr(chk[c]):+.2f}")
    print("\nExample control  :", baseline.query("group=='control'").transcript.iloc[0][:110])
    print("Example mild     :", baseline.query("group=='aphasia' and wab_aq>80").transcript.iloc[0][:110])
    print("Example severe   :", baseline.query("group=='aphasia' and wab_aq<50").transcript.iloc[0][:110])
