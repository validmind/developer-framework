"""
Metrics functions models trained with statsmodels or that provide
a statsmodels-like API
"""
from dataclasses import dataclass
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.sandbox.stats.runs import runstest_1samp
from statsmodels.stats.diagnostic import kstest_normal
from statsmodels.stats.diagnostic import lilliefors
from statsmodels.stats.stattools import jarque_bera
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf
from arch.unitroot import PhillipsPerron
from arch.unitroot import ZivotAndrews
from arch.unitroot import DFGLS
from ...vm_models import Figure, Metric


@dataclass
class ResidualsVisualInspection(Metric):
    """
    Log plots for visual inspection of residuals
    """

    type = "evaluation"
    key = "residuals_visual_inspection"

    @staticmethod
    def residual_analysis(residuals, variable_name, axes):
        residuals = residuals.dropna().reset_index(
            drop=True
        )  # drop NaN values and reset index

        # QQ plot
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title(f"Residuals Q-Q Plot ({variable_name})")

        # Histogram with KDE
        sns.histplot(residuals, kde=True, ax=axes[0, 0])
        axes[0, 0].set_xlabel("Residuals")
        axes[0, 0].set_title(f"Residuals Histogram ({variable_name})")

        # Residual series dot plot
        sns.lineplot(data=residuals, linewidth=0.5, color="red", ax=axes[1, 0])
        axes[1, 0].set_title(f"Residual Series Dot Plot ({variable_name})")

        # ACF plot
        n_lags = min(100, len(residuals) - 1)  # Adjust the number of lags
        plot_acf(residuals, ax=axes[1, 1], lags=n_lags, zero=False)  # Added zero=False
        axes[1, 1].set_title(f"ACF Plot of Residuals ({variable_name})")

    def run(self):
        x_train = self.train_ds.raw_dataset
        figures = []

        # TODO: specify which columns to plot via params
        for col in x_train.columns:
            sd = seasonal_decompose(x_train[col], model="additive")

            # Remove NaN values from the residuals and reset the index
            residuals = pd.Series(sd.resid).dropna().reset_index(drop=True)

            # Create subplots
            fig, axes = plt.subplots(nrows=2, ncols=2)

            self.residual_analysis(residuals, col, axes)

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=self.key, figure=fig, metadata={}))
        return self.cache_results(figures=figures)


class SeasonalityDetectionWithACF(Metric):
    """
    Detects seasonality in a time series dataset using ACF and PACF.
    """

    type = "evaluation"
    key = "seasonality_detection_with_acf"

    def calculate_acf(self, series, nlags=40):
        acf_values = acf(series, nlags=nlags)
        return acf_values

    def calculate_pacf(self, series, nlags=40):
        pacf_values = pacf(series, nlags=nlags)
        return pacf_values

    def find_seasonal_period(self, acf_values, threshold=0.2):
        peaks = np.where(acf_values > threshold)[0]
        if peaks.size == 0:
            return None
        return peaks[1] - peaks[0]

    def run(self):
        x_train = self.train_ds.raw_dataset

        results = {}
        figures = []

        for col in x_train.columns:
            series = x_train[col]
            acf_vals = self.calculate_acf(series)
            pacf_vals = self.calculate_pacf(series)

            seasonal_period = self.find_seasonal_period(acf_vals)

            results[col] = {
                "acf_values": acf_vals,
                "pacf_values": pacf_vals,
                "seasonal_period": seasonal_period,
            }

            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

            plot_acf(series, ax=ax1)
            plot_pacf(series, ax=ax2)

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=self.key, figure=fig, metadata={}))

        return self.cache_results(results=results, figures=figures)


class SeasonalDecompose(Metric):
    """
    Calculates seasonal_decompose metric for each of the dataset features
    """

    type = "evaluation"
    key = "seasonal_decompose"

    def run(self):
        x_train = self.train_ds.raw_dataset

        results = {}
        figures = []

        for col in x_train.columns:
            sd = seasonal_decompose(x_train[col], model="additive")

            results[col] = {
                "observed": sd.observed,
                "trend": sd.trend,
                "seasonal": sd.seasonal,
                "resid": sd.resid,
            }

            # Create subplots
            fig, axes = plt.subplots(nrows=1, ncols=4)
            fig.subplots_adjust(hspace=1)

            axes[0].set_title("Observed")
            sd.observed.plot(ax=axes[0])

            axes[1].set_title("Trend")
            sd.trend.plot(ax=axes[1])

            axes[2].set_title("Seasonal")
            sd.seasonal.plot(ax=axes[2])

            axes[3].set_title("Residuals")
            sd.resid.plot(ax=axes[3])
            axes[3].set_xlabel("Date")

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=f"{self.key}_{col}", figure=fig, metadata={}))

        return self.cache_results(results, figures=figures)


@dataclass
class ADFTest(Metric):
    """
    Augmented Dickey-Fuller unit root test for establishing the order of integration of
    time series
    """

    type = "evaluation"  # assume this value
    scope = "test"  # assume this value (could be "train")
    key = "adf"

    def run(self):
        """
        Calculates ADF metric for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        adf_values = {}
        for col in x_train.columns:
            adf, pvalue, usedlag, nobs, critical_values, icbest = adfuller(
                x_train[col].values
            )
            adf_values[col] = {
                "stat": adf,
                "pvalue": pvalue,
                "usedlag": usedlag,
                "nobs": nobs,
                "critical_values": critical_values,
                "icbest": icbest,
            }

        return self.cache_results(adf_values)


@dataclass
class KolmogorovSmirnov(Metric):
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
            ks_stat, p_value = kstest_normal(x_train[col].values, "norm")
            ks_values[col] = {"stat": ks_stat, "pvalue": p_value}

        return self.cache_results(ks_values)


class ShapiroWilk(Metric):
    """
    The Shapiro-Wilk test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"
    scope = "test"
    key = "shapiro_wilk"

    def run(self):
        """
        Calculates Shapiro-Wilk test for each of the dataset features.
        """
        x_train = self.train_ds.raw_dataset

        sw_values = {}
        for col in x_train.columns:
            sw_stat, sw_pvalue = stats.shapiro(x_train[col].values)

            sw_values[col] = {
                "stat": sw_stat,
                "pvalue": sw_pvalue,
            }

        return self.cache_results(sw_values)


@dataclass
class Lilliefors(Metric):
    """
    The Lilliefors test is a statistical test used to determine
    whether a given set of data follows a normal distribution.
    """

    type = "evaluation"
    scope = "test"
    key = "lilliefors_test"

    def run(self):
        """
        Calculates Lilliefors test for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        lilliefors_values = {}
        for col in x_train.columns:
            l_stat, p_value = lilliefors(x_train[col].values)
            lilliefors_values[col] = {
                "stat": l_stat,
                "pvalue": p_value,
            }

        return self.cache_results(lilliefors_values)


class JarqueBera(Metric):
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
            jb_stat, jb_pvalue, jb_skew, jb_kurtosis = jarque_bera(x_train[col].values)

            jb_values[col] = {
                "stat": jb_stat,
                "pvalue": jb_pvalue,
                "skew": jb_skew,
                "kurtosis": jb_kurtosis,
            }

        return self.cache_results(jb_values)


class LJungBox(Metric):
    """
    The Ljung-Box test is a statistical test used to determine
    whether a given set of data has autocorrelations
    that are different from zero.
    """

    type = "evaluation"
    scope = "test"
    key = "ljung_box"

    def run(self):
        """
        Calculates Ljung-Box test for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        ljung_box_values = {}
        for col in x_train.columns:
            lb_results = acorr_ljungbox(x_train[col].values, return_df=True)

            ljung_box_values[col] = {
                "stat": lb_results["lb_stat"].values[0],
                "pvalue": lb_results["lb_pvalue"].values[0],
            }

        return self.cache_results(ljung_box_values)


class BoxPierce(Metric):
    """
    The Box-Pierce test is a statistical test used to determine
    whether a given set of data has autocorrelations
    that are different from zero.
    """

    type = "evaluation"
    scope = "test"
    key = "box_pierce"

    def run(self):
        """
        Calculates Box-Pierce test for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        box_pierce_values = {}
        for col in x_train.columns:
            bp_results = acorr_ljungbox(
                x_train[col].values, boxpierce=True, return_df=True
            )
            box_pierce_values[col] = {
                "stat": bp_results.iloc[0]["lb_stat"],
                "pvalue": bp_results.iloc[0]["lb_pvalue"],
            }

        return self.cache_results(box_pierce_values)


class RunsTest(Metric):
    """
    The runs test is a statistical test used to determine whether a given set
    of data has runs of positive and negative values that are longer than expected
    under the null hypothesis of randomness.
    """

    type = "evaluation"
    scope = "test"
    key = "runs_test"

    def run(self):
        """
        Calculates the run test for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        runs_test_values = {}
        for col in x_train.columns:
            runs_stat, runs_p_value = runstest_1samp(x_train[col].values)

            runs_test_values[col] = {
                "stat": runs_stat,
                "pvalue": runs_p_value,
            }

        return self.cache_results(runs_test_values)


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

    def run(self):
        """
        Calculates Zivot-Andrews metric for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        za_values = {}
        for col in x_train.columns:
            za = ZivotAndrews(x_train[col].values)
            za_values[col] = {
                "stat": za.stat,
                "pvalue": za.pvalue,
                "usedlag": za.lags,
                "nobs": za.nobs,
            }

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

    def run(self):
        """
        Calculates Dickey-Fuller GLS metric for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        dfgls_values = {}
        for col in x_train.columns:
            dfgls_out = DFGLS(x_train[col].values)
            dfgls_values[col] = {
                "stat": dfgls_out.stat,
                "pvalue": dfgls_out.pvalue,
                "usedlag": dfgls_out.lags,
                "nobs": dfgls_out.nobs,
            }

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

    def run(self):
        """
        Calculates KPSS for each of the dataset features
        """
        x_train = self.train_ds.raw_dataset

        kpss_values = {}
        for col in x_train.columns:
            kpss_stat, pvalue, usedlag, critical_values = kpss(x_train[col].values)
            kpss_values[col] = {
                "stat": kpss_stat,
                "pvalue": pvalue,
                "usedlag": usedlag,
                "critical_values": critical_values,
            }

        return self.cache_results(kpss_values)
