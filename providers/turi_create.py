import logging

import cherrypy
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
    logging.debug(f"turi.execute()")
    try:
        train_data_sf, test_data_sf = _get_sframes(
            features_train, features_test, labels_train, labels_test)
        if algorithm == c.LINEAR_REGRESSION:
            return _linear_regression(train_data_sf, test_data_sf, target)
        elif algorithm == c.BOOSTED_DECISION_TREES:
            return _boosted_decision_trees(train_data_sf, test_data_sf, target)
        elif algorithm == c.DECISION_TREE:
            return _decision_tree(train_data_sf, test_data_sf, target)
        elif algorithm == c.RANDOM_FOREST:
            return _random_forest(train_data_sf, test_data_sf, target)
        elif algorithm == c.LOGISTIC_REGRESSION:
            return _logistic_regression(train_data_sf, test_data_sf, target)
        elif algorithm == c.SUPPORT_VECTOR_MACHINES:
            return _support_vector_machines(train_data_sf, test_data_sf, target)
        else:
            raise NotImplementedError
    except RuntimeError as error:
        message = f"{str(error)}"
        raise Exception(message)


def _linear_regression(
    train_data_sf: SFrame,
    test_data_sf: SFrame,
    target: str
):
    logging.debug(f"turi._linear_regression()")

    # Create a model.
    model = tc.linear_regression.create(
        train_data_sf,
        target=target,
        verbose=False
    )
    lr_predictions = model.predict(test_data_sf)

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data_sf)
    results = _process_results(
        results, test_data_sf, lr_predictions, c.LINEAR_REGRESSION)

    return results


def _boosted_decision_trees(
    train_data_sf: SFrame,
    test_data_sf: SFrame,
    target: str
):
    logging.debug(f"turi._boosted_decision_trees()")

    # Create a model.
    model = tc.boosted_trees_regression.create(
        train_data_sf,
        target=target,
        verbose=False,
        max_iterations=c.BDT_MAX_ITERATIONS
    )
    btr_predictions = model.predict(test_data_sf)

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data_sf)
    results = _process_results(
        results, test_data_sf, btr_predictions, c.BOOSTED_DECISION_TREES)

    return results


def _decision_tree(
    train_data_sf: SFrame,
    test_data_sf: SFrame,
    target: str
):
    logging.debug(f"turi._decision_tree()")

    # Create a model.
    model = tc.decision_tree_regression.create(
        train_data_sf,
        target=target,
        max_depth=c.DT_MAX_DEPTH,
        verbose=False
    )
    dtr_predictions = model.predict(test_data_sf)

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data_sf)
    results = _process_results(
        results, test_data_sf, dtr_predictions, c.DECISION_TREE)

    return results


def _random_forest(
    train_data_sf: SFrame,
    test_data_sf: SFrame,
    target: str
):
    logging.debug(f"turi._random_forest()")

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
    logging.debug(f"turi._logistic_regression()")

    # Create a model.
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
    logging.debug(f"turi._support_vector_machines()")

    # Create a model.
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
    logging.debug(f"turi._get_sframes()")

    train_data: pandas.DataFrame = features_train.join(labels_train)
    test_data: pandas.DataFrame = features_test.join(labels_test)

    train_data_sf = SFrame(data=train_data)
    test_data_sf = SFrame(data=test_data)

    return train_data_sf, test_data_sf


def _process_results(
        results,
        test_data_sf=None,
        predictions=None,
        algorithm=None):
    logging.debug(f"turi._process_results()")

    if 'roc_curve' in results:
        del results['roc_curve']
    if 'confusion_matrix' in results:
        results['confusion_matrix'] = '"\n' + str(results['confusion_matrix']) + '"'

    if algorithm == c.LINEAR_REGRESSION or algorithm == c.BOOSTED_DECISION_TREES or algorithm == c.DECISION_TREE:
        r2_score = _get_r2_score(test_data_sf, predictions)
        results['r2_score'] = r2_score

    return results


def _get_r2_score(test_data_sf, y_pred):
    logging.debug(f"turi._get_r2_score()")

    column_names = test_data_sf.column_names()
    last_column_name = column_names[-1]
    y_true = test_data_sf.select_column(last_column_name)

    rss = ((y_pred - y_true) ** 2).sum()
    tss = ((y_true - y_true.mean()) ** 2).sum()
    rsq = 1 - rss / tss

    return rsq

    # preds < - c(1, 2, 3)
    # actual < - c(2, 2, 4)
    # rss < - sum((preds - actual) ^ 2)
    # tss < - sum((actual - mean(actual)) ^ 2)
    # rsq < - 1 - rss / tss

