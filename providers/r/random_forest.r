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
    return(path)
}

parse.target <- function(target) {
    if (is.null(target)){
        print_help(opt_parser)
        stop("target is a mandatory argument", call.=FALSE)
    }
    return(target)
}

parse.maximum_iterations <- function(maximum_iterations) {
    if (is.null(maximum_iterations)) {
        print_help(opt_parser)
        stop("maximum_iterations is a mandatory argument", call.=FALSE)
    }
    if (!is.numeric(maximum_iterations)) {
        print_help(opt_parser)
        stop("maximum_iterations must be a number", call.=FALSE)
    }
    return(maximum_iterations)
}

parse.maximum_depth <- function(maximum_depth) {
    if (is.null(maximum_depth)) {
        print_help(opt_parser)
        stop("maximum_depth is a mandatory argument", call.=FALSE)
    }
    if (!is.numeric(maximum_depth)) {
        print_help(opt_parser)
        stop("maximum_depth must be a number", call.=FALSE)
    }
    return(maximum_depth)
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
    make_option(c("-i", "--maximum_iterations"), type="integer", default=100, help="maximum number of iterations", metavar="integer"),
    make_option(c("-d", "--maximum_depth"), type="integer", default=3, help="maximum depth of the tree", metavar="integer")
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

path = parse.path(opt$path)
target = parse.target(opt$target)
maximum_iterations = parse.maximum_iterations(opt$maximum_iterations)
maximum_depth = parse.maximum_depth(opt$maximum_depth)

train = load.data("train", path, target)
test = load.data("test", path, target)

common <- intersect(names(train), names(test))
for (p in common) {
    if (class(train[[p]]) == "factor") {
        levels(test[[p]]) <- levels(train[[p]])
    }
}

rf <- randomForest(
    formula(paste(target, "~.")),
    data=train,
    maxit=maximum_iterations,
    nodesize=maximum_depth
)
prediction <- predict(rf, test)
confusionMatrix(prediction, test[[target]])
