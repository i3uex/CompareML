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


def execute(dataset, providers: [], algorithms: [], target: str):
    results = {}
    for algorithm in algorithms:
        for provider in providers:
            if provider not in results:
                results[provider] = {}
            results[provider][algorithm] = PROVIDERS[provider].execute(dataset, algorithm, target)

    return str(results)
