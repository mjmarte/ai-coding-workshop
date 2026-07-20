# =============================================================================
# PART 2 — R: statistical modelling + ggplot        [ SOLUTION / REFERENCE ]
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


# ---- 1. Load and inspect ----------------------------------------------------
transcripts <- read_csv("data/transcripts.csv", show_col_types = FALSE)
features    <- read_csv("data/features.csv",    show_col_types = FALSE)

df <- left_join(transcripts, features, by = "participant_id") |>
  mutate(group = factor(group, levels = c("control", "aphasia")))

glimpse(df)


# ---- 2. Descriptives by group ----------------------------------------------
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


# ---- 3. A first, quick plot ------------------------------------------------
ggplot(df, aes(x = content_word_ratio, y = wab_aq, colour = group)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE)


# ---- 4. Model: do lexical features predict aphasia severity? ---------------
# Restrict to the aphasia group — WAB-AQ has almost no variance in controls,
# so pooling them would manufacture a correlation out of the group difference.
aph <- filter(df, group == "aphasia")

m1 <- lm(wab_aq ~ content_word_ratio + type_token_ratio + n_words + age,
         data = aph)

tidy(m1, conf.int = TRUE) |>
  mutate(across(where(is.numeric), \(x) round(x, 3))) |>
  print()

glance(m1) |> select(r.squared, adj.r.squared, statistic, p.value, df, nobs) |> print()

# Assumption checks — inspect these plots, do not just execute the call
par(mfrow = c(2, 2)); plot(m1); par(mfrow = c(1, 1))

# Multicollinearity: n_words and type_token_ratio are not independent.
# (TTR falls as transcripts get longer — a classic, well-known confound.)
cor(aph[, c("content_word_ratio", "type_token_ratio", "n_words")]) |>
  round(2) |> print()


# ---- 5. Publication-quality figure -----------------------------------------
fig <- ggplot(df, aes(x = content_word_ratio, y = wab_aq)) +
  geom_point(aes(colour = group, shape = group), size = 2.6, alpha = 0.85) +
  geom_smooth(data = aph, method = "lm", se = TRUE,
              colour = "grey25", fill = "grey80", linewidth = 0.7) +
  scale_colour_manual(values = c(control = "#4C9F70", aphasia = "#B5446E")) +
  scale_x_continuous(labels = scales::percent_format(accuracy = 1)) +
  labs(
    x = "Content-word ratio",
    y = "WAB Aphasia Quotient",
    colour = NULL, shape = NULL,
    title = "Lexical content tracks aphasia severity",
    subtitle = "Synthetic Cookie Theft descriptions (n = 60); fit line is the aphasia group only",
    caption = "Synthetic data — for teaching purposes only"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position   = "bottom",
    legend.background = element_rect(fill = "white", colour = "grey85"),
    panel.grid.minor  = element_blank(),
    plot.title        = element_text(face = "bold"),
    plot.caption      = element_text(colour = "grey45", size = 8)
  )

print(fig)
ggsave("outputs/figure1.png", fig, width = 7, height = 5, dpi = 300)


# ---- 6. STRETCH: longitudinal recovery, mixed-effects model -----------------
library(lme4)

long <- read_csv("data/transcripts_long.csv", show_col_types = FALSE) |>
  mutate(timepoint = factor(timepoint, levels = c("acute", "chronic")))

# Repeated measures: two visits per participant. A plain lm here would treat
# the 60 rows as 60 independent people. They are not. Random intercept per person.
long_model <- lmer(wab_aq ~ timepoint + (1 | participant_id), data = long)
summary(long_model)
confint(long_model, method = "Wald")

# Spaghetti plot of individual recovery trajectories
ggplot(long, aes(x = timepoint, y = wab_aq, group = participant_id)) +
  geom_line(alpha = 0.35, colour = "grey50") +
  geom_point(alpha = 0.6, colour = "grey30") +
  stat_summary(aes(group = 1), fun = mean, geom = "line",
               colour = "#B5446E", linewidth = 1.4) +
  stat_summary(aes(group = 1), fun = mean, geom = "point",
               colour = "#B5446E", size = 3.5) +
  labs(x = NULL, y = "WAB Aphasia Quotient",
       title = "Recovery from acute to chronic stage",
       subtitle = "Grey = individual participants; pink = group mean") +
  theme_minimal(base_size = 12)


# ---- 7. The fact-check exercise --------------------------------------------
# Ask the AI: "Write the Results paragraph for model m1 in APA style."
# Then check EVERY number it gives you against this:
tidy(m1, conf.int = TRUE)
glance(m1)
nobs(m1)
# Things it commonly gets wrong: the df, the direction of an effect,
# 'significant' for p = .07, and citing an R-squared it never saw.
