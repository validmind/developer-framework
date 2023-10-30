# Copyright © 2023 ValidMind Inc. All rights reserved.
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class MissingValuesBySegment(Metric):
    category = "data_quality"
    name = "missing"
    required_inputs = ["datasets"]  # Updated to handle multiple datasets
    default_params = {"segments": None, "min_threshold": 1}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality"],
    }

    def run(self):
        missing_values_df = self.missing_values_by_segment()
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

    def missing_values_by_segment(self):
        results = []
        segments = self.params["segments"]
        datasets = self.dataset if isinstance(self.dataset, list) else [self.dataset]
        dataset_names = [f"Dataset {i+1}" for i in range(len(datasets))]

        print("Starting missing values analysis...")

        for dataset, dataset_name in zip(datasets, dataset_names):
            print(f"\nAnalyzing {dataset_name}")

            feature_columns = dataset.feature_columns
            print(f"Feature columns: {feature_columns}")

            # If segments is None, compute missing stats for the entire dataset
            if segments is None:
                print("\nSegments not provided, analyzing entire dataset.")
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
                    print(f"\nAnalyzing segment: {segment}")

                    if segment not in dataset._df.columns:
                        print(f"Segment {segment} not found in dataset.")
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
                        print(f"Segment {segment} found. Calculating missing values...")
                        unique_values = dataset._df[segment].dropna().unique()
                        print(f"Unique values in segment {segment}: {unique_values}")

                        for value in unique_values:
                            print(f"\nAnalyzing segment value: {value}")
                            subset = dataset._df[dataset._df[segment] == value][
                                feature_columns
                            ]
                            missing_values = subset.isnull().sum().sum()
                            total_values = len(subset) * len(feature_columns)
                            missing_percentage = (missing_values / total_values) * 100

                            print(f"Missing Values: {missing_values}")
                            print(f"Total Values: {total_values}")
                            print(f"Missing Percentage: {missing_percentage:.2f}%")

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

        print("\nMissing values analysis complete.")
        return pd.DataFrame(results)
