library(optparse)
library(lattice)
library(ggplot2)
library(randomForest)
library(caret)

parse.path <- function(path) {
    if (is.null(path)){
        print_help(opt_parser)
        stop("path is a mandatory argument", call.=FALSE)
    }
    path
}

parse.target <- function(target) {
    if (is.null(target)){
        print_help(opt_parser)
        stop("target is a mandatory argument", call.=FALSE)
    }
    target
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
    make_option(c("-t", "--target"), type="character", default=NULL, help="target feature", metavar="character")
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

path = parse.path(opt$path)
target = parse.target(opt$target)

train = load.data("train", path, target)
test = load.data("test", path, target)

common <- intersect(names(train), names(test))
for (p in common) {
    if (class(train[[p]]) == "factor") {
        levels(test[[p]]) <- levels(train[[p]])
    }
}

rf <- randomForest(formula(paste(target, "~.")), data=train)
prediction <- predict(rf, test)
confusionMatrix(prediction, test[[target]])
