from io import StringIO

import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

import constants as c


def execute(dataset, algorithm, target):
    dataframe = pandas.read_csv(StringIO(dataset))

    if algorithm == c.RANDOM_FOREST:
        return _random_forest(dataframe, target)
    else:
        # TODO: raise error
        pass


def _random_forest(dataframe, target):
    target_values = dataframe.pop(target).to_numpy()
    feat_values = dataframe.to_numpy()
    features_train, features_test, labels_train, labels_test = train_test_split(feat_values, target_values,
                                                                                test_size=0.2,
                                                                                random_state=1)
    rfc = RandomForestClassifier()
    rfc.fit(features_train, labels_train)
    rfc_predictions = rfc.predict(features_test)

    return classification_report(labels_test, rfc_predictions, output_dict=True)
