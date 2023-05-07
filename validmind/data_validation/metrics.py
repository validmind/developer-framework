"""
Metrics functions for any Pandas-compatible datasets
"""

from dataclasses import dataclass
from typing import ClassVar

import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import coint


from ..vm_models import (
    Figure,
    Metric,
    TestContext,
    TestContextUtils,
    TestPlanDatasetResult,
)


@dataclass
class DatasetMetadata(TestContextUtils):
    """
    Custom class to collect a set of descriptive statistics for a dataset.
    This class will log dataset metadata via `log_dataset` instead of a metric.
    Dataset metadat is necessary to initialize dataset object that can be related
    to different metrics and test results
    """

    # Test Context
    test_context: TestContext

    # Class Variables
    test_type: ClassVar[str] = "DatasetMetadata"
    default_params: ClassVar[dict] = {}

    # Instance Variables
    name = "dataset_metadata"
    params: dict = None
    result: TestPlanDatasetResult = None

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.params is None:
            self.params = self.default_params

    def run(self):
        """
        Just set the dataset to the result attribute of the test plan result
        and it will be logged via the `log_dataset` function
        """
        self.result = TestPlanDatasetResult(
            result_id="dataset_metadata", dataset=self.dataset
        )

        return self.result


@dataclass
class DatasetCorrelations(Metric):
    """
    Extracts the correlation matrix for a dataset. The following coefficients
    are calculated:
    - Pearson's R for numerical variables
    - Cramer's V for categorical variables
    - Correlation ratios for categorical-numerical variables
    """

    type = "dataset"
    key = "dataset_correlations"

    def __post_init__(self):
        self.scope = self.dataset.type

    def run(self):
        # This will populate the "correlations" attribute in the dataset object
        self.dataset.get_correlations()
        correlation_plots = self.dataset.get_correlation_plots()
        return self.cache_results(self.dataset.correlations, figures=correlation_plots)


@dataclass
class DatasetDescription(Metric):
    """
    Collects a set of descriptive statistics for a dataset
    """

    type = "dataset"
    key = "dataset_description"

    def __post_init__(self):
        self.scope = self.dataset.type

    def run(self):
        # This will populate the "fields" attribute in the dataset object
        self.dataset.describe()
        return self.cache_results(self.dataset.fields)


class TimeSeriesLinePlot(Metric):
    """
    Generates a visual analysis of time series data by plotting the
    raw time series. The input dataset can have multiple time series
    if necessary. In this case we produce a separate plot for each time series.
    """

    type = "dataset"
    key = "time_series_line_plot"

    def run(self):
        if "columns" not in self.params:
            raise ValueError("Time series columns must be provided in params")

        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = self.params["columns"]
        df = self.dataset.df

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []
        for col in columns:
            plt.figure(figsize=(10, 6))
            fig, _ = plt.subplots()
            column_index_name = df.index.name
            ax = sns.lineplot(data=df.reset_index(), x=column_index_name, y=col)
            plt.title(f"Time Series: {col}")
            plt.xlabel(column_index_name)
            plt.ylabel(col)

            # Rotate x-axis labels and set the number of x-axis ticks
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

            figures.append(Figure(key=f"{self.key}:{col}", figure=fig, metadata={}))

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )


class TimeSeriesHistogram(Metric):
    """
    Generates a visual analysis of time series data by plotting the
    histogram. The input dataset can have multiple time series if
    necessary. In this case we produce a separate plot for each time series.
    """

    type = "dataset"
    key = "time_series_histogram"

    def run(self):
        if "columns" not in self.params:
            raise ValueError("Time series columns must be provided in params")

        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = self.params["columns"]
        df = self.dataset.df

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []
        for col in columns:
            plt.figure(figsize=(10, 6))
            fig, _ = plt.subplots()
            sns.histplot(data=df, x=col, kde=True)
            plt.title(f"Histogram: {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")

            figures.append(Figure(key=f"{self.key}:{col}", figure=fig, metadata={}))

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )


class ScatterPlot(Metric):
    """
    Generates a visual analysis of data by plotting a scatter plot matrix for all columns
    in the dataset. The input dataset can have multiple columns (features) if necessary.
    """

    type = "dataset"
    key = "scatter_plot"

    def run(self):
        if "columns" not in self.params:
            raise ValueError("Columns must be provided in params")

        columns = self.params["columns"]
        df = self.dataset.df[columns]

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        sns.pairplot(data=df, diag_kind="kde")

        plt.title("Scatter Plot Matrix")
        plt.tight_layout()

        # Get the current figure
        fig = plt.gcf()

        figures = []
        figures.append(Figure(key=self.key, figure=fig, metadata={}))

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )


class LaggedCorrelationHeatmap(Metric):
    """
    Generates a heatmap of correlations between the target variable and the lags of independent variables in the dataset.
    """

    type = "dataset"
    key = "lagged_correlation_heatmap"

    def _compute_correlations(self, df, target_col, independent_vars, num_lags):
        correlations = np.zeros((len(independent_vars), num_lags + 1))

        for i, ind_var_col in enumerate(independent_vars):
            for lag in range(num_lags + 1):
                temp_df = pd.DataFrame(
                    {
                        target_col: df[target_col],
                        f"{ind_var_col}_lag{lag}": df[ind_var_col].shift(lag),
                    }
                )

                temp_df = temp_df.dropna()

                corr = temp_df[target_col].corr(temp_df[f"{ind_var_col}_lag{lag}"])

                correlations[i, lag] = corr

        return correlations

    def _plot_heatmap(self, correlations, independent_vars, num_lags):
        correlation_df = pd.DataFrame(
            correlations,
            columns=[f"lag_{i}" for i in range(num_lags + 1)],
            index=independent_vars,
        )

        plt.figure()
        sns.heatmap(correlation_df, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title(
            "Heatmap of Correlations between Target Variable and Lags of Independent Variables"
        )
        plt.xlabel("Lags")
        plt.ylabel("Independent Variables")

        return plt.gcf()

    def run(self):
        if "target_col" not in self.params or "independent_vars" not in self.params:
            raise ValueError(
                "Both 'target_col' and 'independent_vars' must be provided in params"
            )

        target_col = self.params["target_col"]
        if isinstance(target_col, list) and len(target_col) == 1:
            target_col = target_col[0]

        if not isinstance(target_col, str):
            raise ValueError(
                "The 'target_col' must be a single string or a list containing a single string"
            )

        independent_vars = self.params["independent_vars"]
        num_lags = self.params.get("num_lags", 10)

        df = self.dataset.df

        correlations = self._compute_correlations(
            df, target_col, independent_vars, num_lags
        )
        fig = self._plot_heatmap(correlations, independent_vars, num_lags)

        figures = []
        figures.append(Figure(key=self.key, figure=fig, metadata={}))
        plt.close("all")

        return self.cache_results(
            figures=figures,
        )


class AutoAR(Metric):
    """
    Automatically detects the AR order of a time series using both BIC and AIC.
    """

    type = "dataset"  # assume this value
    key = "auto_ar"

    def run(self):
        if "max_ar_order" not in self.params:
            raise ValueError("max_ar_order must be provided in params")

        max_ar_order = self.params["max_ar_order"]

        df = self.dataset.df

        results = []

        for col in df.columns:
            series = df[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                print(f"Warning: {col} is not stationary. Results may be inaccurate.")

            ar_orders = []
            bic_values = []
            aic_values = []

            for ar_order in range(0, max_ar_order + 1):
                try:
                    model = AutoReg(series, lags=ar_order, old_names=False)
                    model_fit = model.fit()

                    ar_orders.append(ar_order)
                    bic_values.append(model_fit.bic)
                    aic_values.append(model_fit.aic)
                except Exception as e:
                    print(f"Error fitting AR({ar_order}) model for {col}: {e}")

            result = {
                "Variable": col,
                "AR orders": ar_orders,
                "BIC": bic_values,
                "AIC": aic_values,
            }
            results.append(result)

        return self.cache_results(results)


class AutoMA(Metric):
    """
    Automatically detects the MA order of a time series using both BIC and AIC.
    """

    type = "dataset"
    key = "auto_ma"

    def run(self):
        if "max_ma_order" not in self.params:
            raise ValueError("max_ma_order must be provided in params")

        max_ma_order = self.params["max_ma_order"]

        df = self.dataset.df

        results = []

        for col in df.columns:
            series = df[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                print(f"Warning: {col} is not stationary. Results may be inaccurate.")

            ma_orders = []
            bic_values = []
            aic_values = []

            for ma_order in range(0, max_ma_order + 1):
                try:
                    model = ARIMA(series, order=(0, 0, ma_order))
                    model_fit = model.fit()

                    ma_orders.append(ma_order)
                    bic_values.append(model_fit.bic)
                    aic_values.append(model_fit.aic)
                except Exception as e:
                    print(f"Error fitting MA({ma_order}) model for {col}: {e}")

            result = {
                "Variable": col,
                "MA orders": ma_orders,
                "BIC": bic_values,
                "AIC": aic_values,
            }
            results.append(result)

        return self.cache_results(results)


class SeasonalDecompose(Metric):
    """
    Calculates seasonal_decompose metric for each of the dataset features
    """

    type = "dataset"
    key = "seasonal_decompose"
    default_params = {"seasonal_model": "additive"}

    def store_seasonal_decompose(self, column, sd_one_column):
        """
        Stores the seasonal decomposition results in the test context so they
        can be re-used by other tests. Note we store one `sd` at a time for every
        column in the dataset.
        """
        sd_all_columns = (
            self.test_context.get_context_data("seasonal_decompose") or dict()
        )
        sd_all_columns[column] = sd_one_column
        self.test_context.set_context_data("seasonal_decompose", sd_all_columns)

    def serialize_seasonal_decompose(self, sd):
        """
        Serializes the seasonal decomposition results for one column into a
        JSON serializable format that can be sent to the API.
        """
        results = {
            "observed": sd.observed,
            "trend": sd.trend,
            "seasonal": sd.seasonal,
            "resid": sd.resid,
        }

        # Convert pandas Series to DataFrames, reset their indices, and format the dates as strings
        dfs = [
            pd.DataFrame(series)
            .pipe(
                lambda x: x.reset_index()
                if not isinstance(x.index, pd.DatetimeIndex)
                else x.reset_index().rename(columns={x.index.name: "Date"})
            )
            .assign(
                Date=lambda x: x["Date"].dt.strftime("%Y-%m-%d")
                if "Date" in x.columns
                else x.index.strftime("%Y-%m-%d")
            )
            for series in results.values()
        ]

        # Merge DataFrames on the 'Date' column
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = merged_df.merge(df, on="Date")

        # Convert the merged DataFrame into a list of dictionaries
        return merged_df.to_dict("records")

    def run(self):
        # Parse input parameters
        if "seasonal_model" not in self.params:
            raise ValueError("seasonal_model must be provided in params")
        seasonal_model = self.params["seasonal_model"]

        df = self.dataset.df

        # Drop rows with missing values
        df = df.dropna()

        results = {}
        figures = []

        for col in df.columns:
            sd = seasonal_decompose(df[col], model=seasonal_model)
            self.store_seasonal_decompose(col, sd)

            results[col] = self.serialize_seasonal_decompose(sd)

            # Create subplots
            fig, axes = plt.subplots(nrows=4, ncols=2)
            fig.subplots_adjust(hspace=1)
            fig.suptitle(
                f"Seasonal Decomposition and Residual Diagnostics for {col}",
                fontsize=24,
            )

            # Original seasonal decomposition plots
            axes[0, 0].set_title("Observed")
            sd.observed.plot(ax=axes[0, 0])

            axes[0, 1].set_title("Trend")
            sd.trend.plot(ax=axes[0, 1])

            axes[1, 0].set_title("Seasonal")
            sd.seasonal.plot(ax=axes[1, 0])

            axes[1, 1].set_title("Residuals")
            sd.resid.plot(ax=axes[1, 1])
            axes[1, 1].set_xlabel("Date")

            # Residual diagnostics plots
            residuals = sd.resid.dropna()

            # Histogram with KDE
            sns.histplot(residuals, kde=True, ax=axes[2, 0])
            axes[2, 0].set_title("Histogram and KDE of Residuals")

            # Normal Q-Q plot
            stats.probplot(residuals, plot=axes[2, 1])
            axes[2, 1].set_title("Normal Q-Q Plot of Residuals")

            # ACF plot
            plot_acf(residuals, ax=axes[3, 0], title="ACF of Residuals")

            # PACF plot
            plot_pacf(residuals, ax=axes[3, 1], title="PACF of Residuals")

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=f"{self.key}:{col}", figure=fig, metadata={}))

        return self.cache_results(results, figures=figures)


class AutoSeasonality(Metric):
    """
    Automatically detects the optimal seasonal order for a time series dataset
    using the seasonal_decompose method.
    """

    type = "dataset"
    key = "auto_seasonality"
    default_params = {"min_period": 1, "max_period": 4}

    def evaluate_seasonal_periods(self, series, min_period, max_period):
        seasonal_periods = []
        residual_errors = []

        for period in range(min_period, max_period + 1):
            try:
                sd = seasonal_decompose(series, model="additive", period=period)
                residual_error = np.abs(sd.resid.dropna()).mean()

                seasonal_periods.append(period)
                residual_errors.append(residual_error)
            except Exception as e:
                print(f"Error evaluating period {period} for series: {e}")

        return seasonal_periods, residual_errors

    def run(self):
        # Parse input parameters
        if "min_period" not in self.params:
            raise ValueError("min_period must be provided in params")
        min_period = self.params["min_period"]

        if "max_period" not in self.params:
            raise ValueError("max_period must be provided in params")
        max_period = self.params["max_period"]

        df = self.dataset.df

        results = []

        for col_name, col in df.iteritems():
            series = col.dropna()
            seasonal_periods, residual_errors = self.evaluate_seasonal_periods(
                series, min_period, max_period
            )

            best_seasonal_period = seasonal_periods[np.argmin(residual_errors)]
            decision = "Seasonality" if best_seasonal_period > 1 else "Not Seasonality"

            result = {
                "Variable": col_name,
                "Seasonal Periods": seasonal_periods,
                "Residual Errors": residual_errors,
                "Best Period": best_seasonal_period,
                "Decision": decision,
            }
            results.append(result)

        return self.cache_results(results)


class ACFandPACFPlot(Metric):
    """
    Plots ACF and PACF for a given time series dataset.
    """

    type = "evaluation"
    key = "acf_pacf_plot"

    def run(self):
        if "columns" not in self.params:
            raise ValueError("Time series columns must be provided in params")

        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = self.params["columns"]
        df = self.dataset.df.dropna()

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []

        for col in df.columns:
            series = df[col]

            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2)

            plot_acf(series, ax=ax1)
            plot_pacf(series, ax=ax2)

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=f"{self.key}:{col}", figure=fig, metadata={}))

        return self.cache_results(figures=figures)


class AutoStationarity(Metric):
    """
    Automatically detects stationarity for each time series in a DataFrame
    using the Augmented Dickey-Fuller (ADF) test.
    """

    type = "dataset"
    key = "auto_stationarity"
    default_params = {"max_order": 5, "threshold": 0.05}

    def run(self):
        if "max_order" not in self.params:
            raise ValueError("max_order must be provided in params")
        max_order = self.params["max_order"]

        if "threshold" not in self.params:
            raise ValueError("threshold must be provided in params")
        threshold = self.params["threshold"]

        df = self.dataset.df.dropna()
        results = []

        # Loop over each column in the input DataFrame and perform stationarity tests
        for col in df.columns:
            is_stationary = False
            order = 0

            while not is_stationary and order <= max_order:
                series = df[col]

                if order == 0:
                    adf_result = adfuller(series)
                else:
                    adf_result = adfuller(np.diff(series, n=order - 1))

                adf_pvalue = adf_result[1]
                adf_pass_fail = adf_pvalue < threshold
                adf_decision = "Stationary" if adf_pass_fail else "Non-stationary"

                result = {
                    "Variable": col,
                    "Integration Order": order,
                    "Test": "ADF",
                    "p-value": adf_pvalue,
                    "Threshold": threshold,
                    "Pass/Fail": "Pass" if adf_pass_fail else "Fail",
                    "Decision": adf_decision,
                }
                results.append(result)

                if adf_pass_fail:
                    is_stationary = True

                order += 1

        return self.cache_results(results)


class RollingStatsPlot(Metric):
    """
    This class provides a metric to visualize the stationarity of a given time series dataset by plotting the rolling mean and rolling standard deviation. The rolling mean represents the average of the time series data over a fixed-size sliding window, which helps in identifying trends in the data. The rolling standard deviation measures the variability of the data within the sliding window, showing any changes in volatility over time. By analyzing these plots, users can gain insights into the stationarity of the time series data and determine if any transformations or differencing operations are required before applying time series models.
    """

    type = "dataset"
    key = "rolling_stats_plot"
    default_params = {"window_size": 12}

    @staticmethod
    def plot_rolling_statistics(series, window_size=12, ax1=None, ax2=None):
        """
        Plot rolling mean and rolling standard deviation in different subplots for a given series.

        :param series: Pandas Series with time-series data
        :param window_size: Window size for the rolling calculations
        :param ax1: Axis object for the rolling mean plot
        :param ax2: Axis object for the rolling standard deviation plot
        """
        rolling_mean = series.rolling(window=window_size).mean()
        rolling_std = series.rolling(window=window_size).std()

        if ax1 is None or ax2 is None:
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(rolling_mean, label="Rolling Mean")
        ax1.legend()
        ax1.set_ylabel("Value")

        ax2.plot(rolling_std, label="Rolling Standard Deviation", color="orange")
        ax2.legend()
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Value")

    def run(self):
        if "window_size" not in self.params:
            raise ValueError("Window size must be provided in params")

        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        window_size = self.params["window_size"]
        df = self.dataset.df.dropna()

        if not set(df.columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []

        for col in df.columns:
            series = df[col]

            # Create a new figure and axis objects
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
            fig.suptitle(col)

            # Call the plot_rolling_statistics function
            self.plot_rolling_statistics(
                series, window_size=window_size, ax1=ax1, ax2=ax2
            )

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=f"{self.key}:{col}", figure=fig, metadata={}))

        return self.cache_results(figures=figures)


class EngleGrangerCoint(Metric):
    """
    Test for cointegration between pairs of time series variables in a given dataset using the Engle-Granger test.
    """

    type = "dataset"
    key = "engle_granger_coint"
    default_params = {"threshold": 0.05}

    def run(self):
        threshold = self.params["threshold"]
        df = self.dataset.df.dropna()

        results = []
        columns = df.columns
        num_vars = len(columns)

        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                var1 = columns[i]
                var2 = columns[j]

                # Perform the Engle-Granger cointegration test
                _, p_value, _ = coint(df[var1], df[var2])

                # Determine the decision based on the p-value and the significance level
                decision = (
                    "Cointegrated" if p_value <= threshold else "Not cointegrated"
                )
                pass_fail = "Pass" if p_value <= threshold else "Fail"

                result = {
                    "Variable 1": var1,
                    "Variable 2": var2,
                    "Test": "Engle-Granger",
                    "p-value": p_value,
                    "Threshold": threshold,
                    "Pass/Fail": pass_fail,
                    "Decision": decision,
                }
                results.append(result)

        return self.cache_results(results)


class SpreadPlot(Metric):
    """
    This class provides a metric to visualize the spread between pairs of time series variables in a given dataset. By plotting the spread of each pair of variables in separate figures, users can assess the relationship between the variables and determine if any cointegration or other time series relationships exist between them.
    """

    type = "dataset"
    key = "spread_plot"

    @staticmethod
    def plot_spread(series1, series2, ax=None):
        """
        Plot the spread between two time series variables.

        :param series1: Pandas Series with time-series data for the first variable
        :param series2: Pandas Series with time-series data for the second variable
        :param ax: Axis object for the spread plot
        """
        spread = series1 - series2

        if ax is None:
            _, ax = plt.subplots()

        sns.lineplot(data=spread, ax=ax)

        return ax

    def run(self):
        df = self.dataset.df.dropna()

        figures = []
        columns = df.columns
        num_vars = len(columns)

        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                var1 = columns[i]
                var2 = columns[j]

                series1 = df[var1]
                series2 = df[var2]

                fig, ax = plt.subplots()
                fig.suptitle(f"Spread between {var1} and {var2}")

                self.plot_spread(series1, series2, ax=ax)

                # Adjust the layout
                plt.tight_layout()

                # Do this if you want to prevent the figure from being displayed
                plt.close("all")

                figures.append(
                    Figure(key=f"{self.key}:{var1}_{var2}", figure=fig, metadata={})
                )

        return self.cache_results(figures=figures)
