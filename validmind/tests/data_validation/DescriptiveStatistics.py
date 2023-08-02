# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.utils import format_records
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


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
