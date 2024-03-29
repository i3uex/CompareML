import logging
import os
from io import StringIO

import pandas
from pandas.core.dtypes.common import is_numeric_dtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import constants as c
import providers.r as r
import providers.scikit_learn as scikitLearn
import providers.turi_create as turi_create

PROVIDERS = {
    c.TURI_CREATE: turi_create,
    c.SCIKIT_LEARN: scikitLearn,
    c.R: r,
}

ALGORITHMS = {
    'classification': [
        c.RANDOM_FOREST,
        c.LOGISTIC_REGRESSION,
        c.SUPPORT_VECTOR_MACHINES
    ],
    'regression': [
        c.LINEAR_REGRESSION,
        c.BOOSTED_DECISION_TREES,
        c.DECISION_TREE
    ]
}


def get_all_default_datasets():
    logging.debug(f"engine.get_all_default_datasets()")
    return list(map(lambda filename: filename.replace('.csv', ''), os.listdir(c.EXAMPLE_DATASETS_PATH)))


def get_providers():
    """ :return List of providers
    [provider1, provider2]"""
    logging.debug(f"engine.get_providers()")
    return list(PROVIDERS.keys())


def get_algorithms():
    """ :return Dictionary with algorithms
    {
        'classification': [ 'classification_algorithm1', 'classification_algorithm2' ],
        'regression': [ 'regression_algorithm1', 'regression_algorithm2' ]
    } """
    logging.debug(f"engine.get_algorithms()")
    return ALGORITHMS


def get_default_dataset_headers(default_dataset_name: str) -> []:
    logging.debug(f"engine.get_default_dataset_headers()")
    with open(c.EXAMPLE_DATASETS_PATH + default_dataset_name + '.csv', 'r') as dataset_file:
        header: str = dataset_file.readline().replace('\n', '')
        headers: [] = header.split(',')

    return headers


def _split_dataset(dataset: str, target: str):
    logging.debug(f"engine._split_dataset()")
    features_values = pandas.read_csv(StringIO(dataset))
    target_values = features_values.pop(target)

    # Do OneHotEncoding for categorical features:
    features_values = _do_one_hot_encoding(features_values)

    # Split
    features_train, features_test, labels_train, labels_test = train_test_split(features_values, target_values,
                                                                                test_size=0.2, random_state=0)
    # Add target label
    labels_train = labels_train.to_frame(target)
    labels_test = labels_test.to_frame(target)

    # Save to temp folder as CSV
    features_test.to_csv(index=False, path_or_buf='temp/features_test.csv')
    features_train.to_csv(index=False, path_or_buf='temp/features_train.csv')
    labels_train.to_csv(index=False, path_or_buf='temp/labels_train.csv')
    labels_test.to_csv(index=False, path_or_buf='temp/labels_test.csv')

    return features_train, features_test, labels_train, labels_test


def _do_one_hot_encoding(features_values):
    logging.debug(f"engine._do_one_hot_encoding()")
    for col in features_values:
        if not is_numeric_dtype(features_values[col]):
            # One Hot Encoding
            encoder = OneHotEncoder(handle_unknown='ignore')
            encoded_df = pandas.DataFrame(encoder.fit_transform(features_values[[col]]).toarray())
            encoded_df = encoded_df.add_prefix(col + '_')

            features_values = features_values.join(encoded_df)

            # Drop original column
            features_values = features_values.drop(col, axis=1)

    return features_values


def execute(is_default_dataset: bool, dataset: str, providers: [], algorithms: [], target: str):
    logging.debug(f"engine.execute()")
    if is_default_dataset:
        with open(c.EXAMPLE_DATASETS_PATH + dataset + '.csv', 'r') as dataset_file:
            dataset = dataset_file.read()

    features_train, features_test, labels_train, labels_test = _split_dataset(dataset, target)

    results = {}
    for algorithm in algorithms:
        for provider in providers:
            if provider not in results:
                results[provider] = {}
            try:
                results[provider][algorithm] = PROVIDERS[provider].execute(features_train, features_test, labels_train,
                                                                       labels_test, algorithm, target)
            except Exception as exception:
                message = f"{str(exception)}"
                raise Exception(message)

    return str(results)
