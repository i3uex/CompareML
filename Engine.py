import cherrypy
from providers.TuriGraphlab import TuriGraphlab


class Engine:
    dataset: str

    def __init__(self):
        self.providers = {
            'Turi Graphlab': TuriGraphlab
        }

        self.algorithms = {
            'classification': [
                'Random Forest'
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

    def execute(self, providers: [], algorithms: []):
        for algorithm in algorithms:
            for provider in providers:
                res = self.providers[provider].execute(algorithm)
                cherrypy.log(res)

        # result = {
        #     'algorithm': {
        #         'a1': {
        #
        #         }
        #     }
        # }
        return result
