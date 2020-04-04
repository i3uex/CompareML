import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

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
        return _random_forest(features_train, features_test, labels_train, labels_test)
    elif algorithm == c.LOGISTIC_REGRESSION:
        return _logistic_regression(features_train, features_test, labels_train, labels_test)
    elif algorithm == c.SUPPORT_VECTOR_MACHINES:
        return _support_vector_machines(features_train, features_test, labels_train, labels_test)
    else:
        # TODO: raise error
        pass


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

    result = _get_result(labels_test, rfc_predictions)
    return result


def _logistic_regression(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame
):
    lrc = LogisticRegression(max_iter=c.LC_MAX_ITERATIONS)
    lrc.fit(features_train, labels_train)
    lrc_predictions = lrc.predict(features_test)

    result = _get_result(labels_test, lrc_predictions)
    return result


def _support_vector_machines(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame
):
    return ""


def _get_result(y_true, y_pred):
    result = classification_report(y_true, y_pred, output_dict=True)
    result["confusion_matrix"] = pandas.DataFrame(confusion_matrix(y_true, y_pred)).to_string()
    return result
