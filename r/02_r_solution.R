# =============================================================================
# PART 2 - R: statistical modeling + ggplot [solution / reference]
#
# Reference implementation. Attendees should attempt each prompt themselves
# before consulting this file; it exists as a fallback, not a starting point.
# =============================================================================

library(readr)
library(dplyr)
library(ggplot2)
library(broom)
library(tidyr)

# If this line errors, do: Session > Set Working Directory > To Project Directory
stopifnot(dir.exists("data"))


# ---- 1. Load and inspect ---------------------------------------------------
transcripts <- read_csv("data/transcripts.csv", show_col_types = FALSE)
features    <- read_csv("data/features.csv",    show_col_types = FALSE)

df <- left_join(transcripts, features, by = "participant_id") |>
  mutate(group = factor(group, levels = c("control", "aphasia")))

glimpse(df)


# ---- 2. Descriptives by group ---------------------------------------------
desc <- df |>
  group_by(group) |>
  summarise(
    n                  = n(),
    age                = sprintf("%.1f (%.1f)", mean(age), sd(age)),
    wab_aq             = sprintf("%.1f (%.1f)", mean(wab_aq), sd(wab_aq)),
    n_words            = sprintf("%.1f (%.1f)", mean(n_words), sd(n_words)),
    content_word_ratio = sprintf("%.3f (%.3f)", mean(content_word_ratio),
                                 sd(content_word_ratio)),
    .groups = "drop"
  )
print(desc)

# Group difference in content-word ratio
t.test(content_word_ratio ~ group, data = df)


# ---- 3. Exploratory plot ---------------------------------------------------
ggplot(df, aes(x = content_word_ratio, y = wab_aq, colour = group)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE)


# ---- 4. Model: lexical features and WAB-AQ within aphasia -----------------
# The question concerns variation within the aphasia group. Controls cluster near the
# upper end of WAB-AQ in this synthetic dataset.
aph <- filter(df, group == "aphasia")

m1 <- lm(wab_aq ~ content_word_ratio + type_token_ratio + n_words + age,
         data = aph)

tidy(m1, conf.int = TRUE) |>
  mutate(across(where(is.numeric), \(x) round(x, 3))) |>
  print()

glance(m1) |> select(r.squared, adj.r.squared, statistic, p.value, df, nobs) |> print()

# Assumption checks. Inspect the resulting plots.
par(mfrow = c(2, 2)); plot(m1); par(mfrow = c(1, 1))

# Inspect the association among the language predictors. Type-token ratio varies with
# transcript length in this constructed dataset.
cor(aph[, c("content_word_ratio", "type_token_ratio", "n_words")]) |>
  round(2) |> print()


# ---- 5. Publication figure -------------------------------------------------
fig <- ggplot(df, aes(x = content_word_ratio, y = wab_aq)) +
  geom_point(aes(fill = group, shape = group), colour = "#1A1A1A", size = 2.6,
             stroke = 0.35, alpha = 0.85) +
  geom_smooth(data = aph, method = "lm", se = TRUE,
              colour = "#4393C3", fill = "#4393C3", alpha = 0.18, linewidth = 0.7) +
  scale_fill_manual(values = c(control = "#00A087", aphasia = "#E64B35")) +
  scale_shape_manual(values = c(control = 21, aphasia = 24)) +
  scale_x_continuous(labels = scales::percent_format(accuracy = 1)) +
  labs(
    x = "Content-word ratio",
    y = "WAB Aphasia Quotient",
    fill = NULL, shape = NULL,
    title = "Content-word ratio and WAB Aphasia Quotient",
    subtitle = "Synthetic Cookie Theft descriptions, n = 60; fit includes aphasia group only",
    caption = "Synthetic data. Shaded band: 95% confidence interval for the fitted mean."
  ) +
  theme_minimal(base_size = 11, base_family = "Helvetica") +
  theme(
    legend.position = "bottom",
    legend.background = element_blank(),
    legend.key = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(colour = "#EBEBEB", linewidth = 0.25),
    plot.title = element_text(face = "bold", hjust = 0, colour = "#222222"),
    plot.subtitle = element_text(colour = "#666666"),
    plot.caption = element_text(colour = "#666666", size = 8)
  )

print(fig)
ggsave("outputs/figure1.png", fig, width = 7, height = 5, dpi = 300)


# ---- 6. Stretch: longitudinal mixed-effects model -------------------------
library(lme4)

long <- read_csv("data/transcripts_long.csv", show_col_types = FALSE) |>
  mutate(timepoint = factor(timepoint, levels = c("acute", "chronic")))

# Each participant contributes two observations. The random intercept represents
# within-participant dependence across the two timepoints.
long_model <- lmer(wab_aq ~ timepoint + (1 | participant_id), data = long)
summary(long_model)
confint(long_model, method = "Wald")

# Individual trajectories and the sample mean
ggplot(long, aes(x = timepoint, y = wab_aq, group = participant_id)) +
  geom_line(alpha = 0.35, colour = "grey50") +
  geom_point(alpha = 0.6, colour = "grey30") +
  stat_summary(aes(group = 1), fun = mean, geom = "line",
               colour = "#4393C3", linewidth = 1.1) +
  stat_summary(aes(group = 1), fun = mean, geom = "point",
               shape = 21, fill = "#4393C3", colour = "#1A1A1A", size = 3.5,
               stroke = 0.35) +
  labs(x = NULL, y = "WAB Aphasia Quotient",
       title = "Recovery from acute to chronic stage",
       subtitle = "Grey: individual participants. Blue: sample mean.",
       caption = "Synthetic data.") +
  theme_minimal(base_size = 11, base_family = "Helvetica") +
  theme(
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(colour = "#EBEBEB", linewidth = 0.25),
    plot.title = element_text(face = "bold", hjust = 0, colour = "#222222"),
    plot.subtitle = element_text(colour = "#666666"),
    plot.caption = element_text(colour = "#666666", size = 8)
  )


# ---- 7. Fact-check exercise ------------------------------------------------
# Request a Results paragraph for model m1, then compare each reported value with:
tidy(m1, conf.int = TRUE)
glance(m1)
nobs(m1)
# Check the degrees of freedom, effect direction, p-value interpretation, and any
# R-squared or F statistic against the displayed objects.
