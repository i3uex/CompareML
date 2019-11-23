import cherrypy

import constants as c
import providers.TuriGraphlab as TuriGraphlab
import json


class Engine:

    def __init__(self):
        self.dataset = ''
        self.providers = {
            c.TURI_GRAPHLAB: TuriGraphlab
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
        result = ''
        for algorithm in algorithms:
            for provider in providers:
                result = self.providers[provider].execute(self.dataset, algorithm, target)

        return result
