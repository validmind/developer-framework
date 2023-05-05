"""
Metrics functions for any Pandas-compatible datasets
"""

from dataclasses import dataclass
from typing import ClassVar

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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


class TimeSeriesUnivariateInspectionRaw(Metric):
    """
    Generates a visual analysis of time series data by plotting the
    raw time series. The input dataset can have multiple time series
    if necessary. In this case we produce a separate plot for each time series.
    """

    type = "dataset"
    key = "time_series_univariate_inspection_raw"

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
            ax = sns.lineplot(data=df, x="Date", y=col)
            plt.title(f"Time Series: {col}")
            plt.xlabel("Date")
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


class TimeSeriesUnivariateInspectionHistogram(Metric):
    """
    Generates a visual analysis of time series data by plotting the
    histogram. The input dataset can have multiple time series if
    necessary. In this case we produce a separate plot for each time series.
    """

    type = "dataset"
    key = "time_series_univariate_inspection_histogram"

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
        print(df)

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        pair_grid = sns.pairplot(data=df, diag_kind="kde")
        print(pair_grid)

        plt.title("Scatter Plot Matrix")
        plt.tight_layout()

        # Get the current figure
        fig = plt.gcf()
        print(fig)

        figures = []
        figures.append(Figure(key=self.key, figure=fig, metadata={}))
        print(figures)
        plt.close("all")

        return self.cache_results(
            figures=figures,
        )
