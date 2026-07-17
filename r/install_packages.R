# Run this ONCE. Only needed if you're running R locally, or if you're the
# facilitator setting up the shared Posit Cloud project.
#
# On Posit Cloud this takes 2-4 minutes. Attendees who copy the project
# afterwards inherit the installed packages and don't need to run it.

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
