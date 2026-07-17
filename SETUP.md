# Setup — do this BEFORE the workshop (10 minutes)

You will not install anything. Everything runs in your browser. You need
**three tabs open** on the day.

---

## Tab 1 — Your AI assistant

Any one of these. If you have none, make a free Claude account — it takes a minute.

- **Claude** — [claude.ai](https://claude.ai) (free tier is fine)
- **ChatGPT** — [chat.openai.com](https://chat.openai.com)
- Whatever your institution provides

> Check with your IT/compliance office about which AI tools are approved for work use.
> Today's data is synthetic, so it doesn't matter for the workshop — but it matters
> the moment you go back to your own data.

---

## Tab 2 — Python (Google Colab)

1. Go to [colab.research.google.com](https://colab.research.google.com) and sign in
   with any Google account.
2. Click the **Open in Colab** button in the workshop README, or use the link the
   facilitator sends you.
3. Run the first cell. If it prints `Ready.` you are done.

Colab is a Python notebook that runs on Google's computers. Nothing is installed on
yours. It's free.

---

## Tab 3 — R (Posit Cloud)

1. Go to [posit.cloud](https://posit.cloud) and create a free account.
2. Open the project link the facilitator sends you.
3. Click **Save a Permanent Copy** at the top of the screen. *(Important — if you skip
   this, your work disappears.)*
4. In the Files pane at bottom-right, open `r/02_r_starter.R`.

Posit Cloud is RStudio running in your browser. Nothing is installed on your computer.
The free tier is plenty for today.

---

## If a step fails

That's fine — come anyway, we'll sort it out in the first ten minutes. Bring a laptop,
not a tablet. If your institution's network blocks one of these sites, a phone hotspot
usually solves it.

---

## Optional, if you already have R installed locally

Run this in the RStudio console and the whole workshop lands in your home directory:

```r
install.packages("usethis")
usethis::use_course("YOUR-USERNAME/ai-coding-workshop")
```

Then `source("r/install_packages.R")` once to get the packages.
