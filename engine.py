from io import StringIO

import cherrypy
import pandas
from sklearn.model_selection import train_test_split

import constants as c
import providers.ScikitLearn as ScikitLearn
import providers.TuriGraphlab as TuriGraphlab

PROVIDERS = {
    c.TURI_GRAPHLAB: TuriGraphlab,
    c.SCIKIT_LEARN: ScikitLearn
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


def split_dataset(dataset: str, target: str):
    features_values = pandas.read_csv(StringIO(dataset))
    target_values = features_values.pop(target)
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


def execute(dataset: str, providers: [], algorithms: [], target: str):
    features_train, features_test, labels_train, labels_test = split_dataset(dataset, target)

    results = {}
    for algorithm in algorithms:
        for provider in providers:
            if provider not in results:
                results[provider] = {}
            results[provider][algorithm] = PROVIDERS[provider].execute(features_train, features_test, labels_train,
                                                                       labels_test, algorithm, target)

    return str(results)
