# The 1-hour screen-share runbook

**Format:** you drive, on one screen, shared. Nobody else opens a laptop. This file is your
second screen — read it in order, do exactly what it says, say roughly what's in the
`SAY:` blocks. `DO:` blocks are literal clicks/keys. Everything is demoed **inside the
IDE's own AI panel** — no separate chat window, no copy-paste between windows.

**Total: 60 minutes.** Timings are cumulative. If you're behind at the 30-minute mark, skip
straight to §5 (R) — the R section is the strongest material and must not get cut.

---

## Before you go live (do this 15 min before people arrive, not during)

- [ ] Sign into Colab with your Google account (its AI panel requires sign-in — confirmed
      it prompts "Google sign-in required" otherwise).
- [ ] Open `01_python_starter.ipynb` from your repo, confirm it loads, leave the tab open.
- [ ] Open your Posit Cloud project (posit.cloud/content/12671685), confirm `r/02_r_starter.R`
      is there, leave the tab open.
- [ ] **Check RStudio has an in-IDE AI panel enabled.** Posit Cloud's free tier does **not**
      ship GitHub Copilot by default — it requires a Copilot account wired up under
      Tools → Global Options → Copilot. **If you haven't set this up, do it now or fall back
      to a plain browser AI chat tab positioned next to RStudio for the R section** — don't
      discover this live. This is the one real unknown in this plan; verify it today.
- [ ] Font size: bump both Colab and RStudio to at least 16pt (Tools/Global Options → 
      Appearance in RStudio; Ctrl/Cmd + a few times in Colab). If they can't read it from
      the back of the room, none of this works.
- [ ] Close every other tab/app. Turn off notifications. One thing on screen at a time.

---

## 0 · Cold open — 0:00–0:02

DO: Nothing on screen but a blank Colab tab, or your face if on video. No slides yet.

SAY (from SCRIPT.md §0, compressed):
> The bottleneck in research computing was never typing. It was knowing what to type. AI
> removes the typing. It does not remove the knowing — it just makes it possible to skip
> the knowing without noticing you did. That's the whole hour.

---

## 1 · The bad prompt vs. the good prompt — 0:02–0:10

DO: Switch to the Colab tab. Point at the little sparkle/AI icon in the left sidebar (opens
the Gemini panel inside Colab itself — this is "prompting in the IDE").

SAY:
> I'm not going to open a separate chat window today. The AI lives right here, next to your
> code, and that's how you'll actually use it.

DO: In the Colab AI panel, type exactly:
```
write me some code to analyse my data
```
Hit enter. Let it generate. Read the result out loud, pointing at specific invented column
names.

SAY (SCRIPT.md §1):
> It didn't fail. It did exactly what I asked. I gave it nothing, so it filled every blank
> with a confident guess. That's the first law of the day: it fills every blank you leave.
> Your only job is to leave fewer blanks.

DO: Open `data/transcripts.csv` in a second Colab tab (or the Files panel) for 5 seconds so
people see it's a real structured file with real column names. Close it. Back to the AI
panel, type the good prompt:
```
I'm a researcher using Python in Colab. I'm a beginner. I have a CSV at
data/transcripts.csv, one row per person. Columns: participant_id, group ("control" or
"aphasia"), age, sex, education_years, months_post_onset, wab_aq (aphasia severity 0-100,
higher = less impaired), transcript. Load it with pandas, tell me how many rows and
columns, and count the people in each group. Just the code, short comments.
```
DO: Insert the code it returns into a fresh code cell, run it (Shift+Enter). It should print
60 rows, 8 columns, 30/30.

SAY:
> Same tool, thirty seconds later. The only thing that changed is I stopped letting it
> guess. That's most of the skill in this room today — and it's a recipe.

---

## 2 · The recipe — 0:10–0:13

DO: Nothing on screen changes — stay on the working notebook so it's visibly "the thing that
just worked." Talk over it.

SAY (SCRIPT.md §2, compressed to the five words):
> Five ingredients, every time. **Who you are. What the data is. The one task. The
> constraints. The output.** That's it — that's the whole page, and it's in PROMPTS.md if
> you want it later.

*(Skip the "being fair to the tool" aside and the debugging-loop section (old §3) entirely
— no time. If someone hits an error live, handle it in the moment: "paste the whole error
back, ask it to fix it, one error at a time.")*

---

## 3 · Python, fast — 0:13–0:20

DO: In the Colab AI panel, ask it (live, in the IDE) to run the core NLP step:
```
Using the transcripts DataFrame we just loaded, compute a lexical diversity measure
(type-token ratio) and word count per person, and make one scatterplot: word count vs.
type-token ratio, colored by group. Just the code.
```
Run it. Let the plot render. Don't explain every line — this section is "look what it can
do fast," not a Python lesson.

SAY:
> This would've taken you an afternoon a few years ago. Now it's one prompt. Hold onto that
> — because everything after this is about the parts it *can't* do for you.

---

## 4 · The confident lie — 0:20–0:28  ⚠️ never cut

DO: Switch to the Posit Cloud / RStudio tab (or your AI-chat fallback tab, per the setup
checklist above). Open a fresh AI conversation/panel.

DO: Type exactly:
```
I have 30 patients, each measured twice — once at 1 month post-stroke and once at 12
months. I want to know if their language scores improved. Give me the R code.
```
Read whatever comes back. Don't react yet.

DO: Follow up, same panel:
```
Are you sure? What are you assuming about the independence of these observations?
```
Read the correction out loud, slowly.

SAY (SCRIPT.md §4 — this is the center of the talk, don't rush):
> It knew. It knew the whole time. It gave me the wrong answer first anyway, and only told
> me the truth when I poked it. That gap — between what it knows and what it says — is
> where your career gets damaged.

---

## 5 · The two traps that matter — 0:28–0:38 ⚠️ never cut the ceiling one

*(Only two of the original five traps — the ceiling effect and the hidden-effect model.
Both live in `r/02_r_starter.R` / `02_r_solution.R` — have the solution file open in a
second RStudio tab so you can flash real numbers without live-typing a full model.)*

**Trap 1 — the ceiling (SCRIPT.md §5, trap one).**
DO: Show the R console output: pooled R² = 0.70 vs. patients-only R² = 0.36 (pull straight
from `02_r_solution.R` if you don't want to fit it live).

SAY:
> Pool healthy controls in with patients and you get a beautiful R² of .70. Model only the
> patients — the people the question is actually about — and it collapses to .36. The AI
> will happily pool your controls. Only you know they're sitting at a ceiling.

**Trap 2 — the hidden effect (SCRIPT.md §6).**
DO: Show two numbers side by side from the solution file: mixed model t = 5.2 (clear
recovery) vs. naive lm p = 0.056 (not significant).

SAY:
> Same patients, same data. One model says clear recovery. The other says nothing happened.
> The wrong model didn't invent an effect — it hid a real one. Everyone's trained to fear
> the false positive. Nobody trains you to fear the true effect the wrong analysis erases.

---

## 6 · The fabricated paragraph — 0:38–0:48 ⚠️ never cut, this is the punchline

DO: In the RStudio AI panel (in-IDE, same as before), with a real fitted model's output
visible on screen (from `02_r_solution.R`), type:
```
Write the Results paragraph for this linear model in APA style — report the coefficients,
confidence intervals, R-squared, and the F test.
```
Read the paragraph out loud. Sounds great.

DO: Point at the real console output, number by number, hunting for the mismatch (df that
isn't there, a p > .05 called "significant," a flipped sign, an R² it never saw). SCRIPT.md
§7 has the exact hunting language — use it.

SAY:
> It wrote a better paragraph than I would have. And it lied in it. Both of those are true,
> and your job is to hold both.

---

## 7 · Guardrails + close — 0:48–0:58

DO: Switch to the `guardrails/` folder view (just the file list is enough, don't open all
of them).

SAY (compressed from SCRIPT.md §8 — pick 2, not all 4, given time):
> Two rules to leave with. One: never paste real patient data into a chatbot — share the
> schema, not the rows, that's why today's data is fake. Two: every number in a write-up
> gets traced back to real output before you believe it, let alone publish it. Everything
> else — the review checklist, the stats guardrails, a project-rules file you hand the AI
> once — is in the `guardrails/` folder and in your inbox already.

Final line (SCRIPT.md §9, verbatim — don't paraphrase this one):
> You are now the senior author on everything the AI writes for you. So act like it.

## 8 · Questions — 0:58–1:00

Stop talking. Let it sit for a second. Then: "Okay — questions."

---

## What got cut from the full script, and why

- Python Task 4-6 (POS tagging, full plot styling, classifier) — no time; §3 above is a
  single fast pass instead.
- The debugging loop, "three strikes" rule, being-fair-to-the-tool aside — good material,
  cut for time. If a question comes up about errors, answer it live from memory
  (FACILITATOR.md has the gist).
- Three of the five stats traps (content-word-ratio vanishing p-value, type-token-ratio
  confound, regression to the mean) — kept the two most visual/dramatic ones.
- "Where this goes" / agentic tools demo — folded into the close as a one-liner rather than
  a live `claude` terminal demo.

If a question or extra 5 minutes opens up, the content-word-ratio "vanishing p-value" trap
(SCRIPT.md §5, trap two) is the best thing to add back — it's the one with no dramatic
number, which surprises people the most.
