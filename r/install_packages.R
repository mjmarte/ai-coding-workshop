# Run this only for a local R installation or when preparing the shared Posit
# Cloud project. Participants using a permanent copy should not need it.

pkgs <- c("readr", "dplyr", "tidyr", "ggplot2", "broom", "lme4", "scales")
missing <- pkgs[!pkgs %in% rownames(installed.packages())]

if (length(missing)) {
  message("Installing: ", paste(missing, collapse = ", "))
  install.packages(missing)
} else {
  message("All packages already installed.")
}

invisible(lapply(pkgs, library, character.only = TRUE))
message("\nReady. R version: ", R.version.string)
