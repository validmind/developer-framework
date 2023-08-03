# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class TimeSeriesOutliers(ThresholdTest):
    """
    Test that find outliers for time series data using the z-score method
    """

    category = "data_quality"
    name = "time_series_outliers"
    required_context = ["dataset"]
    default_params = {"zscore_threshold": 3}

    def summary(self, results, all_passed: bool):
        """
        Example output:
        [
            {
                "values": {
                    "Variable": [...],
                    "z-score": [...],
                    "Threshold": [3, 3, 3, 3, 3, 3],
                    "Date": [...]
                },
                "test_name": "outliers",
                "passed": false
            }
        ]
        """

        first_result = results[0]

        variables = first_result.values["Variable"]
        zScores = first_result.values["z-score"]
        dates = first_result.values["Date"]
        passFail = [
            "Pass" if z < self.params["zscore_threshold"] else "Fail" for z in zScores
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    # Sort by variable and then by date
                    data=pd.DataFrame(
                        {
                            "Variable": variables,
                            "Date": dates,
                            "z-Score": zScores,
                            "Pass/Fail": passFail,
                        }
                    ).sort_values(["Variable", "Date"]),
                    metadata=ResultTableMetadata(
                        title="Outliers Results with z-Score Test"
                    ),
                )
            ]
        )

    def run(self):
        # Check if the index of dataframe is datetime
        is_datetime = pd.api.types.is_datetime64_any_dtype(self.dataset.df.index)
        if not is_datetime:
            raise ValueError("Dataset must be provided with datetime index")

        # Validate threshold paremeter
        if "zscore_threshold" not in self.params:
            raise ValueError("zscore_threshold must be provided in params")
        zscore_threshold = self.params["zscore_threshold"]

        temp_df = self.dataset.df.copy()
        # temp_df = temp_df.dropna()
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(temp_df)
        test_results = []
        test_figures = []
        num_features_columns = [
            k for k, v in dataset_types.items() if str(v) == "Numeric"
        ]

        outliers_table = self.identify_outliers(
            temp_df[num_features_columns], zscore_threshold
        )

        test_figures = self._plot_outliers(temp_df, outliers_table)
        passed = outliers_table.empty

        if not outliers_table.empty:
            outliers_table["Date"] = outliers_table["Date"].astype(str)

        test_results.append(
            TestResult(
                test_name="outliers",
                passed=passed,
                values=outliers_table.to_dict(orient="list"),
            )
        )

        return self.cache_results(test_results, passed=passed, figures=test_figures)

    def z_score_with_na(self, df):
        return df.apply(
            lambda x: (x - x.mean()) / x.std() if x.dtype.kind in "biufc" else x
        )

    def identify_outliers(self, df, threshold):
        """
        Identifies and returns outliers in a pandas DataFrame using the z-score method.
        Args:
        df (pandas.DataFrame): A pandas DataFrame containing the data to be analyzed.
        threshold (float): The absolute value of the z-score above which a value is considered an outlier.
        Returns:
        pandas.DataFrame: A DataFrame containing the variables, z-scores, threshold, and dates of the identified outliers.
        """
        z_scores = pd.DataFrame(
            self.z_score_with_na(df), index=df.index, columns=df.columns
        )

        outliers = z_scores[(z_scores.abs() > threshold).any(axis=1)]
        outlier_table = []
        for idx, row in outliers.iterrows():
            for col in df.columns:
                if abs(row[col]) > threshold:
                    outlier_table.append(
                        {
                            "Variable": col,
                            "z-score": row[col],
                            "Threshold": threshold,
                            "Date": idx,
                        }
                    )
        return pd.DataFrame(outlier_table)

    def _plot_outliers(self, df, outliers_table):
        """
        Plots time series with identified outliers.
        Args:
            df (pandas.DataFrame): Input data with time series.
            outliers_table (pandas.DataFrame): DataFrame with identified outliers.
        Returns:
            matplotlib.figure.Figure: A matplotlib figure object with subplots for each variable.
        """
        sns.set(style="darkgrid")
        columns = list(self.dataset.df.columns)
        figures = []

        for col in columns:
            plt.figure()
            fig, _ = plt.subplots()
            column_index_name = df.index.name
            ax = sns.lineplot(data=df.reset_index(), x=column_index_name, y=col)

            if not outliers_table.empty:
                variable_outliers = outliers_table[outliers_table["Variable"] == col]
                for idx, row in variable_outliers.iterrows():
                    date = row["Date"]
                    outlier_value = df.loc[date, col]
                    ax.scatter(
                        date,
                        outlier_value,
                        marker="o",
                        s=100,
                        c="red",
                        label="Outlier" if idx == 0 else "",
                    )

            plt.xticks(fontsize=18)
            plt.yticks(fontsize=18)
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.set_title(
                f"Time Series with Outliers for {col}", weight="bold", fontsize=20
            )

            ax.legend()
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:{col}",
                    figure=fig,
                )
            )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")
        return figures
