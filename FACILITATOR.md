# Facilitator guide

The current live format is a one-hour, hands-on session. Use [SCRIPT_1HR.md](SCRIPT_1HR.md)
for the exact delivery language and [ADVANCED_PATHS.md](ADVANCED_PATHS.md) to select a route
after the initial readiness check.

## Before the session

- Open an AI chat, the core Colab notebook, the shared Posit project, and `PROMPTS.md` on the
  display you will share.
- Open this guide, `SCRIPT_1HR.md`, the Python and R solution files, and a timer on the private
  display.
- Run the Colab setup cell and confirm `Ready.`.
- In Posit, run `r/install_packages.R` only if the project does not already load the required R
  packages. Confirm that `readr`, `dplyr`, `ggplot2`, and `lme4` load.
- Run `r/02_r_solution.R` once and retain the Console output for the mixed-model fallback.
- Test the public Colab link and the Posit copy flow in a browser session that is not signed in.

The workshop starts only after participants can access an AI assistant, Colab, and Posit. A
participant without access pairs with another participant rather than waiting for a local setup.

## Route decision

At minute 5, ask who has previously used an AI assistant to write and run research code.

- **Core route:** use `SCRIPT_1HR.md` when participants need the basic prompt-to-code workflow.
- **Experienced-room route:** use the advanced recovery-prediction branch when the room already
  manages basic R or Python prompting.
- **Mixed room:** retain the core route on the shared display. Experienced participants complete
  one advanced task independently and return with a question or output.

Do not combine the two routes in a one-hour session.

## Intervention order when someone is stuck

1. Confirm the correct tab and the setup checkpoint.
2. Ask the participant to copy the full error into the same AI conversation.
3. Request one minimal correction, then run that correction alone.
4. If the correction fails, use the solution file to restore the participant to the current task.

Common causes are a Colab setup cell that was not run, a Posit project that was opened without
making a permanent copy, a working-directory mismatch, or code pasted without its imports.

## Non-negotiable demonstrations

- Participants specify the unit of observation and variable names before requesting code.
- Participants inspect the number of rows and columns after loading or joining data.
- The core route compares the repeated-measures model with the deliberately inappropriate
  independent-rows model.
- The final writing exercise traces every reported value to displayed output.

If time is short, remove Python Task 3 before removing the model-output check. Do not ask the
room to install packages during the session.

## Statements to avoid

- Do not promise that an assistant will generate an error, an inappropriate model, or a fabricated
  statistic on demand.
- Do not characterize a model output as clinically meaningful when it derives from these synthetic
  data.
- Do not state that a tool is approved for real data. The institution, the data-use agreement, and
  the approved service determine that question.
- Do not make the agent exercise an autonomous analysis. It is a read-only project inventory.

## Materials after the session

- `PROMPTS.md` contains the reusable request and debugging patterns.
- `guardrails/` contains source-linked background documents. Its literature references require a
  separate verification pass before reuse in scholarly prose.
- `r/02_r_solution.R` and the solution notebooks are recovery tools, not participant work to run
  before attempting the starter tasks.
