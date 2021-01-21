library(optparse)
library(lattice)
library(ggplot2)
library(caret)
library(rpart)

max_reg <- function(model_obj, testing = NULL, target = NULL) {
    #Calculates rmse for a regression decision tree
    #Arguments:
    # testing - test data set
    # target  - target variable (length 1 character vector)
    yhat <- predict(model_obj, newdata = testing)
    actual <- testing[[target]]
    abs(max(as.numeric(yhat)-as.numeric(actual)))
}

rmse_reg <- function(model_obj, testing = NULL, target = NULL) {
    #Calculates max_error for a regression decision tree
    #Arguments:
    # testing - test data set
    # target  - target variable (length 1 character vector)
    yhat <- predict(model_obj, newdata = testing)
    actual <- testing[[target]]
    # sqrt(mean((as.numeric(yhat)-as.numeric(actual))^2))
    rmse(yhat,actual)
}


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
    make_option(c("-i", "--maximum_depth"), type="integer", default=100, help="maximum depth of the tree", metavar="integer")
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

path = parse.path(opt$path)
target = parse.target(opt$target)
maximum_depth = parse.maximum_depth(opt$maximum_depth)

train = load.data("train", path, target)
test = load.data("test", path, target)

common <- intersect(names(train), names(test))
for (p in common) {
    if (class(train[[p]]) == "factor") {
        levels(test[[p]]) <- levels(train[[p]])
    }
}

tr <- rpart( formula(paste(target, "~.")), method = "class", data = train)
rmse = rmse_reg(tr, test, target)
max_error = max_reg(tr, test, target)
result = paste("rmse:", rmse, ":max_error:", max_error, sep = "")
cat(result)
