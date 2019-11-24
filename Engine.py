import constants as c
import providers.ScikitLearn as ScikitLearn
import providers.TuriGraphlab as TuriGraphlab


class Engine:

    def __init__(self):
        self.dataset = ''
        self.providers = {
            c.TURI_GRAPHLAB: TuriGraphlab,
            c.SCIKIT_LEARN: ScikitLearn
        }

        self.algorithms = {
            'classification': [
                c.RANDOM_FOREST
            ],
            'regression': [

            ]
        }

    def setDataset(self, dataset: str):
        self.dataset = dataset

    def getProviders(self):
        """ :return List of providers
        [provider1, provider2]"""
        return list(self.providers.keys())

    def getAlgorithms(self):
        """ :return Dictionary with algorithms
        {
            'classification': [ 'classification_algorithm1', 'classification_algorithm2' ],
            'regression': [ 'regression_algorithm1', 'regression_algorithm2' ]
        } """
        return self.algorithms

    def execute(self, providers: [], algorithms: [], target: str):
        results = {}
        for algorithm in algorithms:
            for provider in providers:
                if provider not in results:
                    results[provider] = {}
                results[provider][algorithm] = self.providers[provider].execute(self.dataset, algorithm, target)

        return str(results)
