#!/usr/bin/env Rscript
library(lintr)
args <- commandArgs(trailingOnly=T)
lint.list <- with_defaults(commented_code_linter=NULL)
lint(args[1], linters=lint.list, cache=".lintr-cache")
