"""
Metrics functions models trained with statsmodels or that provide
a statsmodels-like API
"""
import pandas as pd
from dataclasses import dataclass
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from ...vm_models import Metric


@dataclass
class LJungBoxTest(Metric):
    """
    The LJung-Box Metric is a statistical test that 
    can be used to detect autocorrelation in a time series.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "ljung_box"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates LB for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        lb_values = {}
        for col in x_train.columns:
            # Aggregate of the ljb results for the first 25 lags
            lb_values[col] = acorr_ljungbox(x_train[col].values, lags=None)['lb_pvalue']

        return self.cache_results(lb_values)

@dataclass
class DurbinWatsonTest(Metric):
    """
    The Durbin-Watson Metric is a statistical test that 
    can be used to detect autocorrelation in a time series.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "durbin_watson"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates DB for each of the dataset features
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
            # adf_values[col] = adfuller(x_train[col].values)
            adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(x_train[col].values)
            adf_values["adf" ] = adf
            adf_values['pvalue'] = pvalue
            adf_values['usedlag'] = usedlag
            adf_values['nobs'] = nobs
            adf_values['icbest'] = icbest
        
        return self.cache_results(adf_values)
