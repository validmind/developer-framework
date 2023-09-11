# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""
from dataclasses import dataclass
from typing import List

import pandas as pd
import plotly.graph_objs as go

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
    VMDataset,
)


@dataclass
class ClassImbalance(ThresholdTest):
    """
    The class imbalance test measures the disparity between the majority
    class and the minority class in the target column.
    """

    category = "data_quality"
    # Changing the name test to avoid a name clash
    name = "class_imbalance"
    required_inputs = ["dataset"]
    default_params = {"min_percent_threshold": 10}

    def summary(self, results: List[TestResult], all_passed: bool):
        return ResultSummary(
            results=[
                ResultTable(
                    data=results[0].values,
                    metadata=ResultTableMetadata(
                        title=f"Class Imbalance Results for Column {self.dataset.target_column}"
                    ),
                )
            ]
        )

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("ClassImbalance requires a validmind Dataset object")

        if self.dataset.target_column is None:
            print("Skipping class_imbalance test because no target column is defined")
            return

        target_column = self.dataset.target_column
        imbalance_percentages = self.dataset.df[target_column].value_counts(
            normalize=True
        )

        classes = list(imbalance_percentages.index)
        percentages = list(imbalance_percentages.values)

        # Calculating the total number of rows
        # total_rows = sum(percentages)

        # Checking class imbalance
        imbalanced_classes = []
        for i, percentage in enumerate(percentages):
            class_label = classes[i]
            proportion = percentage * 100
            passed = proportion > self.params["min_percent_threshold"]

            imbalanced_classes.append(
                {
                    target_column: class_label,
                    "Percentage of Rows (%)	": f"{proportion:.2f}%",
                    "Pass/Fail": "Pass" if passed else "Fail",
                }
            )

        resultset = pd.DataFrame(imbalanced_classes)
        tests_failed = all(resultset["Pass/Fail"] == "Pass")
        results = [
            TestResult(
                column=target_column,
                passed=tests_failed,
                values=resultset.to_dict(orient="records"),
            )
        ]

        # Create a bar chart trace
        trace = go.Bar(
            x=imbalance_percentages.index,
            y=imbalance_percentages.values,
        )

        # Create a layout for the chart
        layout = go.Layout(
            title=f"Class Imbalance Results for Target Column {self.dataset.target_column}",
            xaxis=dict(title="Class"),
            yaxis=dict(title="Percentage"),
        )

        # Create a figure and add the trace and layout
        fig = go.Figure(data=[trace], layout=layout)

        return self.cache_results(
            results,
            passed=tests_failed,
            figures=[
                Figure(
                    for_object=self,
                    key=f"{self.name}",
                    figure=fig,
                )
            ],
        )
