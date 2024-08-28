# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class TimeSeriesMissingValues(ThresholdTest):
    """
    Validates time-series data quality by confirming the count of missing values is below a certain threshold.

    ### Purpose

    This test is designed to validate the quality of a historical time-series dataset by verifying that the number of
    missing values is below a specified threshold. As time-series models greatly depend on the continuity and
    temporality of data points, missing values could compromise the model's performance. Consequently, this test aims
    to ensure data quality and readiness for the machine learning model, safeguarding its predictive capacity.

    ### Test Mechanism

    The test method commences by validating if the dataset has a datetime index; if not, an error is raised. It
    establishes a lower limit threshold for missing values and performs a missing values check on each column of the
    dataset. An object for the test result is created stating whether the number of missing values is within the
    specified threshold. Additionally, the test calculates the percentage of missing values alongside the raw count.

    To aid in data visualization, the test generates two plots - a bar plot and a heatmap - to better illustrate the
    distribution and quantity of missing values per variable. The test results, including a count of missing values,
    the percentage of missing values, and a pass/fail status, are returned in a results table.

    ### Signs of High Risk

    - The number of missing values in any column of the dataset surpasses the threshold, marking a failure and a
    high-risk scenario. The reasons could range from incomplete data collection, faulty sensors to data preprocessing
    errors.
    - A continuous visual 'streak' in the heatmap may indicate a systematic error during data collection, pointing
    towards another potential risk source.

    ### Strengths

    - Effectively identifies missing values which could adversely affect the model’s performance.
    - Applicable and customizable through the threshold parameter across different data sets.
    - Goes beyond raw numbers by calculating the percentage of missing values, offering a more relative understanding
    of data scarcity.
    - Includes a robust visualization mechanism for easy and fast understanding of data quality.

    ### Limitations

    - Although it identifies missing values, the test does not provide solutions to handle them.
    - The test demands that the dataset should have a datetime index, hence limiting its use only to time series
    analysis.
    - The test's sensitivity to the 'min_threshold' parameter may raise false alarms if set too strictly or may
    overlook problematic data if set too loosely.
    - Solely focuses on the 'missingness' of the data and might fall short in addressing other aspects of data quality.
    """

    name = "time_series_missing_values"
    required_inputs = ["dataset"]
    default_params = {"min_threshold": 1}
    tasks = ["regression"]
    tags = ["time_series_data"]

    def summary(self, results, all_passed):
        results_table = [
            {
                "Column": result.column,
                "Number of Missing Values": result.values["n_missing"],
                "Percentage of Missing Values (%)": result.values["p_missing"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="Missing Values Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        df = self.inputs.dataset.df

        # Check if the index of dataframe is datetime
        is_datetime = pd.api.types.is_datetime64_any_dtype(df.index)
        if not is_datetime:
            raise ValueError("Dataset must be provided with datetime index")

        # Validate threshold parameter
        if "min_threshold" not in self.params:
            raise ValueError("min_threshold must be provided in params")
        min_threshold = self.params["min_threshold"]

        rows = df.shape[0]
        missing = df.isna().sum()
        test_results = [
            ThresholdTestResult(
                column=col,
                passed=missing[col] < min_threshold,
                values={"n_missing": missing[col], "p_missing": missing[col] / rows},
            )
            for col in missing.index
        ]

        fig_barplot = self._barplot(df)
        fig_heatmap = self._heatmap(df)
        test_figures = []
        if fig_barplot is not None:
            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:barplot",
                    figure=fig_barplot,
                    metadata={"type": "barplot"},
                )
            )
            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:heatmap",
                    figure=fig_heatmap,
                    metadata={"type": "heatmap"},
                )
            )

        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            # Don't pass figures until we figure out how to group metric-figures for multiple
            # executions inside a single test run
            # figures=test_figures,
        )

    def _barplot(self, df):
        """
        Generate a bar plot of missing values using Plotly.
        """
        missing_values = df.isnull().sum()
        if sum(missing_values.values) != 0:
            fig = px.bar(
                missing_values,
                x=missing_values.index,
                y=missing_values.values,
                labels={"x": "", "y": "Missing Values"},
                title="Total Number of Missing Values per Variable",
                color=missing_values.values,
                color_continuous_scale="Reds",
            )
        else:
            fig = None

        return fig

    def _heatmap(self, df):
        """
        Plots a heatmap to visualize missing values using Plotly.
        """
        # Create a boolean mask for missing values
        missing_mask = df.isnull()
        z = missing_mask.T.astype(int).values  # Convert boolean to int for heatmap

        x = missing_mask.index.tolist()
        y = missing_mask.columns.tolist()

        if not x:
            fig = ff.create_annotated_heatmap(
                z=z, x=x, y=y, colorscale="Reds", showscale=False
            )
            fig.update_layout(title="Missing Values Heatmap")
        else:
            fig = None

        return fig
