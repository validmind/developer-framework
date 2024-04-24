# Saved from __main__.hyperparameters
# Original Test ID: my_custom_metrics.Hyperparameters
# New Test ID: <test_provider_namespace>.Hyperparameters


def Hyperparameters(model):
    """The hyperparameters of a machine learning model are the settings that control the learning process.
    These settings are specified before the learning process begins and can have a significant impact on the
    performance of the model.

    The hyperparameters of a model can be used to tune the model to achieve the best possible performance
    on a given dataset. By examining the hyperparameters of a model, you can gain insight into how the model
    was trained and how it might be improved.
    """
    hyperparameters = model.model.get_xgb_params()  # dictionary of hyperparameters

    # turn the dictionary into a table where each row contains a hyperparameter and its value
    return [{"Hyperparam": k, "Value": v} for k, v in hyperparameters.items() if v]
