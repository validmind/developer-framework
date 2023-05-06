"""
Metrics functions for any Pandas-compatible datasets
"""

from dataclasses import dataclass
from typing import ClassVar

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose


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

        plt.figure(figsize=(12, 3))
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


class SeasonalDecomposeOLD(Metric):
    """
    Calculates seasonal_decompose metric for each of the dataset features
    """

    type = "dataset"
    key = "seasonal_decompose"

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
            .reset_index()
            .assign(Date=lambda x: x["Date"].dt.strftime("%Y-%m-%d"))
            for series in results.values()
        ]

        # Merge DataFrames on the 'Date' column
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = merged_df.merge(df, on="Date")

        # Convert the merged DataFrame into a list of dictionaries
        return merged_df.to_dict("records")

    def run(self):
        df = self.dataset.df

        results = {}
        figures = []

        for col in df.columns:
            sd = seasonal_decompose(df[col], model="additive")
            self.store_seasonal_decompose(col, sd)

            results[col] = self.serialize_seasonal_decompose(sd)

            # Create subplots
            fig, axes = plt.subplots(nrows=2, ncols=2)
            fig.subplots_adjust(hspace=1)
            fig.suptitle(f"Seasonal Decomposition for {col}", fontsize=24)

            axes[0, 0].set_title("Observed")
            sd.observed.plot(ax=axes[0, 0])

            axes[0, 1].set_title("Trend")
            sd.trend.plot(ax=axes[0, 1])

            axes[1, 0].set_title("Seasonal")
            sd.seasonal.plot(ax=axes[1, 0])

            axes[1, 1].set_title("Residuals")
            sd.resid.plot(ax=axes[1, 1])
            axes[1, 1].set_xlabel("Date")

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(Figure(key=f"{self.key}:{col}", figure=fig, metadata={}))

        return self.cache_results(results, figures=figures)
