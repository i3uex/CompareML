from io import StringIO

import pandas
from pandas.api.types import is_numeric_dtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

import constants as c
import providers.r as r
import providers.scikitLearn as scikitLearn
import providers.turiGraphlab as turiGraphlab

PROVIDERS = {
    c.TURI_GRAPHLAB: turiGraphlab,
    c.SCIKIT_LEARN: scikitLearn,
    c.R: r,
}

ALGORITHMS = {
    'classification': [
        c.RANDOM_FOREST
    ],
    'regression': [

    ]
}


def getProviders():
    """ :return List of providers
    [provider1, provider2]"""
    return list(PROVIDERS.keys())


def getAlgorithms():
    """ :return Dictionary with algorithms
    {
        'classification': [ 'classification_algorithm1', 'classification_algorithm2' ],
        'regression': [ 'regression_algorithm1', 'regression_algorithm2' ]
    } """
    return ALGORITHMS


def _split_dataset(dataset: str, target: str):
    features_values = pandas.read_csv(StringIO(dataset))
    target_values = features_values.pop(target)

    # Do OneHotEncoding for categorical features:
    features_values = _doOneHotEncoding(features_values)

    # Split
    features_train, features_test, labels_train, labels_test = train_test_split(features_values, target_values,
                                                                                test_size=0.2)
    # Add target label
    labels_train = labels_train.to_frame(target)
    labels_test = labels_test.to_frame(target)

    # Save to temp folder as CSV
    features_test.to_csv(index=False, path_or_buf='temp/features_test.csv')
    features_train.to_csv(index=False, path_or_buf='temp/features_train.csv')
    labels_train.to_csv(index=False, path_or_buf='temp/labels_train.csv')
    labels_test.to_csv(index=False, path_or_buf='temp/labels_test.csv')

    return features_train, features_test, labels_train, labels_test


def _doOneHotEncoding(features_values):
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


def execute(dataset: str, providers: [], algorithms: [], target: str):
    features_train, features_test, labels_train, labels_test = _split_dataset(dataset, target)

    results = {}
    for algorithm in algorithms:
        for provider in providers:
            if provider not in results:
                results[provider] = {}
            results[provider][algorithm] = PROVIDERS[provider].execute(features_train, features_test, labels_train,
                                                                       labels_test, algorithm, target)

    return str(results)
