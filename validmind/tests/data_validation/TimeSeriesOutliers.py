# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class TimeSeriesOutliers(ThresholdTest):
    """
    Identifies and visualizes outliers in time-series data using the z-score method.

    ### Purpose

    This test is designed to identify outliers in time-series data using the z-score method. It's vital for ensuring
    data quality before modeling, as outliers can skew predictive models and significantly impact their overall
    performance.

    ### Test Mechanism

    The test processes a given dataset which must have datetime indexing, checks if a 'zscore_threshold' parameter has
    been supplied, and identifies columns with numeric data types. After finding numeric columns, the implementer then
    applies the z-score method to each numeric column, identifying outliers based on the threshold provided. Each
    outlier is listed together with their variable name, z-score, timestamp, and relative threshold in a dictionary and
    converted to a DataFrame for convenient output. Additionally, it produces visual plots for each time series
    illustrating outliers in the context of the broader dataset. The 'zscore_threshold' parameter sets the limit beyond
    which a data point will be labeled as an outlier. The default threshold is set at 3, indicating that any data point
    that falls 3 standard deviations away from the mean will be marked as an outlier.

    ### Signs of High Risk

    - Many or substantial outliers are present within the dataset, indicating significant anomalies.
    - Data points with z-scores higher than the set threshold.
    - Potential impact on the performance of machine learning models if outliers are not properly addressed.

    ### Strengths

    - The z-score method is a popular and robust method for identifying outliers in a dataset.
    - Simplifies time series maintenance by requiring a datetime index.
    - Identifies outliers for each numeric feature individually.
    - Provides an elaborate report showing variables, dates, z-scores, and pass/fail tests.
    - Offers visual inspection for detected outliers through plots.

    ### Limitations

    - The test only identifies outliers in numeric columns, not in categorical variables.
    - The utility and accuracy of z-scores can be limited if the data doesn't follow a normal distribution.
    - The method relies on a subjective z-score threshold for deciding what constitutes an outlier, which might not
    always be suitable depending on the dataset and use case.
    - It does not address possible ways to handle identified outliers in the data.
    - The requirement for a datetime index could limit its application.
    """

    name = "time_series_outliers"
    required_inputs = ["dataset"]
    default_params = {"zscore_threshold": 3}
    tasks = ["regression"]
    tags = ["time_series_data"]

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
            "Pass" if abs(z) < self.params["zscore_threshold"] else "Fail"
            for z in zScores
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
        # Initialize the test_results list
        test_results = []

        # Check if the index of dataframe is datetime
        is_datetime = pd.api.types.is_datetime64_any_dtype(self.inputs.dataset.df.index)
        if not is_datetime:
            raise ValueError("Dataset must be provided with datetime index")

        # Validate threshold parameter
        if "zscore_threshold" not in self.params:
            raise ValueError("zscore_threshold must be provided in params")
        zscore_threshold = self.params["zscore_threshold"]

        temp_df = self.inputs.dataset.df.copy()
        # temp_df = temp_df.dropna()

        # Infer numeric columns
        num_features_columns = temp_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        outliers_table = self.identify_outliers(
            temp_df[num_features_columns], zscore_threshold
        )

        test_figures = self._plot_outliers(temp_df, outliers_table)
        passed = outliers_table.empty

        if not outliers_table.empty:
            outliers_table["Date"] = outliers_table["Date"].astype(str)

        test_results.append(
            ThresholdTestResult(
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
            list: A list of Figure objects with subplots for each variable.
        """
        figures = []

        for col in df.columns:
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df.index, y=df[col], mode="lines", name=col))

            if not outliers_table.empty:
                variable_outliers = outliers_table[outliers_table["Variable"] == col]
                fig.add_trace(
                    go.Scatter(
                        x=variable_outliers["Date"],
                        y=df.loc[variable_outliers["Date"], col],
                        mode="markers",
                        marker=dict(color="red", size=10),
                        name="Outlier",
                    )
                )

            fig.update_layout(
                title=f"Outliers for {col}",
                xaxis_title="Date",
                yaxis_title=col,
            )

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:{col}_{self.inputs.dataset.input_id}",
                    figure=fig,
                )
            )

        return figures
