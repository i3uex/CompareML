import os

import pandas
import subprocess

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
    elif algorithm == c.SUPPORT_VECTOR_MACHINES:
        return _support_vector_machines(target)
    else:
        # TODO: raise error
        pass


def _random_forest(target: str):
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

    return result
