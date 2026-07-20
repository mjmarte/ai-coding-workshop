# Workshop setup

Complete these steps before the session. Bring a laptop rather than a tablet.

## 1. AI assistant

Open an AI assistant available to you, such as ChatGPT, Claude, or an institutionally approved
service. Sign in and start a new conversation. The workshop uses synthetic data only.

For real research data, confirm the approved service and applicable data agreement before sharing
any content with an AI tool.

## 2. Python in Google Colab

1. Sign in at [Google Colab](https://colab.research.google.com).
2. Open the link supplied by the facilitator: [core Python notebook](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/01_python_starter.ipynb).
3. Run the first cell and wait for `Ready.`.

The facilitator may assign the [advanced recovery-prediction notebook](https://colab.research.google.com/github/mjmarte/ai-coding-workshop/blob/main/python/02_advanced_recovery_starter.ipynb). Do not open it unless asked.

## 3. R in Posit Cloud

Complete this step for the core route or when the facilitator assigns a core checkpoint in a mixed
room. The primary advanced recovery-prediction route uses only Colab.

1. Create or sign in to a [Posit Cloud](https://posit.cloud) account.
2. Open [the workshop project](https://posit.cloud/content/12671685).
3. Select "Save a Permanent Copy."
4. In the Files pane, open `r/02_r_starter.R`.

The permanent copy is where you run and retain your own work. Do not edit the shared project.

## If a setup step fails

Bring the error to the facilitator. Do not spend the session installing local software. If the
network blocks Colab or Posit, pair with another participant and follow the shared workflow.

## Optional local R setup

If you already use RStudio locally and the facilitator has confirmed this route, clone the
repository and run:

```r
source("r/install_packages.R")
```

Open `r/02_r_starter.R` from the repository root so that `data/` resolves correctly.
