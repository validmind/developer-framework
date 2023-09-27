# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.utils import format_records
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class DescriptiveStatistics(Metric):
    """
    **Purpose**: The purpose of the Descriptive Statistics metric is to provide a comprehensive summary of both
    numerical and categorical data within a dataset. For numerical data, it gathers statistics such as count, mean,
    standard deviation, minimum and maximum values, as well as certain percentiles. For categorical data, it calculates
    the count, number of unique values, most frequent value, frequency of the most common value, and the proportion of
    the most frequent value relative to the total. This metric aids in visualizing the overall distribution of the
    variables in the dataset, which in turn assists in understanding the model's behavior and predicting its
    performance.

    **Test Mechanism**: The test mechanism involves using the describe() function for numerical fields which computes
    several summary statistics and value_counts() for categorical fields which counts unique values. Both of these
    functions are built-in methods of pandas dataframes. The results are then formatted to create two separate tables,
    one for numerical and one for categorical variable summaries. These tables provide a clear summary of the main
    characteristics of these variables, which can be crucial in assessing the model's performance.

    **Signs of High Risk**: High risks can be found in evidence of skewed data or notable outliers. This could be
    reflected in the mean and median (50% percentile) having a significant difference, in the case of numerical data.
    For categorical data, high risk can be indicated by a lack of diversity (low count of unique values), or
    overdominance of a single category (high frequency of the top value).

    **Strengths**: The primary strength of this metric lies in its ability to provide a comprehensive summary of the
    dataset, providing insights on the distribution and characteristics of the variables under consideration. It is a
    flexible and robust method, relevant to both numerical and categorical data. It can help highlight anomalies such
    as outliers, extreme skewness, or lack of diversity which can be essential in understanding model behavior during
    testing and validation.

    **Limitations**: While this metric provides a high-level overview of the data, it may not be sufficient to detect
    subtle correlations or complex patterns in the data. It does not provide any info on the relationship between
    variables. Plus, descriptive statistics alone cannot be used to infer properties about future unseen data. It
    should be used in conjunction with other statistical tests to provide a thorough understanding of the model's data.
    """

    name = "descriptive_statistics"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "time_series_data"],
    }

    def get_summary_statistics_numerical(self, numerical_fields):
        percentiles = [0.25, 0.5, 0.75, 0.90, 0.95]
        summary_stats = (
            self.dataset.df[numerical_fields].describe(percentiles=percentiles).T
        )
        summary_stats = summary_stats[
            ["count", "mean", "std", "min", "25%", "50%", "75%", "90%", "95%", "max"]
        ]
        summary_stats.columns = summary_stats.columns.str.title()
        summary_stats.reset_index(inplace=True)
        summary_stats.rename(columns={"index": "Name"}, inplace=True)

        return format_records(summary_stats)

    def get_summary_statistics_categorical(self, categorical_fields):
        summary_stats = pd.DataFrame()
        for column in self.dataset.df[categorical_fields].columns:
            top_value = self.dataset.df[column].value_counts().idxmax()
            top_freq = self.dataset.df[column].value_counts().max()
            summary_stats.loc[column, "Count"] = self.dataset.df[column].count()
            summary_stats.loc[column, "Number of Unique Values"] = self.dataset.df[
                column
            ].nunique()
            summary_stats.loc[column, "Top Value"] = top_value
            summary_stats.loc[column, "Top Value Frequency"] = top_freq
            summary_stats.loc[column, "Top Value Frequency %"] = (
                top_freq / self.dataset.df[column].count()
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
