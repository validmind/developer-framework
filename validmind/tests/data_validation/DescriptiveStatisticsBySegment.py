# Copyright © 2023 ValidMind Inc. All rights reserved.
from dataclasses import dataclass
from typing import Dict

import pandas as pd
from scipy import stats

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class DescriptiveStatisticsBySegment(Metric):
    """
    Computes and summarizes descriptive statistics for each feature across different segments of a dataset.

    **Purpose**: This class aims to provide comprehensive descriptive statistics for each feature within various
    segments of a dataset or across multiple datasets. It assists in understanding the distribution, central tendency,
    and spread of data values, which is crucial for informing data preprocessing steps and ensuring the validity of
    machine learning models.

    **Test Mechanism**: The class iterates over each provided dataset and optionally, each segment within those
    datasets, to compute a range of descriptive statistics for each feature. These statistics include mean, median,
    standard deviation, skewness, kurtosis, minimum, 25th percentile, 75th percentile, and maximum. The results are
    aggregated into a comprehensive table, displaying the statistics by dataset, segment, and feature.

    **Strengths**:
    - Offers a detailed and granular view of the data distribution for each feature, aiding in data understanding and
      preprocessing.
    - Facilitates the identification of outliers, data errors, and features with skewed distributions, which can
      significantly impact machine learning models.
    - Supports multiple datasets and segmentation, enabling comparative analysis and ensuring consistency across
      different data slices.

    **Limitations**:
    - Descriptive statistics alone may not capture all the nuances of data distribution, especially for complex or
      non-linear relationships.
    - The class may require additional context or domain knowledge to interpret the results effectively and decide
      on the appropriate data preprocessing steps.
    - The segmentation parameter needs to be set thoughtfully to ensure meaningful and interpretable results.

    """

    category = "data_analysis"
    name = "descriptive_statistics"
    required_inputs = ["dataset"]
    default_params = {"segments": None, "dataset_names": None}
    metadata = {
        "task_types": ["classification", "regression", "clustering"],
        "tags": ["tabular_data", "data_analysis", "descriptive_statistics"],
    }

    def run(self):
        datasets = self.dataset if isinstance(self.dataset, list) else [self.dataset]

        dataset_names = self.params["dataset_names"]
        if self.params["dataset_names"] is None:
            dataset_names = [f"Dataset {i+1}" for i in range(len(datasets))]

        descriptive_stats_df = self.descriptive_stats_by_segment(
            datasets, dataset_names
        )
        return self.cache_results(
            {"descriptive_stats_table": descriptive_stats_df.to_dict(orient="records")}
        )

    def summary(self, metric_value: Dict):
        descriptive_stats_table = metric_value["descriptive_stats_table"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=descriptive_stats_table,
                    metadata=ResultTableMetadata(
                        title="Descriptive Statistics for Features per Dataset and Segment"
                    ),
                )
            ]
        )

    def descriptive_stats_by_segment(self, datasets, dataset_names):
        results = []
        segments = self.params["segments"]

        for dataset, dataset_name in zip(datasets, dataset_names):
            feature_columns = dataset.feature_columns

            # If segments is None, compute descriptive stats for the entire dataset
            if segments is None:
                for feature in feature_columns:
                    data = dataset._df[feature].dropna()
                    results.append(
                        self.compute_stats(dataset_name, "N/A", "N/A", feature, data)
                    )

            else:
                # If segments are provided, compute descriptive stats per segment value
                for segment in segments:
                    if segment not in dataset._df.columns:
                        for feature in feature_columns:
                            results.append(
                                {
                                    "Dataset": dataset_name,
                                    "Segment": segment,
                                    "Segment Value": "N/A",
                                    "Feature": feature,
                                    "Mean": "N/A",
                                    "Median": "N/A",
                                    "Standard Deviation": "N/A",
                                    "Skewness": "N/A",
                                    "Kurtosis": "N/A",
                                    "Minimum": "N/A",
                                    "25th Percentile": "N/A",
                                    "75th Percentile": "N/A",
                                    "Maximum": "N/A",
                                }
                            )
                    else:
                        unique_values = dataset._df[segment].dropna().unique()

                        for value in unique_values:
                            for feature in feature_columns:
                                data = dataset._df[dataset._df[segment] == value][
                                    feature
                                ].dropna()
                                results.append(
                                    self.compute_stats(
                                        dataset_name, segment, value, feature, data
                                    )
                                )

        return pd.DataFrame(results)

    def compute_stats(self, dataset_name, segment, segment_value, feature, data):
        if len(data) == 0:
            return {
                "Dataset": dataset_name,
                "Segment": segment,
                "Segment Value": segment_value,
                "Feature": feature,
                "Mean": "N/A",
                "Median": "N/A",
                "Standard Deviation": "N/A",
                "Skewness": "N/A",
                "Kurtosis": "N/A",
                "Minimum": "N/A",
                "25th Percentile": "N/A",
                "75th Percentile": "N/A",
                "Maximum": "N/A",
            }

        return {
            "Dataset": dataset_name,
            "Segment": segment,
            "Segment Value": segment_value,
            "Feature": feature,
            "Mean": data.mean(),
            "Median": data.median(),
            "Standard Deviation": data.std(),
            "Skewness": data.skew(),
            "Kurtosis": stats.kurtosis(data),
            "Minimum": data.min(),
            "25th Percentile": data.quantile(0.25),
            "75th Percentile": data.quantile(0.75),
            "Maximum": data.max(),
        }
