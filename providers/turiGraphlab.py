import pandas
import turicreate as tc
from turicreate import SFrame

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
        return _random_forest(features_train, features_test, labels_train, labels_test, target)
    elif algorithm == c.LOGISTIC_REGRESSION:
        return _logistic_regression(features_train, features_test, labels_train, labels_test, target)
    elif algorithm == c.NEURAL_NETWORK_MP:
        return _neural_network_mp(features_train, features_test, labels_train, labels_test, target)
    else:
        # TODO: raise error
        pass


def _random_forest(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
        target: str
):
    train_data_sf, test_data_sf = _get_sframes(features_train, features_test, labels_train, labels_test)

    # Create a model.
    model = tc.random_forest_classifier.create(train_data_sf, target=target,
                                               max_iterations=2,
                                               max_depth=3,
                                               verbose=False)

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data_sf)

    if 'roc_curve' in results:
        del results['roc_curve']
    if 'confusion_matrix' in results:
        results['confusion_matrix'] = '"\n' + str(results['confusion_matrix']) + '"'

    return results


def _logistic_regression(
    features_train: pandas.DataFrame,
    features_test: pandas.DataFrame,
    labels_train: pandas.DataFrame,
    labels_test: pandas.DataFrame,
    target: str
):
    train_data_sf, test_data_sf = _get_sframes(features_train, features_test, labels_train, labels_test)

    return ""


def _neural_network_mp(
    features_train: pandas.DataFrame,
    features_test: pandas.DataFrame,
    labels_train: pandas.DataFrame,
    labels_test: pandas.DataFrame,
    target: str
):
    train_data_sf, test_data_sf = _get_sframes(features_train, features_test, labels_train, labels_test)

    return ""


def _get_sframes(features_train, features_test, labels_train, labels_test):
    train_data: pandas.DataFrame = features_train.join(labels_train)
    test_data: pandas.DataFrame = features_test.join(labels_test)

    train_data_sf = SFrame(data=train_data)
    test_data_sf = SFrame(data=test_data)

    return train_data_sf, test_data_sf
