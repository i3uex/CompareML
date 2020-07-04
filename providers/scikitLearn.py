from math import sqrt

import cherrypy
import pandas
from sklearn import svm
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import max_error
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor

import constants as c


def execute(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
        algorithm: str,
        target: str
):
    try:
        if algorithm == c.RANDOM_FOREST:
            return _random_forest(features_train, features_test, labels_train, labels_test)
        elif algorithm == c.LOGISTIC_REGRESSION:
            return _logistic_regression(features_train, features_test, labels_train, labels_test)
        elif algorithm == c.SUPPORT_VECTOR_MACHINES:
            return _support_vector_machines(features_train, features_test, labels_train, labels_test)
        elif algorithm == c.LINEAR_REGRESSION:
            return _linear_regression(features_train, features_test, labels_train, labels_test)
        elif algorithm == c.BOOSTED_DECISION_TREES:
            return _boosted_decision_trees(features_train, features_test, labels_train, labels_test)
        elif algorithm == c.DECISION_TREE:
            return _decision_tree(features_train, features_test, labels_train, labels_test)
        else:
            # TODO: raise error
            pass
    except RuntimeError as error:
        message = f"{str(error)}"
        raise Exception(message)


def _random_forest(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
):
    rfc = RandomForestClassifier(
        n_estimators=c.RF_MAX_ITERATIONS,
        max_depth=c.RF_MAX_DEPTH
    )
    rfc.fit(features_train, labels_train)
    rfc_predictions = rfc.predict(features_test)

    result = _get_result_for_classification(labels_test, rfc_predictions)
    return result


def _logistic_regression(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame
):
    lrc = LogisticRegression(
        max_iter=c.LC_MAX_ITERATIONS
    )
    lrc.fit(features_train, labels_train)
    lrc_predictions = lrc.predict(features_test)

    result = _get_result_for_classification(labels_test, lrc_predictions)
    return result


def _support_vector_machines(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame
):
    svmc = svm.SVC(kernel='linear')
    svmc.fit(features_train, labels_train)
    svmc_predictions = svmc.predict(features_test)

    result = _get_result_for_classification(labels_test, svmc_predictions)
    return result


def _linear_regression(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
):
    lr = LinearRegression()
    lr.fit(features_train, labels_train)
    lr_predictions = lr.predict(features_test)

    result = _get_result_for_regression(labels_test, lr_predictions)
    return result


def _boosted_decision_trees(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
):
    gbr = GradientBoostingRegressor(max_depth=c.BDT_MAX_ITERATIONS)
    gbr.fit(features_train, labels_train)
    gbr_predictions = gbr.predict(features_test)

    result = _get_result_for_regression(labels_test, gbr_predictions)
    return result


def _decision_tree(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
):
    dtr = DecisionTreeRegressor(max_depth=c.DT_MAX_DEPTH)
    dtr.fit(features_train, labels_train)
    dtr_predictions = dtr.predict(features_test)

    result = _get_result_for_regression(labels_test, dtr_predictions)
    return result


def _get_result_for_classification(y_true, y_pred):
    result = classification_report(y_true, y_pred, output_dict=True)
    result["confusion_matrix"] = pandas.DataFrame(confusion_matrix(y_true, y_pred)).to_string()
    return result


def _get_result_for_regression(y_true, y_pred):
    result = {
        "rmse": sqrt(mean_squared_error(y_true, y_pred)),
        "max_error": max_error(y_true, y_pred)
    }
    return result
