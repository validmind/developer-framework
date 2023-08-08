# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""
from typing import List
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import (
    VMDataset,
    TestResult,
    Figure,
    ThresholdTest,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


@dataclass
class ClassImbalance(ThresholdTest):
    """
    The class imbalance test measures the disparity between the majority
    class and the minority class in the target column.
    """

    category = "data_quality"
    # Changing the name test to avoid a name clash
    name = "nlp_class_imbalance"
    required_context = ["dataset"]
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
        num_classes = len(classes)
        percentages = list(imbalance_percentages.values)

        # Calculating the total number of rows
        total_rows = sum(percentages)

        # Nomralize threshold based on number of classes
        normalize_min_threshold = (
            100 // num_classes - self.params["min_percent_threshold"]
        )
        # Checking class imbalance
        imbalanced_classes = []
        for i, percentage in enumerate(percentages):
            class_label = classes[i]
            proportion = percentage / total_rows * 100
            if proportion < normalize_min_threshold:
                imbalanced_classes.append(
                    {
                        target_column: class_label,
                        "percentage": f"{proportion:.2f}%",
                        "Test": False,
                    }
                )
            else:
                imbalanced_classes.append(
                    {
                        target_column: class_label,
                        "percentage": f"{proportion:.2f}%",
                        "Test": True,
                    }
                )

        resultset = pd.DataFrame(imbalanced_classes)
        results = [
            TestResult(
                column=target_column,
                passed=all(resultset.Test),
                values=resultset.to_dict(orient="records"),
            )
        ]

        fig, ax = plt.subplots()
        sns.barplot(
            x=imbalance_percentages.index, y=imbalance_percentages.values, ax=ax
        )
        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        figures = []
        figures.append(
            Figure(
                for_object=self,
                key=f"{self.name}",
                figure=fig,
            )
        )

        return self.cache_results(results, passed=all(resultset.Test), figures=figures)
