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
    train_data_sf, test_data_sf = _get_sframes(features_train, features_test, labels_train, labels_test)
    if algorithm == c.RANDOM_FOREST:
        return _random_forest(train_data_sf, test_data_sf, target)
    elif algorithm == c.LOGISTIC_REGRESSION:
        return _logistic_regression(train_data_sf, test_data_sf, target)
    elif algorithm == c.SUPPORT_VECTOR_MACHINES:
        return _support_vector_machines(train_data_sf, test_data_sf, target)
    else:
        # TODO: raise error
        pass


def _random_forest(
    train_data_sf: SFrame,
    test_data_sf: SFrame,
    target: str
):
    # Create a model.
    model = tc.random_forest_classifier.create(
        train_data_sf, target=target,
        max_iterations=c.RF_MAX_ITERATIONS,
        max_depth=c.RF_MAX_DEPTH,
        verbose=False
    )

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data_sf)
    results = _process_results(results)

    return results


def _logistic_regression(
    train_data_sf: SFrame,
    test_data_sf: SFrame,
    target: str
):
    model = tc.logistic_classifier.create(
        train_data_sf,
        target=target,
        max_iterations=c.LC_MAX_ITERATIONS,
        verbose=False
    )

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data_sf)
    results = _process_results(results)

    return results


def _support_vector_machines(
    train_data_sf: SFrame,
    test_data_sf: SFrame,
    target: str
):
    model = tc.svm_classifier.create(
        train_data_sf,
        target=target,
        max_iterations=c.SVM_MAX_ITERATIONS,
        verbose=False
    )

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data_sf)
    results = _process_results(results)

    return results


def _get_sframes(features_train, features_test, labels_train, labels_test):
    train_data: pandas.DataFrame = features_train.join(labels_train)
    test_data: pandas.DataFrame = features_test.join(labels_test)

    train_data_sf = SFrame(data=train_data)
    test_data_sf = SFrame(data=test_data)

    return train_data_sf, test_data_sf


def _process_results(results):
    if 'roc_curve' in results:
        del results['roc_curve']
    if 'confusion_matrix' in results:
        results['confusion_matrix'] = '"\n' + str(results['confusion_matrix']) + '"'
    return results
