# Facilitator guide

**Format:** 3 hours hands-on, or two 90-minute sessions (split at the Python/R boundary).
**Group size:** works up to ~25. Past that you need a second person circulating.
**You need:** a projector, and a helper who can quietly unstick people while you talk.

> **Short on time?** There's a second way to run this: **[SCRIPT.md](SCRIPT.md)** is a
> word-for-word ~50-minute spoken talk (with the four live demos, no laptops required) that
> delivers the whole thesis in a single seminar slot. Use it standalone, or as the spoken
> spine of the full hands-on day — its three optional HANDS-ON beats expand it back out.
>
> **The artifact attendees keep** is **[guardrails/](guardrails/)** — sourced rules, a
> statistics rubric, a data-privacy guide, a printable review checklist, and a ready-to-paste
> project rules file. Point at it in the last ten minutes; it's the durable half of the day.

---

## The thesis of the workshop

Say this out loud in the first five minutes, and again at the end:

> The bottleneck in research computing was never typing. It was knowing what to type.
> AI removes the typing. It does **not** remove the knowing — it just makes it possible
> to skip the knowing without noticing that you did.

Everything in the three hours is in service of that. You are not teaching Python or R.
You are teaching people to *supervise* a fast, confident, occasionally wrong assistant.

---

## Run of show

| Time | Block | You are doing |
|---|---|---|
| 0:00–0:15 | **Setup triage** | Get every laptop into all three tabs. Do not start until everyone is in. Your helper handles stragglers while you start Block 1. |
| 0:15–0:45 | **The basics** | Slides 1–10. The prompt recipe. Two live demos (below). |
| 0:45–1:30 | **Python + NLP** | They work through `01_python_starter.ipynb`. You circulate. |
| 1:30–1:40 | **Break** | |
| 1:40–2:30 | **R + stats + ggplot** | They work through `02_r_starter.R`. |
| 2:30–2:50 | **The fact-check** | Task 7. Do this one together, on the projector. It's the punchline. |
| 2:50–3:00 | **Where this goes** | Agentic tools demo. Guardrails. Questions. |

Timing reality: the Python block always runs 10 minutes long. Steal it from the stretch
tasks (7 and 8), which are explicitly optional.

---

## The two live demos in Block 1

Do these on the projector, in a chat window, live. Do not use slides for them.

**Demo 1 — the bad prompt.** Type, deadpan:

> *write me some code to analyse my data*

Read the answer out loud. It invents a dataframe, invents column names, invents a
research question. Let the room laugh. Then say: *"It didn't fail. It did exactly what I
asked. I asked for nothing."*

Now do it properly, using the recipe from the slide — paste the real column names, one
task, a constraint, an output format. Run the code it gives you. It works. The contrast
does the teaching; you don't have to.

**Demo 2 — the confident lie.** This is the one they'll remember.

Paste this into the chat:

> I have 30 patients, each measured twice — once at 1 month post-stroke and once at 12
> months. I want to know if their language scores improved. Give me the R code.

Roughly half the time you get a paired t-test (correct, if unambitious). The other half
you get something that ignores the pairing, or an independent-samples test, or an lm()
with no random effect. **Whichever you get, ask it the follow-up:**

> Are you sure? What are you assuming about the independence of these observations?

Watch it change its answer. Say: *"It knew. It always knew. It just doesn't lead with it.
That gap — between what it knows and what it says — is where your career gets damaged."*

If it happens to nail the first answer, that's fine. Say so honestly, then ask it for a
Results paragraph with numbers and watch it invent a df. It will.

---

## Traps planted in the materials

These are deliberate. Don't fix them, teach them.

| Where | The trap | What to say |
|---|---|---|
| Python Task 6 | Pooling all 60 people inflates `n_words` from **R² = .36 to R² = .70** — controls are all at WAB ceiling, so half your 'explained variance' is just group membership | *"The AI will happily pool your controls. Only you know they're at ceiling."* |
| R Task 4 | `content_word_ratio`: **p = .004** on its own, **p = .055** in the multiple regression once `n_words` is in it | *"Nothing errored. Nothing warned you. Your headline finding just became a footnote and the code ran fine."* |
| R Task 4 / data | `type_token_ratio` is confounded with transcript length, and impaired speakers produce shorter transcripts | *"This is a 40-year-old known problem in this literature. The model has read every one of those papers and still won't mention it."* |
| R Task 6 | 60 rows, 30 people. The correct `lmer` gives **t = 5.2** — a clear effect. The naive `lm` gives **p = .056** — no effect. | *"The wrong model didn't invent an effect. It HID one. You'd have written 'no significant improvement' and been wrong."* |
| R Task 7 | The AI-written Results paragraph will contain at least one number that isn't in the output | This is the ending. Do it on the projector. |

---

## Task 7 — how to run the punchline

Get one volunteer to project their screen. Ask the AI for the APA Results paragraph.
Then put the real `tidy()` and `glance()` output next to it and go through the prose
**number by number**, out loud, with the room. Ask: *"where does this df come from?"*

You are looking for at least one of:

- a degrees-of-freedom value that appears nowhere in the output
- a significance claim about a predictor with p > .05
- a sign flip
- an R² it never saw

You will find one. If you somehow don't, run it again with a different model — but in
testing this, three of four attempts produced at least one fabricated number.

Close with: *"It wrote a better paragraph than I would have. And it lied in it. Both of
those are true, and you have to hold both."*

---

## Where people get stuck (in order of frequency)

1. **Working directory.** `stopifnot(dir.exists("data"))` fails in R. Fix:
   Session → Set Working Directory → To Project Directory.
2. **They forgot to hit "Save a Permanent Copy"** on Posit Cloud, and lose everything.
   Say it three times during setup. It is the single most common disaster.
3. **The AI gives them code that redefines `df` and wipes their earlier columns.** Teach
   the fix once, publicly: *tell it what columns already exist.*
4. **spaCy model not downloaded** in Colab. The setup cell handles it, but if they
   skipped the setup cell: `!python -m spacy download en_core_web_sm`
5. **They paste the code but not the imports.** The AI omits `import pandas as pd`
   because it assumes context. Teach: *"say 'include all imports' in the prompt."*
6. **Someone's institution blocks Colab or Posit Cloud.** Phone hotspot. Or pair them
   with a neighbour — pairing is good for this workshop anyway.

---

## The last 10 minutes

Show them where this goes, briefly. Don't teach it — just show it, so they know it exists:

- **In-IDE assistants.** Colab's built-in Gemini panel; GitHub Copilot in RStudio.
  Same skill, less copy-pasting.
- **Agentic tools.** Open a terminal, run `claude` in a project folder, and give it the
  whole task at once — *"read data/transcripts.csv, compute lexical measures, fit the
  model, make the figure."* Let it run. It will do in ninety seconds what took them
  ninety minutes. Then say the important part: **they can now read what it did, and tell
  whether it's right. That is the entire difference between a tool and a liability.**
- Point them at `PROMPTS.md`. That's the artifact they keep.

Final slide, final line: *"You are now the senior author on everything the AI writes for
you. Act like it."*

---

## Making the workshop yours

The dataset is aphasia discourse because that's the lab. Swap it out and nothing else
changes: replace `data/*.csv`, update the column descriptions in the prompts inside the
starter files, and the entire structure still works. `data/make_data.py` shows how the
synthetic data was built if you want to generate your own — which is also the honest
answer to *"can I use my real data for this?"* **No. Generate a synthetic twin of it.**
