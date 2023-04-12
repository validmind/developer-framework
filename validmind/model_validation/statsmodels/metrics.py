"""
Metrics functions models trained with statsmodels or that provide
a statsmodels-like API
"""
from dataclasses import dataclass
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.diagnostic import kstest_normal
from arch.unitroot import PhillipsPerron
from ...vm_models import Metric


@dataclass
class KolmogorovSmirnovTest(Metric):
    """
    The Kolmogorov-Smirnov metric is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "kolmogorov_smirnov"

    def run(self):
        """
        Calculates KS for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        ks_values = {}
        for col in x_train.columns:
            ks_values[col] = kstest_normal(x_train[col].values)

        return self.cache_results(ks_values)


@dataclass
class JarqueBeraTest(Metric):
    """
    The Jarque-Bera test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "jarque_bera"

    def run(self):
        """
        Calculates JB for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        jb_values = {}
        for col in x_train.columns:
            jb_values[col] = jarque_bera(x_train[col].values)

        return self.cache_results(jb_values)


@dataclass
class LJungBoxTest(Metric):
    """
    The LJung-Box Metric is a statistical test that
    can be used to detect autocorrelation in a time series.
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "ljung_box"

    def run(self):
        """
        Calculates LB for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        lb_values = {}
        for col in x_train.columns:
            lb_values[col] = acorr_ljungbox(x_train[col].values, lags=None)[
                "lb_pvalue"
            ].tolist()

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
    Augmented Dickey-Fuller unit root test for establishing the order of integration of
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
            adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(
                x_train[col].values
            )
            adf_values["adf"] = adf
            adf_values["pvalue"] = pvalue
            adf_values["usedlag"] = usedlag
            adf_values["nobs"] = nobs
            adf_values["icbest"] = icbest

        return self.cache_results(adf_values)


@dataclass
class PhillipsPerronTest(Metric):
    """
    Phillips-Perron (PP) Test unit root test for 
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "pp"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates PP for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        pp_values = {}
        for col in x_train.columns:
            pp = PhillipsPerron(x_train[col].values)
            pp_values["pp"] = pp.stat
            pp_values["pvalue"] = pp.pvalue
            pp_values["usedlag"] = pp.lags

        return self.cache_results(pp_values)
    

@dataclass
class KPSSTest(Metric):
    """
    Kwiatkowski-Phillips-Schmidt-Shin (KPSS) unit root test for 
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "kpss"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates KPSS for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        kpss_values = {}
        for col in x_train.columns:
            kpss_stat, pvalue, usedlag, critical_values = kpss(
                x_train[col].values
            )
            kpss_values["kpss"] = kpss_stat
            kpss_values["pvalue"] = pvalue
            kpss_values["usedlag"] = usedlag

        return self.cache_results(kpss_values)