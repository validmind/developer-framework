"""
Metrics functions for any Pandas-compatible datasets
"""

from dataclasses import dataclass
from typing import ClassVar
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns

from scipy import stats
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import coint


from ..utils import format_records
from ..vm_models import (
    Figure,
    Metric,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestContext,
    TestContextUtils,
)
from ..vm_models.test_plan_result import TestPlanDatasetResult


@dataclass
class DatasetMetadata(TestContextUtils):
    """
    Custom class to collect a set of descriptive statistics for a dataset.
    This class will log dataset metadata via `log_dataset` instead of a metric.
    Dataset metadata is necessary to initialize dataset object that can be related
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
class PearsonCorrelationMatrix(Metric):
    """
    Extracts the Pearson correlation coefficient for all pairs of numerical variables
    in the dataset. This metric is useful to identify highly correlated variables
    that can be removed from the dataset to reduce dimensionality.
    """

    name = "pearson_correlation_matrix"
    required_context = ["dataset"]

    def run(self):
        columns = self.params.get("columns", list(self.df.columns))

        corr_matrix = self.df[columns].corr(numeric_only=True)
        heatmap = go.Heatmap(
            z=corr_matrix.values,
            x=list(corr_matrix.columns),
            y=list(corr_matrix.index),
            colorscale="rdbu",
            zmin=-1,
            zmax=1,
        )

        annotations = []
        for i, row in enumerate(corr_matrix.values):
            for j, value in enumerate(row):
                color = "#ffffff" if abs(value) > 0.7 else "#000000"
                annotations.append(
                    go.layout.Annotation(
                        text=str(round(value, 2)),
                        x=corr_matrix.columns[j],
                        y=corr_matrix.index[i],
                        showarrow=False,
                        font=dict(color=color),
                    )
                )

        layout = go.Layout(
            annotations=annotations,
            xaxis=dict(side="top"),
            yaxis=dict(scaleanchor="x", scaleratio=1),
            width=800,
            height=800,
            autosize=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        fig = go.Figure(data=[heatmap], layout=layout)

        return self.cache_results(
            figures=[
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                )
            ]
        )


@dataclass
class DatasetCorrelations(Metric):
    """
    Extracts the correlation matrix for a dataset. The following coefficients
    are calculated:

    - Pearson's R for numerical variables
    - Cramer's V for categorical variables
    - Correlation ratios for categorical-numerical variables
    """

    name = "dataset_correlations"
    required_context = ["dataset"]

    # TODO: allow more metric metadata to be set, not just scope
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

    name = "dataset_description"
    required_context = ["dataset"]

    def __post_init__(self):
        self.scope = self.dataset.type

    def run(self):
        # This will populate the "fields" attribute in the dataset object
        self.dataset.describe()
        return self.cache_results(self.dataset.fields)


@dataclass
class DescriptiveStatistics(Metric):
    """
    Collects a set of descriptive statistics for a dataset, both for
    numerical and categorical variables
    """

    name = "descriptive_statistics"
    required_context = ["dataset"]

    def description(self):
        return """
        This section provides descriptive statistics for numerical
        and categorical variables found in the dataset.
        """

    def get_summary_statistics_numerical(self, numerical_fields):
        percentiles = [0.25, 0.5, 0.75, 0.90, 0.95]
        summary_stats = self.df[numerical_fields].describe(percentiles=percentiles).T
        summary_stats = summary_stats[
            ["count", "mean", "std", "min", "25%", "50%", "75%", "90%", "95%", "max"]
        ]
        summary_stats.columns = summary_stats.columns.str.title()
        summary_stats.reset_index(inplace=True)
        summary_stats.rename(columns={"index": "Name"}, inplace=True)

        return format_records(summary_stats)

    def get_summary_statistics_categorical(self, categorical_fields):
        summary_stats = pd.DataFrame()
        for column in self.df[categorical_fields].columns:
            top_value = self.df[column].value_counts().idxmax()
            top_freq = self.df[column].value_counts().max()
            summary_stats.loc[column, "Count"] = self.df[column].count()
            summary_stats.loc[column, "Number of Unique Values"] = self.df[
                column
            ].nunique()
            summary_stats.loc[column, "Top Value"] = top_value
            summary_stats.loc[column, "Top Value Frequency"] = top_freq
            summary_stats.loc[column, "Top Value Frequency %"] = (
                top_freq / self.df[column].count()
            ) * 100

        summary_stats.reset_index(inplace=True)
        summary_stats.rename(columns={"index": "Name"}, inplace=True)

        return format_records(summary_stats)

    def summary(self, metric_value):
        """
        Build two tables: one for summarizing numerical variables and one for categorical variables
        """
        summary_stats_numerical = metric_value["numerical"]
        summary_stats_categorical = metric_value["categorical"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_stats_numerical,
                    metadata=ResultTableMetadata(title="Numerical Variables"),
                ),
                ResultTable(
                    data=summary_stats_categorical,
                    metadata=ResultTableMetadata(title="Categorical Variables"),
                ),
            ]
        )

    def run(self):
        numerical_fields = self.dataset.get_numeric_features_columns()
        categorical_fields = self.dataset.get_categorical_features_columns()

        summary_stats_numerical = self.get_summary_statistics_numerical(
            numerical_fields
        )
        summary_stats_categorical = self.get_summary_statistics_categorical(
            categorical_fields
        )
        return self.cache_results(
            {
                "numerical": summary_stats_numerical,
                "categorical": summary_stats_categorical,
            }
        )


class DatasetSplit(Metric):
    """
    Attempts to extract information about the dataset split from the
    provided training, test and validation datasets.
    """

    name = "dataset_split"
    required_context = ["model"]

    dataset_labels = {
        "train_ds": "Training",
        "test_ds": "Test",
        "validation_ds": "Validation",
        "total": "Total",
    }

    def description(self):
        return """
        This section shows the size of the dataset split into training, test (and validation) sets
        where applicable. The size of each dataset is shown in absolute terms and as a proportion
        of the total dataset size.

        The dataset split is important to understand because it can affect the performance of
        the model. For example, if the training set is too small, the model may not be able to
        learn the patterns in the data and will perform poorly on the test set. On the other hand,
        if the test set is too small, the model may not be able to generalize well to unseen data
        and will perform poorly on the validation set.
        """

    def summary(self, raw_results):
        """
        Returns a summarized representation of the dataset split information
        """
        table_records = []
        for key, value in raw_results.items():
            if key.endswith("_size"):
                dataset_name = key.replace("_size", "")
                if dataset_name == "total":
                    table_records.append(
                        {
                            "Dataset": "Total",
                            "Size": value,
                            "Proportion": "100%",
                        }
                    )
                    continue

                proportion = raw_results[f"{dataset_name}_proportion"] * 100
                table_records.append(
                    {
                        "Dataset": DatasetSplit.dataset_labels[dataset_name],
                        "Size": value,
                        "Proportion": f"{proportion:.2f}%",
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def run(self):
        # Try to extract metrics from each available dataset
        available_datasets = ["train_ds", "test_ds", "validation_ds"]
        results = {}
        total_size = 0

        # First calculate the total size of the dataset
        for dataset_name in available_datasets:
            dataset = getattr(self.model, dataset_name, None)
            if dataset is not None:
                total_size += len(dataset.df)

        # Then calculate the proportion of each dataset
        for dataset_name in available_datasets:
            dataset = getattr(self.model, dataset_name, None)
            if dataset is not None:
                results[f"{dataset_name}_size"] = len(dataset.df)
                results[f"{dataset_name}_proportion"] = len(dataset.df) / total_size

        results["total_size"] = total_size

        return self.cache_results(results)


class TimeSeriesLinePlot(Metric):
    """
    Generates a visual analysis of time series data by plotting the
    raw time series. The input dataset can have multiple time series
    if necessary. In this case we produce a separate plot for each time series.
    """

    name = "time_series_line_plot"
    required_context = ["dataset"]

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.dataset.df.columns)

        df = self.dataset.df

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []
        for col in columns:
            plt.figure()
            fig, _ = plt.subplots()
            column_index_name = df.index.name
            ax = sns.lineplot(data=df.reset_index(), x=column_index_name, y=col)
            plt.title(f"Time Series for {col}", weight="bold", fontsize=20)

            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            ax.set_xlabel("")
            ax.set_ylabel("")
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

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

    name = "time_series_histogram"
    required_context = ["dataset"]

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.dataset.df.columns)

        df = self.dataset.df

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []
        for col in columns:
            plt.figure()
            fig, _ = plt.subplots()
            ax = sns.histplot(data=df, x=col, kde=True)
            plt.title(f"Histogram for {col}", weight="bold", fontsize=20)

            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            ax.set_xlabel("")
            ax.set_ylabel("")
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )


class ScatterPlot(Metric):
    """
    Generates a visual analysis of data by plotting a scatter plot matrix for all columns
    in the dataset. The input dataset can have multiple columns (features) if necessary.
    """

    name = "scatter_plot"
    required_context = ["dataset", "dataset.target_column"]

    def run(self):
        columns = list(self.dataset.df.columns)

        df = self.dataset.df[columns]

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        sns.pairplot(data=df, diag_kind="kde")

        # Get the current figure
        fig = plt.gcf()

        figures = []
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )

        plt.close("all")

        return self.cache_results(
            figures=figures,
        )


class LaggedCorrelationHeatmap(Metric):
    """
    Generates a heatmap of correlations between the target variable and the lags of independent variables in the dataset.
    """

    name = "lagged_correlation_heatmap"
    required_context = ["dataset"]

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

    def _plot_heatmap(self, correlations, independent_vars, target_col, num_lags):
        correlation_df = pd.DataFrame(
            correlations,
            columns=[f"{i}" for i in range(num_lags + 1)],
            index=independent_vars,
        )

        fig, ax = plt.subplots()
        sns.heatmap(
            correlation_df,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            annot_kws={"size": 16},
        )
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=16)  # Here you can set the font size
        fig.suptitle(
            f"Correlations between {target_col} and Lags of Features",
            fontsize=20,
            weight="bold",
            y=0.95,
        )
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.xlabel("Lags", fontsize=18)

        return fig

    def run(self):
        target_col = [self.dataset.target_column]
        independent_vars = list(self.dataset.get_features_columns())
        num_lags = self.params.get("num_lags", 10)

        if isinstance(target_col, list) and len(target_col) == 1:
            target_col = target_col[0]

        if not isinstance(target_col, str):
            raise ValueError(
                "The 'target_col' must be a single string or a list containing a single string"
            )

        df = self.dataset.df

        correlations = self._compute_correlations(
            df, target_col, independent_vars, num_lags
        )
        fig = self._plot_heatmap(correlations, independent_vars, target_col, num_lags)

        figures = []
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )
        plt.close("all")

        return self.cache_results(
            figures=figures,
        )


class AutoAR(Metric):
    """
    Automatically detects the AR order of a time series using both BIC and AIC.
    """

    type = "dataset"
    name = "auto_ar"
    required_context = ["dataset"]
    default_params = {"max_ar_order": 3}

    def run(self):
        if "max_ar_order" not in self.params:
            raise ValueError("max_ar_order must be provided in params")

        max_ar_order = self.params["max_ar_order"]

        df = self.dataset.df

        # Create empty DataFrames to store the results
        summary_ar_analysis = pd.DataFrame()
        best_ar_order = pd.DataFrame()

        for col in df.columns:
            series = df[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                print(f"Warning: {col} is not stationary. Results may be inaccurate.")

            for ar_order in range(0, max_ar_order + 1):
                try:
                    model = AutoReg(series, lags=ar_order, old_names=False)
                    model_fit = model.fit()

                    # Append the result of each AR order directly into the DataFrame
                    summary_ar_analysis = pd.concat(
                        [
                            summary_ar_analysis,
                            pd.DataFrame(
                                [
                                    {
                                        "Variable": col,
                                        "AR Order": ar_order,
                                        "BIC": model_fit.bic,
                                        "AIC": model_fit.aic,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )
                except Exception as e:
                    print(f"Error fitting AR({ar_order}) model for {col}: {e}")

            # Find the best AR Order for this variable based on the minimum BIC
            variable_summary = summary_ar_analysis[
                summary_ar_analysis["Variable"] == col
            ]
            best_bic_row = variable_summary[
                variable_summary["BIC"] == variable_summary["BIC"].min()
            ]
            best_ar_order = pd.concat([best_ar_order, best_bic_row])

        # Convert the 'AR Order' column to integer
        summary_ar_analysis["AR Order"] = summary_ar_analysis["AR Order"].astype(int)
        best_ar_order["AR Order"] = best_ar_order["AR Order"].astype(int)

        return self.cache_results(
            {
                "auto_ar_analysis": summary_ar_analysis.to_dict(orient="records"),
                "best_ar_order": best_ar_order.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the auto AR results
        and another for the best AR Order results
        """
        summary_ar_analysis = metric_value["auto_ar_analysis"]
        best_ar_order = metric_value["best_ar_order"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_ar_analysis,
                    metadata=ResultTableMetadata(title="Auto AR Analysis Results"),
                ),
                ResultTable(
                    data=best_ar_order,
                    metadata=ResultTableMetadata(title="Best AR Order Results"),
                ),
            ]
        )


class AutoMA(Metric):
    """
    Automatically detects the MA order of a time series using both BIC and AIC.
    """

    type = "dataset"
    name = "auto_ma"
    required_context = ["dataset"]
    default_params = {"max_ma_order": 3}

    def run(self):
        if "max_ma_order" not in self.params:
            raise ValueError("max_ma_order must be provided in params")

        max_ma_order = self.params["max_ma_order"]

        df = self.dataset.df

        # Create empty DataFrames to store the results
        summary_ma_analysis = pd.DataFrame()
        best_ma_order = pd.DataFrame()

        for col in df.columns:
            series = df[col].dropna()

            # Check for stationarity using the Augmented Dickey-Fuller test
            adf_test = adfuller(series)
            if adf_test[1] > 0.05:
                print(f"Warning: {col} is not stationary. Results may be inaccurate.")

            for ma_order in range(0, max_ma_order + 1):
                try:
                    model = ARIMA(series, order=(0, 0, ma_order))
                    model_fit = model.fit()

                    # Append the result of each MA order directly into the DataFrame
                    summary_ma_analysis = pd.concat(
                        [
                            summary_ma_analysis,
                            pd.DataFrame(
                                [
                                    {
                                        "Variable": col,
                                        "MA Order": ma_order,
                                        "BIC": model_fit.bic,
                                        "AIC": model_fit.aic,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )
                except Exception as e:
                    print(f"Error fitting MA({ma_order}) model for {col}: {e}")

            # Find the best MA Order for this variable based on the minimum BIC
            variable_summary = summary_ma_analysis[
                summary_ma_analysis["Variable"] == col
            ]
            best_bic_row = variable_summary[
                variable_summary["BIC"] == variable_summary["BIC"].min()
            ]
            best_ma_order = pd.concat([best_ma_order, best_bic_row])

        # Convert the 'MA Order' column to integer
        summary_ma_analysis["MA Order"] = summary_ma_analysis["MA Order"].astype(int)
        best_ma_order["MA Order"] = best_ma_order["MA Order"].astype(int)

        return self.cache_results(
            {
                "auto_ma_analysis": summary_ma_analysis.to_dict(orient="records"),
                "best_ma_order": best_ma_order.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the auto MA results
        and another for the best MA Order results
        """
        summary_ma_analysis = metric_value["auto_ma_analysis"]
        best_ma_order = metric_value["best_ma_order"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_ma_analysis,
                    metadata=ResultTableMetadata(title="Auto MA Analysis Results"),
                ),
                ResultTable(
                    data=best_ma_order,
                    metadata=ResultTableMetadata(title="Best MA Order Results"),
                ),
            ]
        )


class SeasonalDecompose(Metric):
    """
    Calculates seasonal_decompose metric for each of the dataset features
    """

    category = "univariate_analysis"
    name = "seasonal_decompose"
    required_context = ["dataset"]
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

        # Convert pandas Series to DataFrames, reset their indices, and convert the dates to strings
        dfs = [
            pd.DataFrame(series)
            .pipe(
                lambda x: x.reset_index()
                if not isinstance(x.index, pd.DatetimeIndex)
                else x.reset_index().rename(columns={x.index.name: "Date"})
            )
            .assign(
                Date=lambda x: x["Date"].astype(str)
                if "Date" in x.columns
                else x.index.astype(str)
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

        results = {}
        figures = []

        for col in df.columns:
            series = df[col].dropna()

            # Check for non-finite values and handle them
            if not series[np.isfinite(series)].empty:
                inferred_freq = pd.infer_freq(series.index)

                if inferred_freq is not None:
                    print(f"Frequency of {col}: {inferred_freq}")

                    # Only take finite values to seasonal_decompose
                    sd = seasonal_decompose(
                        series[np.isfinite(series)], model=seasonal_model
                    )
                    self.store_seasonal_decompose(col, sd)

                    results[col] = self.serialize_seasonal_decompose(sd)

                    # Create subplots
                    fig, axes = plt.subplots(3, 2)
                    width, _ = fig.get_size_inches()
                    fig.set_size_inches(width, 15)
                    fig.subplots_adjust(hspace=0.3)
                    fig.suptitle(
                        f"Seasonal Decomposition for {col}",
                        fontsize=20,
                        weight="bold",
                        y=0.95,
                    )

                    # Original seasonal decomposition plots
                    # Observed
                    sd.observed.plot(ax=axes[0, 0])
                    axes[0, 0].set_title("Observed", fontsize=18)
                    axes[0, 0].set_xlabel("")
                    axes[0, 0].tick_params(axis="both", labelsize=18)

                    # Trend
                    sd.trend.plot(ax=axes[0, 1])
                    axes[0, 1].set_title("Trend", fontsize=18)
                    axes[0, 1].set_xlabel("")
                    axes[0, 1].tick_params(axis="both", labelsize=18)

                    # Seasonal
                    sd.seasonal.plot(ax=axes[1, 0])
                    axes[1, 0].set_title("Seasonal", fontsize=18)
                    axes[1, 0].set_xlabel("")
                    axes[1, 0].tick_params(axis="both", labelsize=18)

                    # Residuals
                    sd.resid.plot(ax=axes[1, 1])
                    axes[1, 1].set_title("Residuals", fontsize=18)
                    axes[1, 1].set_xlabel("")
                    axes[1, 1].tick_params(axis="both", labelsize=18)

                    # Histogram with KDE
                    residuals = sd.resid.dropna()
                    sns.histplot(residuals, kde=True, ax=axes[2, 0])
                    axes[2, 0].set_title("Histogram and KDE of Residuals", fontsize=18)
                    axes[2, 0].set_xlabel("")
                    axes[2, 0].tick_params(axis="both", labelsize=18)

                    # Normal Q-Q plot
                    stats.probplot(residuals, plot=axes[2, 1])
                    axes[2, 1].set_title("Normal Q-Q Plot of Residuals", fontsize=18)
                    axes[2, 1].set_xlabel("")
                    axes[2, 1].tick_params(axis="both", labelsize=18)

                    # Do this if you want to prevent the figure from being displayed
                    plt.close("all")

                    figures.append(
                        Figure(
                            for_object=self,
                            key=f"{self.key}:{col}",
                            figure=fig,
                        )
                    )
                else:
                    warnings.warn(
                        f"No frequency could be inferred for variable '{col}'. Skipping seasonal decomposition and plots for this variable."
                    )

        return self.cache_results(results, figures=figures)


class AutoSeasonality(Metric):
    """
    Automatically detects the optimal seasonal order for a time series dataset
    using the seasonal_decompose method.
    """

    name = "auto_seasonality"
    required_context = ["dataset"]
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

        # Create an empty DataFrame to store the results
        summary_auto_seasonality = pd.DataFrame()

        for col_name, col in df.items():
            series = col.dropna()

            # Evaluate seasonal periods
            seasonal_periods, residual_errors = self.evaluate_seasonal_periods(
                series, min_period, max_period
            )

            for i, period in enumerate(seasonal_periods):
                decision = "Seasonality" if period > 1 else "No Seasonality"
                summary_auto_seasonality = pd.concat(
                    [
                        summary_auto_seasonality,
                        pd.DataFrame(
                            [
                                {
                                    "Variable": col_name,
                                    "Seasonal Period": period,
                                    "Residual Error": residual_errors[i],
                                    "Decision": decision,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

        # Convert the 'Seasonal Period' column to integer
        summary_auto_seasonality["Seasonal Period"] = summary_auto_seasonality[
            "Seasonal Period"
        ].astype(int)

        # Create a DataFrame to store the best seasonality period for each variable
        best_seasonality_period = pd.DataFrame()

        for variable in summary_auto_seasonality["Variable"].unique():
            temp_df = summary_auto_seasonality[
                summary_auto_seasonality["Variable"] == variable
            ]
            best_row = temp_df[
                temp_df["Residual Error"] == temp_df["Residual Error"].min()
            ]
            best_seasonality_period = pd.concat([best_seasonality_period, best_row])

        # Rename the 'Seasonal Period' column to 'Best Period'
        best_seasonality_period = best_seasonality_period.rename(
            columns={"Seasonal Period": "Best Period"}
        )

        # Convert the 'Best Period' column to integer
        best_seasonality_period["Best Period"] = best_seasonality_period[
            "Best Period"
        ].astype(int)

        return self.cache_results(
            {
                "auto_seasonality": summary_auto_seasonality.to_dict(orient="records"),
                "best_seasonality_period": best_seasonality_period.to_dict(
                    orient="records"
                ),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the auto seasonality results
        and another for the best seasonality period results
        """
        summary_auto_seasonality = metric_value["auto_seasonality"]
        best_seasonality_period = metric_value["best_seasonality_period"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_auto_seasonality,
                    metadata=ResultTableMetadata(title="Auto Seasonality Results"),
                ),
                ResultTable(
                    data=best_seasonality_period,
                    metadata=ResultTableMetadata(
                        title="Best Seasonality Period Results"
                    ),
                ),
            ]
        )


class ACFandPACFPlot(Metric):
    """
    Plots ACF and PACF for a given time series dataset.
    """

    name = "acf_pacf_plot"
    required_context = ["dataset"]

    def run(self):
        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.dataset.df.index):
            raise ValueError("Index must be a datetime type")

        columns = list(self.dataset.df.columns)

        df = self.dataset.df.dropna()

        if not set(columns).issubset(set(df.columns)):
            raise ValueError("Provided 'columns' must exist in the dataset")

        figures = []

        for col in df.columns:
            series = df[col]

            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2)
            width, _ = fig.get_size_inches()
            fig.set_size_inches(width, 5)

            plot_acf(series, ax=ax1)
            plot_pacf(series, ax=ax2)

            # Get the current y-axis limits
            ymin, ymax = ax1.get_ylim()
            # Set new limits - adding a bit of space
            ax1.set_ylim([ymin, ymax + 0.05 * (ymax - ymin)])

            ymin, ymax = ax2.get_ylim()
            ax2.set_ylim([ymin, ymax + 0.05 * (ymax - ymin)])

            ax1.tick_params(axis="both", labelsize=18)
            ax2.tick_params(axis="both", labelsize=18)
            ax1.set_title(f"ACF for {col}", weight="bold", fontsize=20)
            ax2.set_title(f"PACF for {col}", weight="bold", fontsize=20)
            ax1.set_xlabel("Lag", fontsize=18)
            ax2.set_xlabel("Lag", fontsize=18)
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

        return self.cache_results(figures=figures)


class AutoStationarity(Metric):
    """
    Automatically detects stationarity for each time series in a DataFrame
    using the Augmented Dickey-Fuller (ADF) test.
    """

    type = "dataset"
    name = "auto_stationarity"
    required_context = ["dataset"]
    default_params = {"max_order": 5, "threshold": 0.05}

    def run(self):
        if "max_order" not in self.params:
            raise ValueError("max_order must be provided in params")
        max_order = self.params["max_order"]

        if "threshold" not in self.params:
            raise ValueError("threshold must be provided in params")
        threshold = self.params["threshold"]

        df = self.dataset.df.dropna()

        # Create an empty DataFrame to store the results
        summary_stationarity = pd.DataFrame()
        best_integration_order = pd.DataFrame()  # New DataFrame

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

                # Append the result of each test directly into the DataFrame
                summary_stationarity = pd.concat(
                    [
                        summary_stationarity,
                        pd.DataFrame(
                            [
                                {
                                    "Variable": col,
                                    "Integration Order": order,
                                    "Test": "ADF",
                                    "p-value": adf_pvalue,
                                    "Threshold": threshold,
                                    "Pass/Fail": "Pass" if adf_pass_fail else "Fail",
                                    "Decision": adf_decision,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

                if adf_pass_fail:
                    is_stationary = True
                    best_integration_order = pd.concat(
                        [
                            best_integration_order,
                            pd.DataFrame(
                                [
                                    {
                                        "Variable": col,
                                        "Best Integration Order": order,
                                        "Test": "ADF",
                                        "p-value": adf_pvalue,
                                        "Threshold": threshold,
                                        "Decision": adf_decision,
                                    }
                                ]
                            ),
                        ],
                        ignore_index=True,
                    )

                order += 1

        # Convert the 'Integration Order' and 'Best Integration Order' column to integer
        summary_stationarity["Integration Order"] = summary_stationarity[
            "Integration Order"
        ].astype(int)
        best_integration_order["Best Integration Order"] = best_integration_order[
            "Best Integration Order"
        ].astype(int)

        return self.cache_results(
            {
                "stationarity_analysis": summary_stationarity.to_dict(orient="records"),
                "best_integration_order": best_integration_order.to_dict(
                    orient="records"
                ),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the stationarity results
        and another for the best integration order results
        """
        summary_stationarity = metric_value["stationarity_analysis"]
        best_integration_order = metric_value["best_integration_order"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_stationarity,
                    metadata=ResultTableMetadata(title="Stationarity Analysis Results"),
                ),
                ResultTable(
                    data=best_integration_order,
                    metadata=ResultTableMetadata(
                        title="Best Integration Order Results"
                    ),
                ),
            ]
        )


class RollingStatsPlot(Metric):
    """
    This class provides a metric to visualize the stationarity of a given time series dataset by plotting the rolling mean and rolling standard deviation. The rolling mean represents the average of the time series data over a fixed-size sliding window, which helps in identifying trends in the data. The rolling standard deviation measures the variability of the data within the sliding window, showing any changes in volatility over time. By analyzing these plots, users can gain insights into the stationarity of the time series data and determine if any transformations or differencing operations are required before applying time series models.
    """

    name = "rolling_stats_plot"
    required_context = ["dataset"]
    default_params = {"window_size": 12}

    def plot_rolling_statistics(self, col, window_size=12):
        """
        Plot rolling mean and rolling standard deviation in different subplots for a given series.

        :param series: Pandas Series with time-series data
        :param window_size: Window size for the rolling calculations
        :param ax1: Axis object for the rolling mean plot
        :param ax2: Axis object for the rolling standard deviation plot
        """
        rolling_mean = self.df[col].rolling(window=window_size).mean()
        rolling_std = self.df[col].rolling(window=window_size).std()

        # Create a new figure and axis objects
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.plot(rolling_mean)

        ax1.set_title(
            f"Rolling Mean for {col}",
            fontsize=20,
            weight="bold",
        )
        ax1.set_ylabel("")
        ax1.tick_params(axis="both", labelsize=18)
        ax1.legend()

        ax2.plot(rolling_std, label="Rolling Standard Deviation", color="orange")
        ax2.set_title(
            f"Rolling STD for {col}",
            fontsize=20,
            weight="bold",
        )
        ax2.set_xlabel("")
        ax2.set_ylabel("")
        ax2.tick_params(axis="both", labelsize=18)
        ax2.legend()

        return fig

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
            fig = self.plot_rolling_statistics(col, window_size=window_size)

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{col}",
                    figure=fig,
                )
            )

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

        return self.cache_results(figures=figures)


class EngleGrangerCoint(Metric):
    """
    Test for cointegration between pairs of time series variables in a given dataset using the Engle-Granger test.
    """

    type = "dataset"
    name = "engle_granger_coint"
    required_context = ["dataset"]
    default_params = {"threshold": 0.05}

    def run(self):
        threshold = self.params["threshold"]
        df = self.dataset.df.dropna()

        # Create an empty DataFrame to store the results
        summary_cointegration = pd.DataFrame()

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

                # Append the result of each test directly into the DataFrame
                summary_cointegration = pd.concat(
                    [
                        summary_cointegration,
                        pd.DataFrame(
                            [
                                {
                                    "Variable 1": var1,
                                    "Variable 2": var2,
                                    "Test": "Engle-Granger",
                                    "p-value": p_value,
                                    "Threshold": threshold,
                                    "Pass/Fail": pass_fail,
                                    "Decision": decision,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

        return self.cache_results(
            {
                "cointegration_analysis": summary_cointegration.to_dict(
                    orient="records"
                ),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the cointegration results
        """
        summary_cointegration = metric_value["cointegration_analysis"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_cointegration,
                    metadata=ResultTableMetadata(
                        title="Cointegration Analysis Results"
                    ),
                ),
            ]
        )


class SpreadPlot(Metric):
    """
    This class provides a metric to visualize the spread between pairs of time series variables in a given dataset. By plotting the spread of each pair of variables in separate figures, users can assess the relationship between the variables and determine if any cointegration or other time series relationships exist between them.
    """

    name = "spread_plot"
    required_context = ["dataset"]

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
                fig.suptitle(
                    f"Spread between {var1} and {var2}",
                    fontsize=20,
                    weight="bold",
                    y=0.95,
                )

                self.plot_spread(series1, series2, ax=ax)

                ax.set_xlabel("")
                ax.tick_params(axis="both", labelsize=18)

                # Do this if you want to prevent the figure from being displayed
                plt.close("all")

                figures.append(
                    Figure(
                        for_object=self,
                        key=f"{self.key}:{var1}_{var2}",
                        figure=fig,
                    )
                )

        return self.cache_results(figures=figures)
