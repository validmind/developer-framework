"""
Metrics functions models trained with statsmodels or that provide
a statsmodels-like API
"""
from dataclasses import dataclass
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.stattools import durbin_watson
from ...vm_models import Metric

@dataclass
class DurbinWatsonTest(Metric):
    """
    Durbin-Watson Metric
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "durbin_watson"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates PSI for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        dw_values = {}
        for col in x_train.columns:
            dw_values[col] = durbin_watson(x_train[col].values)

        return self.cache_results(dw_values)

@dataclass
class ADFTest(Metric):
    """
    Augmented Dickey-Fuller Metric for establishing the order of integration of 
    time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "adf"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates ADF for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        adf_values = {}
        for col in x_train.columns:
            adf_values[col] = adfuller(x_train[col].values)

        return self.cache_results(adf_values)
