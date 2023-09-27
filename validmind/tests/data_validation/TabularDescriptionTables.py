# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class TabularDescriptionTables(Metric):
    """
    **Purpose**: The primarily purpose of this metric is to gather and present descriptive statistics for numerical,
    categorical and datetime variables from a given dataset. This helps in understanding the core traits of the dataset
    like the count, mean, min, max, percentage of missing values, data types of fields, unique values in case of
    categorical fields, amongst other descriptors.

    **Test Mechanism**: The methodology for this metric involves first segregating the variables in the dataset into
    their data types - numerical, categorical or datetime. Once they are segregated, the metric gathers the summary
    statistics for each variable type. The capture of these summary statistics varies depending upon the type of
    variable. For numerical variables, it extracts descriptors like count, mean, min, max, count of missing values and
    data type. For categorical variables, it extracts descriptors like count, number of unique values, display of
    unique values, count of missing values, and data type. For datetime variables, it extracts descriptors like count,
    number of unique values, earliest and latest date, count of missing values and data type.

    **Signs of High Risk**: There could be signs of high risk or failure when a substantial number of missing values is
    observed in the descriptive statistics results. It signals potential issues regarding data collection, integrity,
    and quality. Other red signals could include seeing inappropriate distributions for numerical variables (like
    having negative values for a variable that should always be positive), or finding inappropriate data types (like a
    continuous variable encoded as a categorical type).

    **Strengths**: This metric provides a comprehensive overview of the dataset. It not only gives a snapshot into the
    essence of the numerical, categorical, and datetime fields respectively but also identifies potential data quality
    issues such as missing values or inconsistencies which are crucial for building credible machine learning models.
    The metadata, notably the data type and missing value information, are vital for anyone including data scientists
    dealing with the dataset before the modeling process.

    **Limitations**: However, the limitations of this metric include not performing any deeper statistical analysis or
    tests on the data. It doesn't handle issues such as outliers, or relationships between variables. It does not offer
    insights into potential correlations or possible interactions between variables. It also stays silent on the
    potential impact of missing values on the performance of the machine learning models. Furthermore, it doesn’t
    investigate potential transformation requirements that may be necessary to enhance the performance of the chosen
    algorithm.
    """

    name = "tabular_description_tables"
    required_inputs = ["dataset"]

    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data"],
    }

    def get_summary_statistics_numerical(self, numerical_fields):
        summary_stats = self.dataset.df[numerical_fields].describe().T
        summary_stats["Missing Values (%)"] = (
            self.dataset.df[numerical_fields].isnull().mean() * 100
        )
        summary_stats["Data Type"] = self.dataset.df[numerical_fields].dtypes.astype(
            str
        )
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
            for column in self.dataset.df[categorical_fields].columns:
                summary_stats.loc[column, "Num of Obs"] = int(
                    self.dataset.df[column].count()
                )
                summary_stats.loc[column, "Num of Unique Values"] = self.dataset.df[
                    column
                ].nunique()
                summary_stats.loc[column, "Unique Values"] = str(
                    self.dataset.df[column].unique()
                )
                summary_stats.loc[column, "Missing Values (%)"] = (
                    self.dataset.df[column].isnull().mean() * 100
                )
                summary_stats.loc[column, "Data Type"] = str(
                    self.dataset.df[column].dtype
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
        for column in self.dataset.df[datetime_fields].columns:
            summary_stats.loc[column, "Num of Obs"] = int(
                self.dataset.df[column].count()
            )
            summary_stats.loc[column, "Num of Unique Values"] = self.dataset.df[
                column
            ].nunique()
            summary_stats.loc[column, "Earliest Date"] = self.dataset.df[column].min()
            summary_stats.loc[column, "Latest Date"] = self.dataset.df[column].max()
            summary_stats.loc[column, "Missing Values (%)"] = (
                self.dataset.df[column].isnull().mean() * 100
            )
            summary_stats.loc[column, "Data Type"] = str(self.dataset.df[column].dtype)

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
        categorical_columns = self.dataset.df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()
        return categorical_columns

    def get_numerical_columns(self):
        numerical_columns = self.dataset.df.select_dtypes(
            include=["int", "float", "uint8"]
        ).columns.tolist()
        return numerical_columns

    def get_datetime_columns(self):
        datetime_columns = self.dataset.df.select_dtypes(
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
