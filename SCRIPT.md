# The spoken script

*Word-for-word, ~50 minutes out loud. This is the talk-with-live-demos version of the
workshop — deliverable in a single 45–55 minute slot. `[Stage directions are in brackets;
you don't say them.]` Lines in **bold** are the ones to slow down and land. Lines like
`> this` are what you type into the AI or read off the screen.*

**How to use this:** Read it aloud once at home with a timer — that's the only way to trust
the timing. The pure talking runs ~40 minutes at an unhurried, emphatic pace; the four live
demos and natural pauses push it to roughly **46–52 minutes as delivered** — inside the
window with margin at both ends. (The per-section clocks below are cumulative and *include*
demo time; a brisk delivery lands near 45, an unhurried one near 55.) The demos are the spine
— if you're tight, the demos stay and you trim the storytelling around them. Three optional **HANDS-ON** beats are marked in the
text: leave them out for a clean 50-minute talk, open them up if you have two hours and want
laptops involved.

**You need on screen:** one AI chat window (Claude or ChatGPT), large font, and the `data/`
folder open in a second tab. That's it. No slides required — though there's a deck in
`slides/` if you want one.

---

## 0 · Cold open ⏱ 0:00–0:04

[Don't introduce yourself yet. Don't do housekeeping. Start cold, while people are still
settling. Say it plainly, and mean it.]

Here's the whole workshop in one sentence, and if you have to leave after the first four
minutes you'll still have gotten your money's worth:

**The bottleneck in research computing was never typing. It was knowing what to type.**

Think about what actually stopped you, all these years, from doing your own analysis. It
wasn't the statistics — you understand your design better than any programmer ever will. It
was the *syntax*. The comma in the wrong place. The bracket that wouldn't close. The name of
the function you could never remember. A wall of punctuation between you and the thing you
already knew how to think about.

That wall is gone. As of about two years ago, an AI assistant will write the code for you,
in seconds, and — this is the uncomfortable part — it will mostly be *good* code. Better than
what a lot of us were writing by hand.

[Beat. Let that be a small relief. Then take it back.]

So here's the problem, and it's the reason we're all in this room. AI removed the typing. **It
did not remove the knowing.** It just made it possible to skip the knowing — to go from a
question straight to a published result — *without noticing that you skipped it.* The gap
didn't close. It went invisible.

I'll give you the version that keeps me up at night. It is not that the AI will hand you
something broken. Broken you'd catch — it errors, it turns red, you go get help. The thing
that will end up in your paper is the code that runs **perfectly** and answers a slightly
different question than the one you asked. No error. No warning. A clean green checkmark and
a wrong number.

[Beat.]

So today is not a Python class. It is not an R class. **Today is about how to supervise a
fast, confident, occasionally wrong collaborator who has read every paper in your field and
understood none of them.** By the end of this hour you will have watched it lie to me — in
APA format, with a confidence interval, with a completely straight face — and, more
importantly, you'll know exactly how to catch it doing it.

[Now, one sentence: who you are, why you're the person saying this. Then move.]

---

## 1 · The bad prompt ⏱ 0:04–0:10

[Go to the chat window. Everyone can see it. Type this live, deadpan. Actually type it — the
live-ness is the whole point.]

Let me show you the single most common way researchers actually use these tools. I'm not
going to show you an expert prompt. I'm going to type what people really type at 9pm when
they're behind on a paper.

> write me some code to analyse my data

[Hit enter. Let it generate. Narrate the answer out loud as it streams — point at the screen.]

Now watch what it does, because it's remarkable. It invented a dataset — see, it's made up
something called `df`. It invented column names I never gave it. It picked a research
question for me — it decided I want a t-test comparing two groups. It's writing analysis code
for data that does not exist anywhere in the universe.

[Let the room laugh. Then, not unkindly — this is a real teaching point, not a joke:]

And here's what I want you to sit with. **It didn't fail.** It did precisely what I asked. I
gave it nothing — "my data," "analyse" — so it filled every single blank I left with a
confident guess. And it will *always* do that. It never comes back and says "I need more
information." It cannot stand a blank. It fills it and moves on, smiling.

**That is the first law of this entire day: the AI fills every blank you leave with a
confident guess. Your only job is to leave fewer blanks.** Every hallucinated column name,
every wrong test, every invented number you'll see today — trace it back and it started as a
blank you didn't know you left.

[Now do it properly. Open `data/transcripts.csv` in the other tab so they can see it's a real,
structured thing.]

So let me stop making it guess. This is our data for today — it's synthetic, generated by a
script, but it's shaped exactly like a real aphasia dataset. Sixty people describing a
picture out loud: thirty with aphasia after a stroke, thirty healthy controls. For each one
we've got their age, a severity score, and the transcript of what they said. Same task as
before — but this time I'm going to hand the AI a brief instead of a wish.

> I'm a researcher using Python in Colab. I'm a beginner. I have a CSV at
> `data/transcripts.csv`, one row per person. Columns: participant_id, group
> ("control" or "aphasia"), age, sex, education_years, months_post_onset, wab_aq
> (aphasia severity 0–100, higher = less impaired), transcript. Load it with pandas,
> tell me how many rows and columns, and count the people in each group. Just the code,
> short comments.

[Run whatever it gives you. It works — 60 rows, 8 columns, 30 per group.]

Same tool. Same thirty seconds. The only thing that changed between the disaster and the
clean result is that I stopped letting it guess what my data looks like. **The distance
between those two prompts is most of the skill in this room today.** And it's a recipe — the
same five ingredients every time. Let me give it to you.

---

## 2 · The recipe ⏱ 0:10–0:15

[This is the one thing worth having them physically write down. Say that.]

If you write down one thing today, write this. A bad prompt is a wish. A good prompt is a
**brief**. Five parts, and I'll tell you what breaks if you drop each one.

**One — who you are.** "I'm a beginner using R in RStudio." One sentence. This sets the
altitude of the answer. Leave it out and it either explains like you've got a computer
science degree, or it assumes you know what a random intercept is and skips the thing you
needed. Tell it who it's talking to.

**Two — what the data is.** The actual column names, pasted straight in. This is the most
important ingredient and the one people always skip. *Every* hallucinated variable name in
the history of these tools comes from the AI guessing at a structure you never showed it. If
you show it the structure, it stops guessing. Copy your column names in. Every time.

**Three — the one task.** One. Singular. "Fit a linear model predicting severity from age."
Not "analyse my data, make some plots, and tell me what's interesting" — that's three
requests and a wish, and you'll get a shallow pass at all three. One clear task gets one good
answer.

**Four — the constraints.** "Use the tidyverse, not base R. Don't install anything new.
Include all the imports." That last one matters more than it sounds — the AI constantly
leaves out the `import pandas` or the `library(dplyr)` line because it assumes you've already
got it, and then your code fails on line one for no reason you can see. Tell it: include
everything.

**Five — the output you want.** "Just the code, with short comments. No essay." Otherwise you
get four paragraphs of explanation wrapped around the six lines you actually needed.

[Land it.]

Who you are. What the data is. The one task. The constraints. The output. There's a one-page
version of this in the file called PROMPTS.md, and honestly, that page is the thing you'll
still be using six months from now when you've forgotten my name. **The recipe is not the
clever part. It's the boring part that makes the clever parts possible.**

[Now be fair to the tool. You've been hard on it and you're about to be harder. Balance it,
because a room that leaves terrified just stops using it, and that's the wrong lesson.]

And let me be fair to it for a minute, because I'm going to spend most of this hour telling
you how it lies, and that's not the whole story — if it were, none of us would bother. There
are things this tool is genuinely, spectacularly good at, and you should use it for all of
them without guilt. **Making a figure publication-ready** — nobody on earth remembers the
ggplot incantation for a colourblind-safe palette and a 300-dpi export, and you never should;
that's exactly what to hand off. **Explaining code you inherited** — you open a script from a
former grad student who left no comments and it's four hundred lines of nothing; paste it in
and say "walk me through this in plain language and flag anything that looks like a bug," and
it's like having the author back in the room. **The boilerplate** — reshaping data, renaming
columns, the fiddly plumbing that used to eat an afternoon. For all of that, it is a
tireless, brilliant assistant and you should lean on it hard. The trouble starts — and this is
the whole rest of the talk — the moment the task shifts from *typing* to *judgement*. It's a
phenomenal typist. It is a treacherous statistician. Learn which one you're asking for.

[OPTIONAL HANDS-ON — +10 min. Cut for the 50-minute talk. If you want laptops involved, this
is the natural spot: everyone opens the Colab notebook, runs the setup cell, and does Task 1
with the recipe. Circulate with a helper. The single most common snag is that someone didn't
run the setup cell first, so nothing else works — check that first, every time.]

---

## 3 · The debugging loop ⏱ 0:15–0:19

[Before the scary stuff, give them the one skill that makes them self-sufficient. Beginners
panic at errors; reframe the error as the normal state.]

Before I show you the ways this goes wrong, I have to tell you the truth about what using
these tools actually feels like day to day, because nobody warns you and then you think
you're bad at it. Here it is: **most of the time, the first thing the AI gives you will not
run.** It'll throw an error. And that is not failure. That is not you being a bad programmer.
**That is the normal, expected, everyday state of this work.** The loop of "try it, it breaks,
paste the error back, fix it, try again" — that loop *is* the job. It's 80% of the job. Real
programmers live in that loop all day long.

So here's how to run the loop well, because there's a right way and a way that wastes your
afternoon.

When something breaks, paste the **whole** error back to the AI. Not your summary of it — not
"it says something about a type." The whole thing, every line of it, including the ugly
traceback that looks like nonsense. Those line numbers are exactly what it needs. Paste it
all and say "this is the error I got, fix it."

Fix **one** error at a time. Re-run. Next error. People try to fix five at once and lose the
thread — one at a time is faster even though it feels slower.

And the rule that saves you when you're truly stuck — I call it three strikes. **If it fails
three times on the same error, stop.** It's stuck in a groove, and every message you send is
digging the groove deeper, because now it's staring at all its own failed attempts and
getting more confused. Open a brand-new chat. Describe the goal from scratch. Do *not* paste
the failed history. A fresh, clean context beats more arguing, every single time. A blank
page is a feature.

[Quick aside, worth it:]

That's true of *any* stuck conversation with these tools, by the way, not just errors. When
it's confidently going in circles, the answer is almost never a longer argument. The answer
is a new chat.

---

## 4 · The confident lie ⏱ 0:19–0:28

[This is the one they'll remember. Slow way down. Open a new, clean chat — fresh context
matters here.]

Now the thing that should scare you a little. Not because the AI is stupid — it isn't. Because
it's *smart*, and it does this anyway.

I'm going to give it a completely ordinary rehab research scenario. The kind you'd actually
have. Watch closely.

> I have 30 patients, each measured twice — once at 1 month post-stroke and once at 12
> months. I want to know if their language scores improved. Give me the R code.

[Run it. Read what you got. About half the time you get a paired t-test — which is correct.
The other half it ignores the pairing, or runs an independent-samples test, or fits a linear
model with no random effect. Whatever you got, don't react yet. Just ask the follow-up.]

Okay. Now, before I run a single line of that, I'm going to ask it one question. And I want
you to memorize this question, because it's the one you ask about every analysis it ever
hands you, for the rest of your career.

> Are you sure? What are you assuming about the independence of these observations?

[Watch it revise its answer. It will now explain that the two measurements come from the same
person, that they are therefore not independent, that you have to account for the
within-person correlation — with a paired test or a mixed-effects model. Read its correction
out loud, slowly.]

[Now stop. This is the center of the whole workshop. Don't rush it.]

Look carefully at what just happened, because it is the most important thing I'll show you all
day. **It knew.** It knew those observations weren't independent. It knew from the very first
word. It had that knowledge the entire time — and it gave me the wrong answer first anyway,
and only told me the truth when I happened to poke it.

Let me put it in plain language, because "independence" is jargon and this matters too much
to leave in jargon. When you measure the same person twice, those two numbers are not two
independent facts about the world. They're two facts about *Bob*. Bob who talks a lot in
January talks a lot in December too — that's just Bob. If your analysis pretends Bob's two
measurements are the same as measurements from two different strangers, it's counting Bob
twice and calling it evidence. Thirty people become sixty people who don't exist. And the
statistics that come out the other end are a lie — a confident, well-formatted lie.

The AI knew all of that. It just didn't *lead* with it.

[This is the line. Land it hard.]

**That gap — between what the model knows and what it says — that is where your career gets
damaged.** Not because it's ignorant. Because it's *agreeable*. It answers the question you
asked, in the shape you asked it, and it saves the crucial caveat for the moment you happen to
ask "are you sure." **And if you never ask — you never find out.** You just publish.

[If your very first answer happened to be correct, say so honestly — it does happen — and
pivot: "It got that one right; it does, sometimes. So let me show you a different one it won't
get right —" and ask it for a Results paragraph with real numbers, and watch it invent a
degrees-of-freedom. There is always a lie somewhere in the session. Your job on stage is to
go find the one it's telling today.]

And I don't want you to think this is just my personal paranoia, so let me give you the
study. Researchers at Stanford ran a controlled experiment — people writing code, half with
an AI assistant, half without. Two findings. First, the people *with* the AI wrote *less*
secure, buggier code. That's bad, but it's not the scary part. The scary part is the second
finding: the people with the AI were **more confident that their code was correct.** The tool
didn't just make them wrong. **It made them sure.** It handed them a wrongness that felt like
competence.

And there was one group that did well — the people who *trusted the AI least* and kept
interrogating it, kept refining, kept asking "are you sure." **So the correct posture toward a
confident AI answer is not trust. It is more skepticism, not less.** I know that feels
backwards. It is the entire job. The moment it sounds most authoritative is exactly the moment
to slow down.

---

## 5 · The traps you can't see ⏱ 0:28–0:37

[Now the statistics, told as stories. This is where your domain expertise earns the room.
Keep the data or a scatter on screen. No laptops needed — you're narrating.]

Let me show you three traps that are living inside this dataset right now. All three run
perfectly. None of them errors. None of them warns you. And an AI will lead you into all three
while being nothing but helpful. These aren't exotic. These are Tuesday.

**Trap one — the ceiling.** [Point at the groups.] Remember our sixty people: thirty controls,
thirty patients. The controls all score around 99 out of 100 on the aphasia quotient — they're
healthy, they're at the ceiling of the test, that's what "control" means. The patients are
spread all the way from 26 to 99.

Now I ask a perfectly reasonable question: does the number of words a person produces predict
how severe their aphasia is? And I let the AI model all sixty people together. It gives me a
gorgeous result — **an R-squared of 0.70.** Seventy percent of the variance explained. That's
a career-making number. You'd write it up tonight.

But watch. If I model only the *patients* — the people the question is actually about — that
R-squared collapses to **0.36.** Half of it just evaporated.

[Beat. Let them wonder where it went.]

Where did the other half go? It was never real. When you pool a group jammed against the
ceiling together with a group that's spread out, the "correlation" you get is really just the
gap *between* the two groups, wearing a correlation's clothes. You didn't discover that words
predict severity. You rediscovered that patients are different from healthy controls — which,
respectfully, you knew before you started.

Here's the point: **the AI will cheerfully pool your controls into that model. Only you know
they're at the ceiling.** That fact isn't in the data it can see. It's in your head, in your
understanding of the test. This is the whole thesis — the knowing it can't do for you.

**Trap two — the finding that quietly disappears.** This one's even sneakier, because there's
no dramatic number. In this data there's a measure called content-word ratio — basically, how
much of someone's speech is real content, nouns and verbs, versus filler and "um." On its own,
it predicts severity beautifully. p equals **0.004.** A real, solid effect. Your headline.

Then you do the responsible thing — the thing good training tells you to do. You build a proper
model with several predictors at once: content-word ratio, plus number of words, plus
vocabulary diversity, plus age. Control for things, like a grown-up.

And content-word ratio's p-value slides from 0.004 to **0.055.** It crossed the line. Your
headline just became a footnote. And here's the part I need you to feel: **nothing errored.
Nothing warned you.** What happened is that "number of words" is related to content-word ratio,
so when they're both in the model they split the credit, and neither one clears the bar
anymore. The code ran green. Your finding dissolved in complete silence. You would only catch
this if you were looking at the actual numbers and thinking about what they mean — which the AI
will never do for you.

**Trap three — the forty-year-old confound.** One of our measures is type-token ratio — unique
words divided by total words, a classic index of vocabulary diversity. It looks useful. It is a
trap, and it's been a *known* trap in this literature since 1987, before some of us were born.

The problem: type-token ratio drops, mechanically, as a transcript gets longer — more words
means more repetition, so the ratio falls automatically. Now, who produces the shortest
transcripts? The most impaired patients. So the measure fights itself: the people with genuinely
richer vocabulary produce more words and therefore score *lower* on the diversity measure. In
our data, the correlation between that "diversity" score and transcript length is minus 0.41.
It's not measuring diversity. It's measuring length in a lab coat.

Forty years this has been in the aphasiology journals. The model has read every one of those
papers. **And it will not say a word about it unless you ask.** But ask it — "hey, is this
measure confounded with sample length?" — and out comes a flawless answer about moving-average
type-token ratio and all the standard corrections. It knew. Same as the independence thing. It
always knows. It just never leads with it.

[Pull the lesson up out of the three stories:]

Notice the shape all three share. In every case the code was perfect and the *understanding* was
missing — and the understanding was the part only you have. Which brings me to the single most
useful habit I can give a beginner, and it takes ten seconds: **print the number of rows before
and after every filter, every join, every time you drop missing data.** The AI will quietly fit
your model on 47 of your 60 people because something dropped out, and never mention it. If
you're watching the row count, you catch it. If you're not, it's invisible. Count your people.
Before and after. Every time.

And its twin, just as cheap: **look at your data before you model it. Actually plot it.**
Every trap I just showed you announces itself in a picture. The ceiling trap? You'd see it in
one second — a tight little cloud of controls jammed at the top, a smear of patients below,
and a line pretending to connect them. The eye catches instantly what a p-value hides
completely. So before you fit anything, make the ugly five-second scatterplot — not for the
paper, for you. Never model data you haven't looked at. That's step one of every analysis,
forever, and the AI skips it because you didn't ask.

[Optional, ~30 sec, rehab-specific — include if the room is clinical:]

One more that's specific to recovery research, because it'll bite you personally. If you enroll
your most impaired patients — the ones at the bottom — and measure them again later, they will
appear to improve *even if your treatment does nothing at all.* It's called regression to the
mean: pick people because they scored extreme, and pure measurement noise pulls them back toward
the middle next time. Stack that on top of the natural recovery that happens after a stroke
anyway, and a do-nothing intervention can look like a triumph. The AI computes your change
scores without a whisper about it. Ask it: "how much of this could be regression to the mean?"

---

## 6 · The model that hid an effect ⏱ 0:37–0:43

[The counterintuitive one. Everyone assumes the danger is false positives. Flip it — this is
the beat that makes people gasp.]

Everything I've shown you so far is the AI helping you *find* something that isn't there. Now
I'm going to show you the opposite, and it's the direction almost nobody warns you about.

Back to our thirty patients, measured at one month and at twelve months post-stroke. Simple
question: did they recover?

Now, the right tool here is something called a mixed-effects model. Let me demystify that,
because the name is scary and the idea is simple. A mixed-effects model is just a model that
*knows Bob's two scores are both Bob's.* It builds in the fact that each person shows up twice,
and it accounts for the fact that Bob is generally a bit above average and Sara generally a bit
below, before it asks the real question — did people, on average, get better over time. That's
all it is. It's a model that respects your design.

When you do it that way, the answer is loud and clear: recovery of about **7 points** on the
aphasia quotient from month one to month twelve, with a t-statistic of **5.2.** In plain terms:
a strong, unambiguous improvement. Real patients genuinely got better.

Now watch what happens when you do it the way the AI will happily let you do it — a plain
linear model that treats all sixty rows as sixty separate, unrelated people. Counting Bob
twice.

[Say the number slowly. Let it hang.]

**p equals 0.056.** Not significant. The write-up practically types itself: "language scores
did not significantly improve over time."

Same patients. Same data. One model says "clear, strong recovery, t of 5.2." The other says
"nothing happened, p of 0.056." And here's the gut-punch: **the wrong one is the one you'd
have written.** The plain linear model is the obvious thing, the thing the AI reaches for, the
thing that doesn't make you learn a new function. You'd have concluded these patients didn't
recover. And you'd have been flat wrong — you'd have buried a real recovery in real stroke
survivors.

[Land it.]

The wrong model didn't invent an effect out of nothing. **It hid one that was really there.**
By pretending thirty people were sixty, it threw away the pairing — and with the pairing went
the statistical power to see what actually happened. Everybody in research is trained to fear
the false positive, the effect that isn't real. Nobody trains you to fear this: the true
effect the wrong analysis quietly erases. And the code ran perfectly the whole time. It always
runs perfectly. **That is precisely what makes it dangerous.**

---

## 7 · The fabricated paragraph — the punchline ⏱ 0:43–0:50

[The ending everyone remembers. If you have a volunteer's screen, use it; otherwise do it live
yourself. Go slow. This is the payoff for everything.]

Last demo. The one I want lodged in your memory when you walk out. I'm going to ask the AI to do
the single most seductive thing it does for a busy researcher — write my Results section for me.
And I promise you two things that are both true at once: it will write it *better than I would*,
and it will *lie* in it. Learning to hold both of those in your head at the same time is the
entire skill.

[You need a real fitted model on screen with real output — the aphasia-group linear model from
the R materials, with its coefficient table and fit statistics visible. Then ask:]

> Write the Results paragraph for this linear model in APA style — report the coefficients,
> confidence intervals, R-squared, and the F test.

[It produces beautiful, publication-ready APA prose. Read it aloud. It sounds perfect. It sounds
like you on your best day. Now put it side by side with the actual output and go through it
number by number, out loud, with the room.]

Gorgeous, right? I would sign that. My co-authors would sign that. Now — we check it. Not skim
it. **Check it.** The rule is brutal and simple: every number in this paragraph, I am going to
find in the real output with my own finger, or that number does not exist.

[Now hunt, out loud. You're looking for at least one of these — and in testing this, three runs
out of four produce at least one:]

- A degrees-of-freedom value that's nowhere in the output — "it says df equals... hold on,
  where is that? That's not in the model. It made that up."
- A significance claim that's actually false — "it calls this predictor 'significant.' The
  output says p equals 0.055. That is not significant. It just rounded a decision your reviewers
  will make for you."
- A flipped sign — "it says this effect is positive. Look at the coefficient. It's negative. The
  direction is backwards."
- An R-squared it never saw — "where did this R-squared come from? That's not the one in the
  output."

[When you find it — and you will — stop and hold it up like evidence, because it is.]

There. Right there. That number is not in the output. The AI wrote a flawless, submittable
paragraph and set a fabricated statistic in the middle of it — in perfect APA format, with a
confidence interval wrapped around a number it invented. And if I hadn't checked — if I'd
trusted the beautiful prose the way it is practically *designed* to make me trust it — that
invented number goes into the manuscript. Past me. Past my co-authors. Past the reviewers, who
are also busy and also trust clean prose. Into the published, permanent, citable record.

[Beat. This is the line of the whole talk.]

**It wrote a better paragraph than I would have. And it lied in it. Both of those are true, and
your job — starting now — is to hold both at the same time.**

And this isn't a fluke of one bad model. When researchers audited hundreds of AI-generated
citations, the older models fabricated more than *half* of them; even today's best models
fabricate close to one in five — references to papers that were never written. So take the
general rule with you: **a number in prose is not a result. A number in prose is a claim. And
every claim gets traced back to the actual output before you let yourself believe it.**

---

## 8 · What you actually take home ⏱ 0:50–0:56

[Shift the tone. Calmer, warmer. You've frightened them on purpose; now arm them so they leave
capable, not scared. Gesture at the `guardrails/` folder — it's the thing they keep.]

So it lies. What do we do about it? We don't stop using it — it is far too useful, and this is
the direction the whole field is going whether any of us voted for it. We *supervise* it. And
supervision is a set of concrete habits, all of them written down, all of them sourced, in the
folder called `guardrails/`. Let me give you the four that matter most.

**First — the one rule that does not bend. Never paste real patient data into a chatbot.** Not a
transcript, not a date of birth, not an MRN, not "de-identified" text you haven't personally
checked line by line. When you type into the ordinary consumer version of these tools, what you
send can be stored, retained, and reviewed — and it is *not* covered by your institution's
compliance agreement unless someone has told you, in writing, that a specific approved version
is. And "de-identified" is a legal standard, not a vibe — HIPAA lists *eighteen* kinds of
identifier you'd have to strip, and here's the one that catches researchers like us: **a voice
recording is a biometric identifier. It is protected health information even with the name torn
off.** So is a face photo. A picture-description transcript can name a spouse, a hometown, a
rare diagnosis — you cannot eyeball a paragraph and pronounce it clean.

If you think this is theoretical: in 2023, Samsung engineers pasted confidential source code
into ChatGPT to get debugging help — three separate times in three weeks — and Samsung's
response was to ban the tools company-wide. That was *source code*. Yours would be a patient.
**The two most dangerous everyday actions with these tools are "paste this code to debug it" and
"summarize this transcript." Both of them leak.**

And the fix is genuinely easy — it's the whole reason today's data is fake. **Share the schema,
not the rows.** Give the AI your column names, the types, and one completely made-up example
row. That is everything it needs to write correct code. It never needs to see a single real
value, ever.

**Second — the review rubric.** There's a one-page checklist in the guardrails folder. Print it,
laminate it, whatever it takes. Run every AI analysis through it before a single number leaves
your screen. It's built as gates: did any real data leak — if yes, stop, nothing else matters.
Does it run on *my* data and not just a toy example. Did I print my row counts around every
filter. Are the packages it wants me to install even *real* — and I mean that literally, because
these tools invent package names that don't exist, and attackers have started registering those
predictable fake names *with malware inside*, sitting there waiting for the next person to
install what the AI hallucinated. The study that measured this found up to one in five suggested
packages simply don't exist. **Check before you install. Always.** And the last gate, the big
one: is every number in the write-up traceable to the real output.

**Third — the statistics guardrails.** Every trap I showed you — the ceiling, the vanishing
finding, the hidden recovery, the confounded measure, regression to the mean — is in there, each
one paired with the exact question that flushes it out. And underneath all of them sits one
question. If you take a single sentence of statistics home, take this one: **"What is my unit of
analysis, and is anything in this model being counted as independent evidence when it isn't?"**
Ask that of every analysis, forever. It catches more mistakes than any statistics course I ever
took.

**Fourth — and this is the move that makes the whole thing scale beyond your own vigilance.**
There's a file called RESEARCH_PROJECT_RULES. It's a short set of standing instructions you hand
the AI *once*, at the start of a project — and the modern tools read it before every single
answer they give you. You tell it your study design. You tell it never to invent a column name.
You tell it to use a mixed model for repeated measures. And my favorite line in the whole
template — you tell it **never to state a p-value in prose, only ever to print it from the real
output.** Think about what that does. You cannot be handed a fabricated number if you have
instructed the assistant to only ever show you real ones. You've taught it to catch itself, so
you are no longer the only line of defense standing between a hallucination and your paper.

[A gift to end the guardrails on — a positive habit, not another warning.]

And one habit that costs nothing and pays you back every time. At the *end* of a working
session with the AI, before you close the tab, ask it this: **"summarise everything we just
did as a numbered list of the analysis steps, so I can paste it into my methods section."** It
is genuinely excellent at that — it remembers every step you took, in order, better than you
will tomorrow morning. You get a first-draft methods paragraph and a record of what you
actually did, for free. That's the tool at its best: not making the decisions, but keeping
faithful track of the ones *you* made.

[One more, quickly, because it's now expected of us:]

And when you do use it — say so. Journals now require it, and the rule everyone's converged on is
simple: the AI cannot be an author, because it cannot be held accountable, and you disclose where
you used it in your methods. Keep your chat logs. They're your paper trail.

---

## 9 · Where this goes, and the last line ⏱ 0:56–0:59

[Ninety seconds. Show them the horizon so they know it exists — don't teach it.]

One last thing, so you know where all of this is heading. What we did today was copy-paste — me,
in the middle, ferrying code back and forth between a chat window and a notebook. The next step
deletes the middle. There are tools now where you sit in your project folder and just say, in
plain English, "read this CSV, compute these language measures, fit the mixed model, make the
figure," and it goes and *does the whole thing* — reads, computes, models, plots — while you
watch. Ninety seconds for what took us ninety minutes.

[Beat.]

And that sounds like it makes today pointless. It does the exact reverse. When the machine can do
the entire analysis in ninety seconds, **the only thing standing between you and a published
mistake is whether you can read what it did and tell whether it's right.** The faster the tool
gets, the more the whole enterprise collapses down to one skill: judgment. Today was not a
tutorial in a slow way of doing things you're about to be able to skip. **Today was practice for
the one skill that survives all of it.**

[Final beat. Slow all the way down. This is the closing line — deliver it, then stop talking. Do
not add "any questions."]

Every one of you walked in here as the person who *runs* the analysis. You walk out as something
different, whether you wanted the promotion or not. You are now the **senior author** on
everything the AI writes for you. You didn't type it — but you're the one who signs it, who
defends it at your committee, who answers when a reviewer asks, "where did this number come
from?"

**So act like it.**

[Stop. Let the line be the last thing in the air for a second. Then: "Okay — questions."]

---

## Appendix · Timing cheat-sheet

| Section | Clock | If you're running long |
|---|---|---|
| 0 · Cold open | 0:00–0:04 | Never cut — it's the thesis. |
| 1 · The bad prompt | 0:04–0:10 | Keep both prompts; the contrast is the lesson. |
| 2 · The recipe | 0:10–0:15 | Can compress to 3 min; point to PROMPTS.md. |
| 3 · The debugging loop | 0:15–0:19 | Can trim to the "three strikes → new chat" rule. |
| 4 · The confident lie | 0:19–0:28 | **Never cut.** Core demo. |
| 5 · The traps you can't see | 0:28–0:37 | Can drop to two traps (keep the ceiling + the confound). |
| 6 · The model that hid an effect | 0:37–0:43 | **Never cut.** The counterintuitive one. |
| 7 · The fabricated paragraph | 0:43–0:50 | **Never cut.** The punchline. |
| 8 · What you take home | 0:50–0:56 | Can compress; just walk them to `guardrails/`. |
| 9 · Where this goes + close | 0:56–0:59 | Keep the last line no matter what. |

**The four demos that must survive any cut:** the bad-vs-good prompt (§1), the confident lie
(§4), the hidden effect (§6), and the fabricated Results paragraph (§7). Everything else is
connective tissue. If you have 30 minutes instead of 50, run only those four plus the closing
line and you've still delivered the workshop.

**The numbers you'll say out loud — every one verified against `data/`, so you can trust them
on stage:** pooled R² 0.70 vs patients-only 0.36 · content-word ratio p 0.004 → 0.055 ·
type-token ratio vs length r = −0.41 · mixed model +7.1 points, t = 5.2 · naive model p = 0.056.

**If you'd rather run the full hands-on workshop** (3 hours, laptops, Python + R), this script
is the spoken spine of it — open the three HANDS-ON beats and follow the block structure in
[FACILITATOR.md](FACILITATOR.md).
