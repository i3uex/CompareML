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
        return _neural_network_mp(target)
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
    return {'result': output.decode('utf-8').replace('\'', '-')}


def _logistic_regression(target: str):
    temp_dir = os.path.abspath("temp")
    script = os.path.abspath("providers/r/logistic_regression.r")
    output = subprocess.check_output([
        "Rscript", script,
        "--path", temp_dir,
        "--target", target,
        "--maximum_iterations", str(c.LC_MAX_ITERATIONS)
    ])
    return {'result': output.decode('utf-8').replace('\'', '-')}


def _support_vector_machines(target: str):
    return ""
