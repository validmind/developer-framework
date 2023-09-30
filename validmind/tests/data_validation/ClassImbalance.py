# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""
from dataclasses import dataclass
from typing import List

import pandas as pd
import plotly.graph_objs as go

from validmind.errors import SkipTestError
from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
    VMDataset,
)


@dataclass
class ClassImbalance(ThresholdTest):
    """
    **Purpose**: The purpose of the ClassImbalance test is to assess the distribution of the target classes in a
    dataset used for a machine learning model. Particularly, this method is geared towards ensuring that the classes
    are not too skewed, which could bias the predictions of the model. It is important to have a balanced dataset for
    training to avoid biased model with high accuracy for the majority class and low accuracy for the minority class.

    **Test Mechanism**: The ClassImbalance test functions by determining the frequency (in percentage proportion) of
    each class in the target column of the dataset and checks whether each class appears in at least a particular
    minimum percentage of the total records. This minimum percentage is a parameter that can be pre-set or changed
    according to requirements; the default value in this case is set to 10%.

    **Signs of High Risk**: Any class that constitutes less than the preset minimum percentage threshold is flagged as
    a high risk, indicating potential class imbalance. The function provides a pass/fail verdict for each class based
    on this criterion. In essence, if any class fails this test, the dataset is likely to contain an imbalanced class
    distribution.

    **Strengths**:

    1. Identifies under-represented classes which can impact the performance of a machine learning model.
    2. Easy and fast to compute.
    3. The test is very informative as it not only detects imbalance but also quantifies the degree of imbalance.
    4. Adjustable threshold allows flexibility and adaptation to varying use-cases or domain-specific requirements.
    5. The test generates a visually intuitive plot showing classes and their corresponding proportions, aiding in
    interpretability and understanding of the data.

    **Limitations**:

    1. The test might not perform well, or offer useful insights for datasets with too many classes. The imbalance may
    be inevitable due to the inherent class distribution.
    2. Sensitivity to the threshold value may lead to false discrimination of imbalance when the threshold is set too
    high.
    3. Irrespective of the percentage threshold, it does not account for different costs or impacts of
    misclassification of different classes, which can vary based on specific application or domain.
    4. While it can identify imbalances in class distribution, it does not offer direct ways to handle or correct such
    imbalances.
    5. The test is only applicable for classification tasks and not for regression or clustering tasks.
    """

    category = "data_quality"
    # Changing the name test to avoid a name clash
    name = "class_imbalance"
    required_inputs = ["dataset"]
    default_params = {"min_percent_threshold": 10}
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "binary_classification", "multiclass_classification"],
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
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
        if len(imbalance_percentages) > 10:
            raise SkipTestError(
                f"Skipping {self.__class__.__name__} test as"
                "target column as more than 10 classes"
            )

        classes = list(imbalance_percentages.index)
        percentages = list(imbalance_percentages.values)

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
            ThresholdTestResult(
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
