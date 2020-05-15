library(optparse)
library(lattice)
library(ggplot2)
library(caret)
require(gbm)

parse.path <- function(path) {
    if (is.null(path)){
        print_help(opt_parser)
        stop("path is a mandatory argument", call.=FALSE)
    }
    return(path)
}

parse.target <- function(target) {
    if (is.null(target)){
        print_help(opt_parser)
        stop("target is a mandatory argument", call.=FALSE)
    }
    return(target)
}

load.data <- function(type, path, target) {
    x <- read.csv(paste(path, "/features_", type, ".csv", sep = ""))
    y <- read.csv(paste(path, "/labels_", type, ".csv", sep = ""))

    data = x
    data[length(x) + 1] = y

    data[[target]] = as.factor(data[[target]])
    return(data)
}

option_list = list(
    make_option(c("-p", "--path"), type="character", default=NULL, help="path to features and labels files", metavar="character"),
    make_option(c("-t", "--target"), type="character", default=NULL, help="target feature", metavar="character"),
    make_option(c("-i", "--trees"), type="integer", default=4, help="number of trees", metavar="integer")
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

path = parse.path(opt$path)
target = parse.target(opt$target)
trees = parse.target(opt$trees)

train = load.data("train", path, target)
test = load.data("test", path, target)

common <- intersect(names(train), names(test))
for (p in common) {
    if (class(train[[p]]) == "factor") {
        levels(test[[p]]) <- levels(train[[p]])
    }
}

gbmr <- gbm(
    formula(paste(target, "~.")),
    data=train, distribution="gaussian")
prediction <- predict(gbmr, test, n.trees=trees)
summary = summary(prediction)
rmse = sqrt(mean((prediction[1]-data.matrix(test[target]))^2))
result = paste("rmse:", rmse, ":max_error:", summary["Max."], sep = "")
cat(result)
