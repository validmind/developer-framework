# Copyright © 2023 ValidMind Inc. All rights reserved.
from dataclasses import dataclass
from typing import Any, Dict, List

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class MissingValuesBySegment(Metric):
    """
    Evaluates dataset quality by assessing the ratio of missing values within each segment of the dataset, broken down by feature.

    **Purpose**: The main goal of this class is to provide a detailed analysis of missing values across different
    segments of a dataset or multiple datasets, on a per-feature basis. It ensures that the data quality is maintained
    by identifying sections of the dataset that may require attention due to a high ratio of missing values.
    This is crucial for ensuring the reliability of machine learning models, as missing values can lead to biased or
    incorrect predictions.

    **Test Mechanism**: The test works by iterating over each dataset provided, and optionally, each segment within
    those datasets. It calculates the total number of missing values, the percentage of missing values, and breaks
    down these statistics per feature. The results are then collated into a comprehensive table that breaks down
    the missing value statistics by dataset, segment, and feature. This table includes information on the number of
    missing values, the total number of values, and the percentage of missing values for each feature.

    **Signs of High Risk**:
    - A feature within a segment with a missing value percentage greater than the `min_threshold` parameter is
      considered high risk.
    - Multiple features across different segments or datasets showing high missing value ratios can also be indicative
      of systemic issues with the data collection or preprocessing steps, signaling a need for further investigation.

    **Strengths**:
    - This class provides a granular view of missing values on a per-feature basis, allowing for a detailed analysis
      that can pinpoint specific areas of concern.
    - It helps maintain high data quality by identifying features within segments of the dataset that may be unreliable
      due to excessive missing values, ensuring the robustness of subsequent machine learning models.

    **Limitations**:
    - The class does not provide direct insights into the causes of the missing values or offer strategies for handling
      or imputing them.
    - There is a potential risk of missing subtle patterns of missingness if the segments are not appropriately defined
      or if the `min_threshold` parameter is not set at an optimal level.
    - The test does not account for values that are encoded in a way that masks their missing status (such as placeholder
      or sentinel values).

    """

    category = "data_quality"
    name = "missing_by_feature_segment"
    required_inputs = ["dataset"]
    default_params = {"segments": None, "dataset_names": None, "min_threshold": 1}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality"],
    }

    def run(self):
        datasets = self.dataset if isinstance(self.dataset, list) else [self.dataset]

        dataset_names = self.params["dataset_names"]
        if self.params["dataset_names"] is None:
            dataset_names = [f"Dataset {i+1}" for i in range(len(datasets))]

        missing_values_df = self.missing_values_by_feature_segment(
            datasets, dataset_names
        )
        return self.cache_results(
            {"missing_values_table": missing_values_df.to_dict(orient="records")}
        )

    def summary(self, metric_value: Dict[str, Any]) -> ResultSummary:
        missing_values_table = metric_value["missing_values_table"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=missing_values_table,
                    metadata=ResultTableMetadata(
                        title="Missing Values for Features per Dataset and Segment"
                    ),
                )
            ]
        )

    def missing_values_by_feature_segment(
        self, datasets: List[pd.DataFrame], dataset_names: List[str]
    ) -> pd.DataFrame:
        results = []
        segments = self.params["segments"]

        for dataset, dataset_name in zip(datasets, dataset_names):
            feature_columns = dataset.feature_columns

            # If segments is None, compute missing stats for the entire dataset per feature
            if segments is None:
                for feature in feature_columns:
                    missing_values = dataset._df[feature].isnull().sum()
                    total_values = len(dataset._df)
                    missing_percentage = (missing_values / total_values) * 100

                    results.append(
                        {
                            "Dataset": dataset_name,
                            "Segment": "N/A",
                            "Segment Value": "N/A",
                            "Feature": feature,
                            "Missing Values": missing_values,
                            "Total Values": total_values,
                            "Missing Percentage": missing_percentage,
                        }
                    )
            else:
                # If segments are provided, compute missing stats per segment value for each feature
                for segment in segments:
                    if segment not in dataset._df.columns:
                        for feature in feature_columns:
                            results.append(
                                {
                                    "Dataset": dataset_name,
                                    "Segment": segment,
                                    "Segment Value": "N/A",
                                    "Feature": feature,
                                    "Missing Values": "N/A",
                                    "Total Values": "N/A",
                                    "Missing Percentage": "N/A",
                                }
                            )
                    else:
                        unique_values = dataset._df[segment].dropna().unique()

                        for value in unique_values:
                            subset = dataset._df[dataset._df[segment] == value]
                            for feature in feature_columns:
                                missing_values = subset[feature].isnull().sum()
                                total_values = len(subset)
                                missing_percentage = (
                                    missing_values / total_values
                                ) * 100

                                results.append(
                                    {
                                        "Dataset": dataset_name,
                                        "Segment": segment,
                                        "Segment Value": value,
                                        "Feature": feature,
                                        "Missing Values": missing_values,
                                        "Total Values": total_values,
                                        "Missing Percentage": missing_percentage,
                                    }
                                )

        return pd.DataFrame(results)
