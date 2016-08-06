#!/usr/bin/env Rscript

# bootstrap devtools
install.packages("devtools")
library(devtools)
devtools::install_github("hadley/devtools")

devtools::install_github("jalvesaq/colorout")

packages <- c("setwidth",
              "data.table",
              "MASS",
              "ggplot2",
              "reshape2",
              "texreg",
              "knitr",
              "xtable",
              "stargazer",
              "Matrix",
              "ffbase",
              "xlsx",
              "Rcpp",
              "RcppArmadillo",
              "RColorBrewer",
              "Zelig",
              "igraph",
              "Rtsne",
              "purrr",
              "dplyr",
              "gridExtra",
              "lintr",
              "docopt")
install.packages(packages)
