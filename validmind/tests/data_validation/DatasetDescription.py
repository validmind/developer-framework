# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import re
from collections import Counter
from dataclasses import dataclass

import numpy as np
from ydata_profiling.config import Settings
from ydata_profiling.model.typeset import ProfilingTypeSet

from validmind.errors import UnsupportedColumnTypeError
from validmind.logging import get_logger
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

DEFAULT_HISTOGRAM_BINS = 10
DEFAULT_HISTOGRAM_BIN_SIZES = [5, 10, 20, 50]

logger = get_logger(__name__)


@dataclass
class DatasetDescription(Metric):
    """
    Provides comprehensive analysis and statistical summaries of each field in a machine learning model's dataset.

    ### Purpose

    The test depicted in the script is meant to run a comprehensive analysis on a Machine Learning model's datasets.
    The test or metric is implemented to obtain a complete summary of the fields in the dataset, including vital
    statistics of each field such as count, distinct values, missing values, histograms for numerical, categorical,
    boolean, and text fields. This summary gives a comprehensive overview of the dataset to better understand the
    characteristics of the data that the model is trained on or evaluates.

    ### Test Mechanism

    The DatasetDescription class accomplishes the purpose as follows: firstly, the test method "run" infers the data
    type of each column in the dataset and stores the details (id, column type). For each field, the
    "describe_dataset_field" method is invoked to collect statistical information about the field, including count,
    missing value count and its proportion to the total, unique value count, and its proportion to the total. Depending
    on the data type of a field, histograms are generated that reflect the distribution of data within the field.
    Numerical fields use the "get_numerical_histograms" method to calculate histogram distribution, whereas for
    categorical, boolean and text fields, a histogram is computed with frequencies of each unique value in the
    datasets. For unsupported types, an error is raised. Lastly, a summary table is built to aggregate all the
    statistical insights and histograms of the fields in a dataset.

    ### Signs of High Risk

    - High ratio of missing values to total values in one or more fields which may impact the quality of the
    predictions.
    - Unsupported data types in dataset fields.
    - Large number of unique values in the dataset's fields which might make it harder for the model to establish
    patterns.
    - Extreme skewness or irregular distribution of data as reflected in the histograms.

    ### Strengths

    - Provides a detailed analysis of the dataset with versatile summaries like count, unique values, histograms, etc.
    - Flexibility in handling different types of data: numerical, categorical, boolean, and text.
    - Useful in detecting problems in the dataset like missing values, unsupported data types, irregular data
    distribution, etc.
    - The summary gives a comprehensive understanding of dataset features allowing developers to make informed
    decisions.

    ### Limitations

    - The computation can be expensive from a resource standpoint, particularly for large datasets with numerous fields.
    - The histograms use an arbitrary number of bins which may not be the optimal number of bins for specific data
    distribution.
    - Unsupported data types for columns will raise an error which may limit evaluating the dataset.
    - Fields with all null or missing values are not included in histogram computation.
    - This test only validates the quality of the dataset but doesn't address the model's performance directly.
    """

    name = "dataset_description"
    required_inputs = ["dataset"]
    tasks = [
        "classification",
        "regression",
        "text_classification",
        "text_summarization",
    ]
    tags = ["tabular_data", "time_series_data", "text_data"]

    def summary(self, metric_value):
        """
        Build a dataset summary table. metric_value is a list of fields where each field
        has an id, type (Numeric or Categorical), and statistics. The statistics object
        depends on the type being Numeric or Categorical. For Numeric fields, it has
        the following keys: count, mean, std, min, 25%, 50%, 75%, 90%, 95%, max. For
        categorical fields, it has the following keys: count, unique, top, freq.
        """
        results_table = []
        for field in metric_value:
            field_id = field["id"]
            field_type = field["type"]
            field_statistics = field["statistics"]

            results_table.append(
                {
                    "Name": field_id,
                    "Type": field_type,
                    "Count": field_statistics["count"],
                    "Missing": field_statistics["n_missing"],
                    "Missing %": field_statistics["missing"],
                    "Distinct": field_statistics["n_distinct"],
                    "Distinct %": field_statistics["distinct"],
                }
            )

        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Dataset Description"),
                )
            ]
        )

    def run(self):
        results = []
        for ds_field in self.infer_datatype(self.inputs.dataset.df):
            self.describe_dataset_field(self.inputs.dataset.df, ds_field)
            results.append(ds_field)
        return self.cache_results(results)

    def infer_datatype(self, df):
        vm_dataset_variables = {}
        typeset = ProfilingTypeSet(Settings())
        variable_types = typeset.infer_type(df)

        for column, type in variable_types.items():
            if str(type) == "Unsupported":
                if df[column].isnull().all():
                    vm_dataset_variables[column] = {"id": column, "type": "Null"}
                else:
                    raise UnsupportedColumnTypeError(
                        f"Unsupported type for column {column}. Please review all values in this dataset column."
                    )
            else:
                vm_dataset_variables[column] = {"id": column, "type": str(type)}

        return list(vm_dataset_variables.values())

    def describe_dataset_field(self, df, field):
        """
        Gets descriptive statistics for a single field in a Pandas DataFrame.
        """
        field_type = field["type"]

        # - When we call describe on one field at a time, Pandas will
        #   know better if it needs to report on numerical or categorical statistics
        # - Boolean (binary) fields should be reported as categorical
        #       (force to categorical when nunique == 2)
        if field_type == ["Boolean"] or df[field["id"]].nunique() == 2:
            top_value = df[field["id"]].value_counts().nlargest(1)

            field["statistics"] = {
                "count": df[field["id"]].count(),
                "unique": df[field["id"]].nunique(),
                "top": top_value.index[0],
                "freq": top_value.values[0],
            }
        elif field_type == "Numeric":
            field["statistics"] = (
                df[field["id"]]
                .describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95])
                .to_dict()
            )
        elif field_type == "Categorical" or field_type == "Text":
            field["statistics"] = (
                df[field["id"]].astype("category").describe().to_dict()
            )

        # Initialize statistics object for non-numeric or categorical fields
        if "statistics" not in field:
            field["statistics"] = {}

        field["statistics"]["n_missing"] = df[field["id"]].isna().sum()
        field["statistics"]["missing"] = field["statistics"]["n_missing"] / len(
            df[field["id"]]
        )
        field["statistics"]["n_distinct"] = df[field["id"]].nunique()
        field["statistics"]["distinct"] = field["statistics"]["n_distinct"] / len(
            df[field["id"]]
        )

        field["histograms"] = self.get_field_histograms(df, field["id"], field_type)

    def get_field_histograms(self, df, field, type_):
        """
        Returns a collection of histograms for a numerical or categorical field.
        We store different combinations of bin sizes to allow analyzing the data better

        Will be used in favor of _get_histogram in the future
        """
        # Set the minimum number of bins to nunique if it's less than the default
        if type_ == "Numeric":
            return self.get_numerical_histograms(df, field)
        elif type_ == "Categorical" or type_ == "Boolean":
            value_counts = df[field].value_counts()
            return {
                "default": {
                    "bin_size": len(value_counts),
                    "histogram": value_counts.to_dict(),
                }
            }
        elif type_ == "Text":
            # Combine all the text in the specified field
            text_data = " ".join(df[field].astype(str))
            # Split the text into words (tokens) using a regular expression
            words = re.findall(r"\w+", text_data)
            # Use Counter to count the frequency of each word
            word_counts = Counter(words)

            return {
                "default": {
                    "bin_size": len(word_counts),
                    "histogram": dict(word_counts),
                }
            }
        elif type_ == "Null":
            logger.info(f"Ignoring histogram generation for null column {field}")
        else:
            raise ValueError(
                f"Unsupported field type found when computing its histogram: {type_}"
            )

    def get_numerical_histograms(self, df, field):
        """
        Returns a collection of histograms for a numerical field, each one
        with a different bin size
        """
        values = df[field].to_numpy()
        values_cleaned = values[~np.isnan(values)]

        # bins='sturges'. Cannot use 'auto' until we review and fix its performance
        #  on datasets with too many unique values
        #
        # 'sturges': R’s default method, only accounts for data size. Only optimal
        # for gaussian data and underestimates number of bins for large non-gaussian datasets.
        default_hist = np.histogram(values_cleaned, bins="sturges")

        histograms = {
            "default": {
                "bin_size": len(default_hist[0]),
                "histogram": {
                    "bin_edges": default_hist[1].tolist(),
                    "counts": default_hist[0].tolist(),
                },
            }
        }

        for bin_size in DEFAULT_HISTOGRAM_BIN_SIZES:
            hist = np.histogram(values_cleaned, bins=bin_size)
            histograms[f"bins_{bin_size}"] = {
                "bin_size": bin_size,
                "histogram": {
                    "bin_edges": hist[1].tolist(),
                    "counts": hist[0].tolist(),
                },
            }

        return histograms
