"""
Metrics functions models trained with statsmodels or that provide
a statsmodels-like API
"""
from dataclasses import dataclass
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.diagnostic import kstest_normal
from arch.unitroot import PhillipsPerron
from arch.unitroot import ZivotAndrews
from arch.unitroot import DFGLS
from ...vm_models import Figure, Metric
import matplotlib.pyplot as plt


@dataclass
class SeasonalDecomposeMetricWithFigure(Metric):
    """
    Calculates seasonal_decomponse metric for each of the dataset features
    """

    type = "dataset"
    key = "seasonal_decomposition_with_figure"

    def run(self):

        x_train = self.train_ds.raw_dataset

        sd_values = {}
        for col in x_train.columns:
            sd = seasonal_decompose(
                x_train[col], model="additive"
            )  # Use 'multiplicative' for a multiplicative model

            sd_values["trend"] = sd.trend
            sd_values["seasonal"] = sd.seasonal
            sd_values["resid"] = sd.resid
            sd_values["observed"] = sd.observed

            # Create a random histogram with matplotlib
            fig, (ax_observed, ax_trend, ax_seasonal, ax_resid) = plt.subplots(
                nrows=4, ncols=1
            )

            ax_observed.set_title("Observed")
            ax_trend.set_title("Trend")
            ax_seasonal.set_title("Seasonal")
            ax_resid.set_title("Residuals")
            ax_resid.set_xlabel("Date")

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figure = Figure(key=self.key, figure=fig, metadata={})

        return self.cache_results(sd_values, figures=[figure])


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
        Calculates ADF metric for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        adf_values = {}
        for col in x_train.columns:
            # adf_values[col] = adfuller(x_train[col].values)
            adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(
                x_train[col].values
            )
            adf_values["stat"] = adf
            adf_values["pvalue"] = pvalue
            adf_values["usedlag"] = usedlag
            adf_values["nobs"] = nobs
            adf_values["icbest"] = icbest

        return self.cache_results(adf_values)


@dataclass
class PhillipsPerronTest(Metric):
    """
    Phillips-Perron (PP) unit root test for
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "phillips_perron"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates PP metric for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        pp_values = {}
        for col in x_train.columns:
            pp = PhillipsPerron(x_train[col].values)
            pp_values["stat"] = pp.stat
            pp_values["pvalue"] = pp.pvalue
            pp_values["usedlag"] = pp.lags
            pp_values["nobs"] = pp.nobs

        return self.cache_results(pp_values)


@dataclass
class ZivotAndrewsTest(Metric):
    """
    Zivot-Andrews unit root test for
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "zivot_andrews"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates Zivot-Andrews metric for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        za_values = {}
        for col in x_train.columns:
            za = ZivotAndrews(x_train[col].values)
            za_values["stat"] = za.stat
            za_values["pvalue"] = za.pvalue
            za_values["usedlag"] = za.lags
            za_values["nobs"] = za.nobs

        return self.cache_results(za_values)


@dataclass
class DFGLSTest(Metric):
    """
    Dickey-Fuller GLS unit root test for
    establishing the order of integration of time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "dickey_fuller_gls"
    value_formatter = "key_values"

    def run(self):
        """
        Calculates Dickey-Fuller GLS metric for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        dfgls_values = {}
        for col in x_train.columns:
            dfgls_out = DFGLS(x_train[col].values)
            dfgls_values["stat"] = dfgls_out.stat
            dfgls_values["pvalue"] = dfgls_out.pvalue
            dfgls_values["usedlag"] = dfgls_out.lags
            dfgls_values["nobs"] = dfgls_out.nobs

        return self.cache_results(dfgls_values)


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
            kpss_stat, pvalue, usedlag, critical_values = kpss(x_train[col].values)
            kpss_values["stat"] = kpss_stat
            kpss_values["pvalue"] = pvalue
            kpss_values["usedlag"] = usedlag

        return self.cache_results(kpss_values)
