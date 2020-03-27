import os

import pandas
import rpy2.robjects as robjects

import constants as c


def execute(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
        algorithm: str,
        target: str
):
    if algorithm == c.RANDOM_FOREST:
        return _random_forest(target)
    elif algorithm == c.LOGISTIC_REGRESSION:
        return _logistic_regression(target)
    elif algorithm == c.NEURAL_NETWORK_MP:
        return _neural_network_mp(target)
    else:
        # TODO: raise error
        pass


def _random_forest(
        target: str
):
    temp_dir = os.path.abspath("temp")
    result = robjects.r('''
        library(randomForest)
        library(caret)
        
        x <- read.csv("%s/features_train.csv")
        y <- read.csv("%s/labels_train.csv")
        xtest <- read.csv("%s/features_test.csv")
        ytest <- read.csv("%s/labels_test.csv")
        
        train = x
        train[length(x)+1] = y
        
        test = xtest
        test[length(x)+1] = ytest
        
        train$%s = as.factor(train$%s)
        test$%s = as.factor(test$%s)
        
        common <- intersect(names(train), names(test))
        for (p in common) {
          if (class(train[[p]]) == "factor") {
            levels(test[[p]]) <- levels(train[[p]])
          }
        }
        
        rf <- randomForest(%s~.,data=train)
        prediction <- predict(rf, test)
        confusionMatrix(prediction, test$%s)
    ''' % (temp_dir, temp_dir, temp_dir, temp_dir, target, target, target, target, target, target))

    return {'result': str(result).replace('\'', '-')}

def _logistic_regression(
        target: str
):
    return ""


def _neural_network_mp(
        target: str
):
    return ""
