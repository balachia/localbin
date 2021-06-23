#!/usr/bin/env Rscript

#x <- capture.output(install.packages("devtools"))
#x <- system2("Rscript", "-e \"install.packages('devtools')\"", stdout = TRUE, stderr = TRUE)
#groups <- regmatches(x, regexec("installation of package .(.+). had", x))
#groups <- groups[sapply(groups, length) > 0]
#failed <- sapply(groups, function(x) x[[2]])

system.install.package <- function(package, ...) {
    package.string <- paste0("-e \"install.packages('", package, "')\"")
    system2("Rscript", package.string, stdout = TRUE, stderr = TRUE)
}

extract.warning.messages <- function(output) {
    groups <- regmatches(output, regexec("installation of package .(.+). had non-zero exit status", output))
    groups <- groups[sapply(groups, length) > 0]
    as.character(sapply(groups, function(x) x[[2]]))
}

extract.reinstall.package <- function(output) {
    groups <- regmatches(output, regexec("[Ee]rror.?: package .(.+). was installed before", output))
    groups <- groups[sapply(groups, length) > 0]
    as.character(sapply(groups, function(x) x[[2]]))
}

try.load <- function(package) {
    suppressMessages(res <- require(package, character.only = TRUE, quietly = TRUE))
    if(res) {
        detach(sprintf('package:%s', package), unload = TRUE, character.only = TRUE)
    }
    res
}

try.install <- function(packages, stack=character(0), max.depth=10) {
    # input: get list of packages
    # for each package:
    #   try to install package
    #       if successful return up
    #       else, get list of failures
    #           try to install each one
    if(length(stack) > max.depth) {
        cat('hit stack limit\n', stack)
        stop('hit stack limit')
    }
    stack.s <- if(length(stack) == 0) '' else sprintf(' (%d: %s)', length(stack), paste(stack, collapse = ' '))
    for(p in packages) {
        cat(sprintf('installing %s%s', p, stack.s))
        if(try.load(p)) {
            cat(', already installed\n')
        } else {
            ip.out <- system.install.package(p)
            ps.reinstall <- extract.reinstall.package(ip.out)
            ps.warn <- extract.warning.messages(ip.out)
            failed <- c(ps.reinstall, ps.warn)
            if(length(failed) == 0) {
                cat(' \U2713\n')
            } else if (length(failed) == 1 && failed == p){
                cat('\n', ip.out, sep = '\n')
                stop('hit dead end')
            } else {
                cat(' \U2717\n\tFailed:', failed, '\n')
                try.install(failed, stack=c(stack, p))
            }
        }              
    }
}

# bootstrap devtools
#install.packages("devtools")
try.install("devtools")
#library(devtools)
#devtools::install_github("hadley/devtools")

devtools::install_github("jalvesaq/colorout")

try.install('tidyverse')
try.install('data.table')
try.install('lintr')
try.install('cowplot')
try.install('Rtsne')
try.install('igraph')
try.install('openxlsx')
try.install('reshape2')
try.install('shiny')

#packages <- c("tidyverse",
#              "data.table",
#              "Rcpp",
#              "lintr")

#packages <- c("setwidth",
#              "data.table",
#              "MASS",
#              "ggplot2",
#              "reshape2",
#              "texreg",
#              "knitr",
#              "xtable",
#              "stargazer",
#              "Matrix",
#              "ffbase",
#              "xlsx",
#              "Rcpp",
#              "RcppArmadillo",
#              "RColorBrewer",
#              "Zelig",
#              "igraph",
#              "Rtsne",
#              "purrr",
#              "dplyr",
#              "gridExtra",
#              "lintr",
#              "docopt")
#install.packages(packages)
