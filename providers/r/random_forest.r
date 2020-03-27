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

option_list = list(
    make_option(c("-p", "--path"), type="character", default=NULL, help="path to features and labels files", metavar="character"),
    make_option(c("-t", "--target"), type="character", default=NULL, help="target feature", metavar="character")
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

path = parse.path(opt$path)
target = parse.target(opt$target)

x <- read.csv(paste(path, "/features_train.csv", sep = ""))
y <- read.csv(paste(path, "/labels_train.csv", sep = ""))
xtest <- read.csv(paste(path, "/features_test.csv", sep = ""))
ytest <- read.csv(paste(path, "/labels_test.csv", sep = ""))

train = x
train[length(x) + 1] = y

test = xtest
test[length(x) + 1] = ytest

train[[target]] = as.factor(train[[target]])
test[[target]] = as.factor(test[[target]])

common <- intersect(names(train), names(test))
for (p in common) {
    if (class(train[[p]]) == "factor") {
        levels(test[[p]]) <- levels(train[[p]])
    }
}

rf <- randomForest(formula(paste(target, "~.")), data=train)
prediction <- predict(rf, test)
confusionMatrix(prediction, test[[target]])
