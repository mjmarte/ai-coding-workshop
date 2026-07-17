"""
make_data.py — builds the SYNTHETIC dataset used in the workshop.

Nothing in here is real patient data. Every transcript is generated from
templates by the code below. That is deliberate: the whole point of the
workshop is that you can practice AI-assisted coding without ever pasting
protected health information into a chatbot.

Run:  python data/make_data.py
Makes: transcripts.csv, transcripts_long.csv, features.csv
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260713)

# ---------------------------------------------------------------- content units
# Each "main concept" of the Cookie Theft / Modern Cookie Theft scene, rendered
# at three levels of degradation. Index 0 = intact, 1 = reduced, 2 = fragmented.
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
    """Insert fillers, empty words and repetitions in proportion to severity."""
    words = sentence.split()
    out = []
    for w in words:
        # repeat a word (perseveration / self-correction)
        if rng.random() < 0.14 * severity:
            out.append(w)
        # swap a content word for a vague, low-information word
        if rng.random() < 0.06 * severity and len(w) > 4:
            out.append(rng.choice(EMPTY))
        else:
            out.append(w)
        # hesitation filler
        if rng.random() < 0.24 * severity:
            out.append(rng.choice(FILLERS))
        # stranded function word (false start)
        if rng.random() < 0.12 * severity:
            out.append(rng.choice(FUNCTION_PAD))
    return " ".join(out)


def make_transcript(severity, rng):
    """severity: 0 = unimpaired, 1 = severe."""
    parts = []
    if rng.random() < 0.3 + 0.5 * severity:
        parts.append(rng.choice(OPENERS))
    for _name, variants in UNITS:
        # more severe -> fewer main concepts produced
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

    # controls: essentially no impairment
    ctrl_sev = np.clip(RNG.normal(0.04, 0.03, n_ctrl), 0, 0.12)
    ctrl = demographics(n_ctrl, RNG, aphasia=False)
    ctrl["participant_id"] = [f"C{i:03d}" for i in range(1, n_ctrl + 1)]
    ctrl["group"] = "control"
    ctrl["months_post_onset"] = np.nan
    ctrl["wab_aq"] = np.clip(100 - 8 * ctrl_sev + RNG.normal(0, 0.8, n_ctrl), 96, 100).round(1)
    ctrl["transcript"] = [make_transcript(s, RNG) for s in ctrl_sev]

    # aphasia, acute (~1 month post-onset)
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

    # ---- longitudinal: the same 30 aphasia participants ~12 months post-onset
    recovery = RNG.uniform(0.45, 0.92, n_aph)           # multiplicative severity change
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


# -------------------------------------------------- features (the Python answer)
def extract_features(df):
    """Must match python/01_python_starter.ipynb exactly, so attendees can
    compare their own numbers against features.csv and get the same answer."""
    import spacy
    nlp = spacy.load("en_core_web_sm")
    fillers = {"uh", "um", "well", "hmm", "okay", "alright", "so"}
    content_pos = {"NOUN", "PROPN", "VERB", "ADJ", "ADV"}
    rows = []
    for _, r in df.iterrows():
        text = r["transcript"]
        # simple features: plain whitespace split (same as the notebook)
        words = text.lower().replace(".", " ").split()
        n = max(len(words), 1)
        # POS features: spaCy tokens (same as the notebook)
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
    baseline.to_csv("data/transcripts.csv", index=False)
    long.to_csv("data/transcripts_long.csv", index=False)

    feats = extract_features(baseline)
    feats.to_csv("data/features.csv", index=False)

    chk = baseline.merge(feats, on="participant_id")
    print(f"{len(baseline)} baseline rows, {len(long)} longitudinal rows")
    print("\nCorrelations with WAB-AQ (should be strong — that's the point):")
    for c in ["content_word_ratio", "type_token_ratio", "n_words", "filler_rate"]:
        print(f"  {c:22s} r = {chk['wab_aq'].corr(chk[c]):+.2f}")
    print("\nExample control  :", baseline.query("group=='control'").transcript.iloc[0][:110])
    print("Example mild     :", baseline.query("group=='aphasia' and wab_aq>80").transcript.iloc[0][:110])
    print("Example severe   :", baseline.query("group=='aphasia' and wab_aq<50").transcript.iloc[0][:110])
