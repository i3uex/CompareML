import turicreate as tc

import constants as c


def execute(dataset, algorithm, target):
    if algorithm == c.RANDOM_FOREST:
        return _random_forest(dataset, target)
    else:
        # TODO: raise error
        pass


def _random_forest(dataset, target):
    # Load the data (didn't find other way than using tempfile to create a SFrame from string)
    with open(c.TEMP_FILEPATH, 'w') as tempfile:
        tempfile.write(dataset)
    data = tc.SFrame.read_csv(c.TEMP_FILEPATH)

    # Make a train-test split
    train_data, test_data = data.random_split(0.8)

    # Create a model.
    model = tc.random_forest_classifier.create(train_data, target=target,
                                               max_iterations=2,
                                               max_depth=3)

    # Evaluate the model and save the results into a dictionary
    results = model.evaluate(test_data)

    if 'roc_curve' in results:
        del results['roc_curve']
    if 'confusion_matrix' in results:
        results['confusion_matrix'] = '"\n' + str(results['confusion_matrix']) + '"'

    return results
