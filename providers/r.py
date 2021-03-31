import logging
import os
import subprocess

import pandas

import constants as c


def execute(
        features_train: pandas.DataFrame,
        features_test: pandas.DataFrame,
        labels_train: pandas.DataFrame,
        labels_test: pandas.DataFrame,
        algorithm: str,
        target: str
):
    logging.debug(f"r.execute()")
    try:
        if algorithm == c.LINEAR_REGRESSION:
            return _linear_regression(target)
        elif algorithm == c.BOOSTED_DECISION_TREES:
            return _boosted_decision_trees(target)
        elif algorithm == c.DECISION_TREE:
            return _decision_tree(target)
        elif algorithm == c.RANDOM_FOREST:
            return _random_forest(target)
        elif algorithm == c.LOGISTIC_REGRESSION:
            return _logistic_regression(target)
        elif algorithm == c.SUPPORT_VECTOR_MACHINES:
            return _support_vector_machines(target)
        else:
            raise NotImplementedError
    except RuntimeError as error:
        message = f"{str(error)}"
        raise Exception(message)


def _linear_regression(target: str):
    logging.debug(f"r._linear_regression()")
    temp_dir = os.path.abspath("temp")
    script = os.path.abspath("providers/r/linear_regression.r")
    output = subprocess.check_output([
        "Rscript", script,
        "--path", temp_dir,
        "--target", target
    ])
    result = _get_result_regression(output)
    return result


def _boosted_decision_trees(target: str):
    logging.debug(f"r._boosted_decision_trees()")
    temp_dir = os.path.abspath("temp")
    script = os.path.abspath("providers/r/boosted_decision_trees.r")
    output = subprocess.check_output([
        "Rscript", script,
        "--path", temp_dir,
        "--target", target,
        "--trees", str(c.BDT_MAX_ITERATIONS)
    ])
    result = _get_result_regression(output)
    return result


def _decision_tree(target: str):
    logging.debug(f"r._decision_tree()")
    temp_dir = os.path.abspath("temp")
    script = os.path.abspath("providers/r/decision_tree.r")
    output = subprocess.check_output([
        "Rscript", script,
        "--path", temp_dir,
        "--target", target,
        "--maximum_depth", str(c.DT_MAX_DEPTH)
    ])
    result = _get_result_regression(output)
    return result


def _random_forest(target: str):
    logging.debug(f"r._random_forest()")
    temp_dir = os.path.abspath("temp")
    script = os.path.abspath("providers/r/random_forest.r")
    output = subprocess.check_output([
        "Rscript", script,
        "--path", temp_dir,
        "--target", target,
        "--maximum_iterations", str(c.RF_MAX_ITERATIONS),
        "--maximum_depth", str(c.RF_MAX_DEPTH)
    ])
    result = _get_result_classification(output)
    return result


def _logistic_regression(target: str):
    logging.debug(f"r._logistic_regression()")
    temp_dir = os.path.abspath("temp")
    script = os.path.abspath("providers/r/logistic_regression.r")
    output = subprocess.check_output([
        "Rscript", script,
        "--path", temp_dir,
        "--target", target,
        "--maximum_iterations", str(c.LC_MAX_ITERATIONS)
    ])
    result = _get_result_classification(output)
    return result


def _support_vector_machines(target: str):
    logging.debug(f"r._support_vector_machines()")
    temp_dir = os.path.abspath("temp")
    script = os.path.abspath("providers/r/support_vector_machines.r")
    output = subprocess.check_output([
        "Rscript", script,
        "--path", temp_dir,
        "--target", target
    ])
    result = _get_result_classification(output)
    return result


def _get_result_classification(output):
    logging.debug(f"r._get_result_classification()")
    result_string = output.decode('utf-8').replace('\'', '-')

    confusion_matrix_end = result_string.find("Accuracy")
    confusion_matrix = result_string[:confusion_matrix_end]
    confusion_matrix = confusion_matrix.rstrip()
    confusion_matrix = confusion_matrix.replace("Confusion Matrix and Statistics\n\n", "")

    statistics = result_string[confusion_matrix_end:]
    result_list = statistics.split("\n")

    result_list_split = []
    for i in range(len(result_list)):
        result_list_item = result_list[i].strip()
        if result_list_item != "":
            result_list_split.extend(result_list_item.split(":"))

    for i in range(len(result_list_split)):
        result_list_split[i] = result_list_split[i].strip()
    result_list_split.insert(0, "Confusion Matrix")
    result_list_split.insert(1, confusion_matrix)

    result = {}
    for i in range(0, len(result_list_split), 2):
        key = result_list_split[i]
        value = result_list_split[i + 1]
        result[key] = value

    print(f"result: {result}")
    return result


def _get_result_regression(output):
    logging.debug(f"r._get_result_regression()")
    result_string = output.decode('utf-8')
    result_list_split = result_string.split(":")
    result = {}
    for i in range(0, len(result_list_split), 2):
        key = result_list_split[i]
        value = result_list_split[i + 1]
        result[key] = value
    print(f"result: {result}")
    return result
