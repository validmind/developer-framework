"""
Metrics functions models trained with statsmodels or that provide
a statsmodels-like API
"""
from dataclasses import dataclass
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.diagnostic import kstest_normal
from statsmodels.stats.diagnostic import lilliefors
from statsmodels.stats.stattools import jarque_bera
from statsmodels.graphics.tsaplots import plot_acf
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


@dataclass
class SeasonalDecomposeMetricWithFigure(Metric):
    """
    Calculates seasonal_decomponse metric for each of the dataset features
    """

    type = "evaluation"
    key = "seasonal_decomposition_with_figure"

    def run(self):
        x_train = self.train_ds.raw_dataset

        # Each key holds the table of seasonal_decompose values for each column
        sd_values = {}
        for col in x_train.columns:
            sd = seasonal_decompose(x_train[col], model="additive")
            sd_values[col] = sd
            sd_df = pd.DataFrame()
            sd_df["date"] = x_train[col].index.astype(str)
            sd_df["trend"] = sd.trend.values
            sd_df["seasonal"] = sd.seasonal.values
            sd_df["resid"] = sd.resid.values
            sd_df["observed"] = sd.observed.values
            sd_values[col] = sd_df.to_dict(orient="records")

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
