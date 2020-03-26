import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

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
    elif algorithm == c.NEURAL_NETWORK_MP:
        return _neural_network_mp(features_train, features_test, labels_train, labels_test)
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
        max_depth=c.RF_MAX_DEPTH
    )
    rfc.fit(features_train, labels_train)
    rfc_predictions = rfc.predict(features_test)

    return classification_report(labels_test, rfc_predictions, output_dict=True)


def _logistic_regression(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame
):
    return ""


def _neural_network_mp(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame
):
    return ""
