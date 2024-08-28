# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd

from validmind.utils import format_records
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class DescriptiveStatistics(Metric):
    """
    Performs a detailed descriptive statistical analysis of both numerical and categorical data within a model's
    dataset.

    ### Purpose

    The purpose of the Descriptive Statistics metric is to provide a comprehensive summary of both numerical and
    categorical data within a dataset. This involves statistics such as count, mean, standard deviation, minimum and
    maximum values for numerical data. For categorical data, it calculates the count, number of unique values, most
    common value and its frequency, and the proportion of the most frequent value relative to the total. The goal is to
    visualize the overall distribution of the variables in the dataset, aiding in understanding the model's behavior
    and predicting its performance.

    ### Test Mechanism

    The testing mechanism utilizes two in-built functions of pandas dataframes: `describe()` for numerical fields and
    `value_counts()` for categorical fields. The `describe()` function pulls out several summary statistics, while
    `value_counts()` accounts for unique values. The resulting data is formatted into two distinct tables, one for
    numerical and another for categorical variable summaries. These tables provide a clear summary of the main
    characteristics of the variables, which can be instrumental in assessing the model's performance.

    ### Signs of High Risk

    - Skewed data or significant outliers can represent high risk. For numerical data, this may be reflected via a
    significant difference between the mean and median (50% percentile).
    - For categorical data, a lack of diversity (low count of unique values), or overdominance of a single category
    (high frequency of the top value) can indicate high risk.

    ### Strengths

    - Provides a comprehensive summary of the dataset, shedding light on the distribution and characteristics of the
    variables under consideration.
    - It is a versatile and robust method, applicable to both numerical and categorical data.
    - Helps highlight crucial anomalies such as outliers, extreme skewness, or lack of diversity, which are vital in
    understanding model behavior during testing and validation.

    ### Limitations

    - While this metric offers a high-level overview of the data, it may fail to detect subtle correlations or complex
    patterns.
    - Does not offer any insights on the relationship between variables.
    - Alone, descriptive statistics cannot be used to infer properties about future unseen data.
    - Should be used in conjunction with other statistical tests to provide a comprehensive understanding of the
    model's data.
    """

    name = "descriptive_statistics"
    required_inputs = ["dataset"]
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "time_series_data"]

    def get_summary_statistics_numerical(self, df, numerical_fields):
        percentiles = [0.25, 0.5, 0.75, 0.90, 0.95]

        summary_stats = df[numerical_fields].describe(percentiles=percentiles).T
        summary_stats = summary_stats[
            ["count", "mean", "std", "min", "25%", "50%", "75%", "90%", "95%", "max"]
        ]
        summary_stats.columns = summary_stats.columns.str.title()
        summary_stats.reset_index(inplace=True)
        summary_stats.rename(columns={"index": "Name"}, inplace=True)

        return format_records(summary_stats)

    def get_summary_statistics_categorical(self, df, categorical_fields):
        summary_stats = pd.DataFrame()

        for column in df[categorical_fields].columns:
            top_value = df[column].value_counts().idxmax()
            top_freq = df[column].value_counts().max()
            summary_stats.loc[column, "Count"] = df[column].count()
            summary_stats.loc[column, "Number of Unique Values"] = df[column].nunique()
            summary_stats.loc[column, "Top Value"] = top_value
            summary_stats.loc[column, "Top Value Frequency"] = top_freq
            summary_stats.loc[column, "Top Value Frequency %"] = (
                top_freq / df[column].count()
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
        results = []
        if len(summary_stats_numerical) != 0:
            results.append(
                ResultTable(
                    data=summary_stats_numerical,
                    metadata=ResultTableMetadata(title="Numerical Variables"),
                )
            )
        if len(summary_stats_categorical) != 0:
            results.append(
                ResultTable(
                    data=summary_stats_categorical,
                    metadata=ResultTableMetadata(title="Categorical Variables"),
                )
            )

        return ResultSummary(results=results)

    def run(self):
        feature_columns = self.inputs.dataset.feature_columns
        numerical_feature_columns = self.inputs.dataset.feature_columns_numeric
        categorical_feature_columns = self.inputs.dataset.feature_columns_categorical

        df = self.inputs.dataset.df[feature_columns]

        summary_stats_numerical = self.get_summary_statistics_numerical(
            df, numerical_feature_columns
        )
        summary_stats_categorical = self.get_summary_statistics_categorical(
            df, categorical_feature_columns
        )
        return self.cache_results(
            {
                "numerical": summary_stats_numerical,
                "categorical": summary_stats_categorical,
            }
        )
