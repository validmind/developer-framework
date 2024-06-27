# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class TabularDescriptionTables(Metric):
    """
    Summarizes key descriptive statistics for numerical, categorical, and datetime variables in a dataset.

    **Purpose**: The main purpose of this metric is to gather and present the descriptive statistics of numerical,
    categorical, and datetime variables present in a dataset. The attributes it measures include the count, mean,
    minimum and maximum values, percentage of missing values, data types of fields, and unique values for categorical
    fields, among others.

    **Test Mechanism**: The test first segregates the variables in the dataset according to their data types
    (numerical, categorical, or datetime). Then, it compiles summary statistics for each type of variable. The
    specifics of these statistics vary depending on the type of variable:

    - For numerical variables, the metric extracts descriptors like count, mean, minimum and maximum values, count of
    missing values, and data types.
    - For categorical variables, it counts the number of unique values, displays unique values, counts missing values,
    and identifies data types.
    - For datetime variables, it counts the number of unique values, identifies the earliest and latest dates, counts
    missing values, and identifies data types.

    **Signs of High Risk**:
    - Masses of missing values in the descriptive statistics results could hint at high risk or failure, indicating
    potential data collection, integrity, and quality issues.
    - Detection of inappropriate distributions for numerical variables, like having negative values for variables that
    are always supposed to be positive.
    - Identifying inappropriate data types, like a continuous variable being encoded as a categorical type.

    **Strengths**:
    - Provides a comprehensive overview of the dataset.
    - Gives a snapshot into the essence of the numerical, categorical, and datetime fields.
    - Identifies potential data quality issues such as missing values or inconsistencies crucial for building credible
    machine learning models.
    - The metadata, including the data type and missing value information, are vital for anyone including data
    scientists dealing with the dataset before the modeling process.

    **Limitations**:
    - It does not perform any deeper statistical analysis or tests on the data.
    - It does not handle issues such as outliers, or relationships between variables.
    - It offers no insights into potential correlations or possible interactions between variables.
    - It does not investigate the potential impact of missing values on the performance of the machine learning models.
    - It does not explore potential transformation requirements that may be necessary to enhance the performance of the
    chosen algorithm.
    """

    name = "tabular_description_tables"
    required_inputs = ["dataset"]

    tasks = ["classification", "regression"]
    tags = ["tabular_data"]

    def get_summary_statistics_numerical(self, numerical_fields):
        summary_stats = self.inputs.dataset.df[numerical_fields].describe().T
        summary_stats["Missing Values (%)"] = (
            self.inputs.dataset.df[numerical_fields].isnull().mean() * 100
        )
        summary_stats["Data Type"] = self.inputs.dataset.df[
            numerical_fields
        ].dtypes.astype(str)
        summary_stats = summary_stats[
            ["count", "mean", "min", "max", "Missing Values (%)", "Data Type"]
        ]
        summary_stats.columns = [
            "Num of Obs",
            "Mean",
            "Min",
            "Max",
            "Missing Values (%)",
            "Data Type",
        ]
        summary_stats["Num of Obs"] = summary_stats["Num of Obs"].astype(int)
        summary_stats = summary_stats.sort_values(
            by="Missing Values (%)", ascending=False
        )
        summary_stats.reset_index(inplace=True)
        summary_stats.rename(columns={"index": "Numerical Variable"}, inplace=True)
        return summary_stats

    def get_summary_statistics_categorical(self, categorical_fields):
        summary_stats = pd.DataFrame()
        if categorical_fields:  # check if the list is not empty
            for column in self.inputs.dataset.df[categorical_fields].columns:
                summary_stats.loc[column, "Num of Obs"] = int(
                    self.inputs.dataset.df[column].count()
                )
                summary_stats.loc[
                    column, "Num of Unique Values"
                ] = self.inputs.dataset.df[column].nunique()
                summary_stats.loc[column, "Unique Values"] = str(
                    self.inputs.dataset.df[column].unique()
                )
                summary_stats.loc[column, "Missing Values (%)"] = (
                    self.inputs.dataset.df[column].isnull().mean() * 100
                )
                summary_stats.loc[column, "Data Type"] = str(
                    self.inputs.dataset.df[column].dtype
                )

            summary_stats = summary_stats.sort_values(
                by="Missing Values (%)", ascending=False
            )
            summary_stats.reset_index(inplace=True)
            summary_stats.rename(
                columns={"index": "Categorical Variable"}, inplace=True
            )
        return summary_stats

    def get_summary_statistics_datetime(self, datetime_fields):
        summary_stats = pd.DataFrame()
        for column in self.inputs.dataset.df[datetime_fields].columns:
            summary_stats.loc[column, "Num of Obs"] = int(
                self.inputs.dataset.df[column].count()
            )
            summary_stats.loc[column, "Num of Unique Values"] = self.inputs.dataset.df[
                column
            ].nunique()
            summary_stats.loc[column, "Earliest Date"] = self.inputs.dataset.df[
                column
            ].min()
            summary_stats.loc[column, "Latest Date"] = self.inputs.dataset.df[
                column
            ].max()
            summary_stats.loc[column, "Missing Values (%)"] = (
                self.inputs.dataset.df[column].isnull().mean() * 100
            )
            summary_stats.loc[column, "Data Type"] = str(
                self.inputs.dataset.df[column].dtype
            )

        if not summary_stats.empty:
            summary_stats = summary_stats.sort_values(
                by="Missing Values (%)", ascending=False
            )
        summary_stats.reset_index(inplace=True)
        summary_stats.rename(columns={"index": "Datetime Variable"}, inplace=True)
        return summary_stats

    def summary(self, metric_value):
        summary_stats_numerical = metric_value["numerical"]
        summary_stats_categorical = metric_value["categorical"]
        summary_stats_datetime = metric_value["datetime"]

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
                ResultTable(
                    data=summary_stats_datetime,
                    metadata=ResultTableMetadata(title="Datetime Variables"),
                ),
            ]
        )

    def get_categorical_columns(self):
        categorical_columns = self.inputs.dataset.df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        return categorical_columns

    def get_numerical_columns(self):
        numerical_columns = self.inputs.dataset.df.select_dtypes(
            include=["int", "float", "uint8"]
        ).columns.tolist()
        return numerical_columns

    def get_datetime_columns(self):
        datetime_columns = self.inputs.dataset.df.select_dtypes(
            include=["datetime"]
        ).columns.tolist()
        return datetime_columns

    def run(self):
        numerical_fields = self.get_numerical_columns()
        categorical_fields = self.get_categorical_columns()
        datetime_fields = self.get_datetime_columns()

        summary_stats_numerical = self.get_summary_statistics_numerical(
            numerical_fields
        )
        summary_stats_categorical = self.get_summary_statistics_categorical(
            categorical_fields
        )
        summary_stats_datetime = self.get_summary_statistics_datetime(datetime_fields)

        return self.cache_results(
            {
                "numerical": summary_stats_numerical.to_dict(orient="records"),
                "categorical": summary_stats_categorical.to_dict(orient="records"),
                "datetime": summary_stats_datetime.to_dict(orient="records"),
            }
        )
