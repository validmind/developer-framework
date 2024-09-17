# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
    Evaluates and quantifies class distribution imbalance in a dataset used by a machine learning model.

    ### Purpose

    The Class Imbalance test is designed to evaluate the distribution of target classes in a dataset that's utilized by
    a machine learning model. Specifically, it aims to ensure that the classes aren't overly skewed, which could lead
    to bias in the model's predictions. It's crucial to have a balanced training dataset to avoid creating a model
    that's biased with high accuracy for the majority class and low accuracy for the minority class.

    ### Test Mechanism

    This Class Imbalance test operates by calculating the frequency (expressed as a percentage) of each class in the
    target column of the dataset. It then checks whether each class appears in at least a set minimum percentage of the
    total records. This minimum percentage is a modifiable parameter, but the default value is set to 10%.

    ### Signs of High Risk

    - Any class that represents less than the pre-set minimum percentage threshold is marked as high risk, implying a
    potential class imbalance.
    - The function provides a pass/fail outcome for each class based on this criterion.
    - Fundamentally, if any class fails this test, it's highly likely that the dataset possesses imbalanced class
    distribution.

    ### Strengths

    - The test can spot under-represented classes that could affect the efficiency of a machine learning model.
    - The calculation is straightforward and swift.
    - The test is highly informative because it not only spots imbalance, but it also quantifies the degree of
    imbalance.
    - The adjustable threshold enables flexibility and adaptation to differing use-cases or domain-specific needs.
    - The test creates a visually insightful plot showing the classes and their corresponding proportions, enhancing
    interpretability and comprehension of the data.

    ### Limitations

    - The test might struggle to perform well or provide vital insights for datasets with a high number of classes. In
    such cases, the imbalance could be inevitable due to the inherent class distribution.
    - Sensitivity to the threshold value might result in faulty detection of imbalance if the threshold is set
    excessively high.
    - Regardless of the percentage threshold, it doesn't account for varying costs or impacts of misclassifying
    different classes, which might fluctuate based on specific applications or domains.
    - While it can identify imbalances in class distribution, it doesn't provide direct methods to address or correct
    these imbalances.
    - The test is only applicable for classification operations and unsuitable for regression or clustering tasks.
    """

    # Changing the name test to avoid a name clash
    name = "class_imbalance"
    required_inputs = ["dataset"]
    default_params = {"min_percent_threshold": 10}
    tasks = ["classification"]
    tags = ["tabular_data", "binary_classification", "multiclass_classification"]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        return ResultSummary(
            results=[
                ResultTable(
                    data=results[0].values,
                    metadata=ResultTableMetadata(
                        title=f"Class Imbalance Results for Column {self.inputs.dataset.target_column}"
                    ),
                )
            ]
        )

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.inputs.dataset, VMDataset):
            raise ValueError("ClassImbalance requires a validmind Dataset object")

        if self.inputs.dataset.target_column is None:
            print("Skipping class_imbalance test because no target column is defined")
            return

        target_column = self.inputs.dataset.target_column
        imbalance_percentages = self.inputs.dataset.df[target_column].value_counts(
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
            title=f"Class Imbalance Results for Target Column {self.inputs.dataset.target_column}",
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

    def test(self):
        """Unit test for ClassImbalance"""
        assert self.result is not None

        assert self.result.test_results is not None
        assert self.result.test_results.passed

        assert self.result.figures is not None
