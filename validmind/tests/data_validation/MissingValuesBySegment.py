# Copyright © 2023 ValidMind Inc. All rights reserved.
from dataclasses import dataclass
from typing import Dict

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class MissingValuesBySegment(Metric):
    category = "data_quality"
    name = "missing"
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

        missing_values_df = self.missing_values_by_segment(datasets, dataset_names)
        return self.cache_results(
            {"missing_values_table": missing_values_df.to_dict(orient="records")}
        )

    def summary(self, metric_value: Dict):
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

    def missing_values_by_segment(self, datasets, dataset_names):
        results = []
        segments = self.params["segments"]

        for dataset, dataset_name in zip(datasets, dataset_names):
            feature_columns = dataset.feature_columns

            # If segments is None, compute missing stats for the entire dataset
            if segments is None:
                missing_values = dataset._df[feature_columns].isnull().sum().sum()
                total_values = len(dataset._df) * len(feature_columns)
                missing_percentage = (missing_values / total_values) * 100

                results.append(
                    {
                        "Dataset": dataset_name,
                        "Segment": "N/A",
                        "Segment Value": "N/A",
                        "Missing Values": missing_values,
                        "Total Values": total_values,
                        "Missing Percentage": missing_percentage,
                    }
                )
            else:
                # If segments are provided, compute missing stats per segment value
                for segment in segments:
                    if segment not in dataset._df.columns:
                        results.append(
                            {
                                "Dataset": dataset_name,
                                "Segment": segment,
                                "Segment Value": "N/A",
                                "Missing Values": "N/A",
                                "Total Values": "N/A",
                                "Missing Percentage": "N/A",
                            }
                        )
                    else:
                        unique_values = dataset._df[segment].dropna().unique()

                        for value in unique_values:
                            subset = dataset._df[dataset._df[segment] == value][
                                feature_columns
                            ]
                            missing_values = subset.isnull().sum().sum()
                            total_values = len(subset) * len(feature_columns)
                            missing_percentage = (missing_values / total_values) * 100

                            results.append(
                                {
                                    "Dataset": dataset_name,
                                    "Segment": segment,
                                    "Segment Value": value,
                                    "Missing Values": missing_values,
                                    "Total Values": total_values,
                                    "Missing Percentage": missing_percentage,
                                }
                            )

        return pd.DataFrame(results)
