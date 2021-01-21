library(optparse)
library(lattice)
library(ggplot2)
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

#lr <- lm(    formula(paste(target, "~.")),    data=train)
#prediction <- predict(lr, test)
#summary = summary(prediction)
#rss <- c(crossprod(lr$residuals))
#mse <- rss / length(lr$residuals)
#rmse <- sqrt(mse)
#result <- paste("rmse:", rmse, ":max_error:", summary["Max."], sep = "")
#cat(result)

modelLR<- lm ( formula(paste(target, "~.")), data = train)
predictionsLR <- predict(modelLR, newdata = test)
test$lr = predictionsLR
rmseLR = sqrt(mean((as.numeric(test$lr)-as.numeric(test[[target]]))^2))
maxerrorLR = max(as.numeric(test$lr)-as.numeric(test[[target]]))
result <- paste("rmse:", rmseLR, ":max_error:", maxerrorLR, sep = "")
#result <- paste("a:", test[[target]][1], ":b:", test$dt[1], sep = "")
cat(result)
