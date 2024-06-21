# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class HighPearsonCorrelation(ThresholdTest):
    """
    Identifies highly correlated feature pairs in a dataset suggesting feature redundancy or multicollinearity.

    **Purpose**: The High Pearson Correlation test measures the linear relationship between features in a dataset, with
    the main goal of identifying high correlations that might indicate feature redundancy or multicollinearity.
    Identification of such issue allows developers and risk management teams to properly deal with potential impacts on
    the machine learning model's performance and interpretability.

    **Test Mechanism**: The test works by generating pairwise Pearson correlations for all features in the dataset,
    then sorting and eliminating duplicate and self-correlations. It assigns a Pass or Fail based on whether the
    absolute value of the correlation coefficient surpasses a pre-set threshold (defaulted at 0.3). It lastly returns
    the top ten strongest correlations regardless of passing or failing status.

    **Signs of High Risk**:
    - A high risk indication would be the presence of correlation coefficients exceeding the threshold.
    - If the features share a strong linear relationship, this could lead to potential multicollinearity and model
    overfitting.
    - Redundancy of variables can undermine the interpretability of the model due to uncertainty over the authenticity
    of individual variable's predictive power.

    **Strengths**:
    - The High Pearson Correlation test provides a quick and simple means of identifying relationships between feature
    pairs.
    - It generates a transparent output which not only displays pairs of correlated variables but also delivers the
    Pearson correlation coefficient and a Pass or Fail status for each.
    - It aids early identification of potential multicollinearity issues that may disrupt model training.

    **Limitations**:
    - The Pearson correlation test can only delineate linear relationships. It fails to shed light on nonlinear
    relationships or dependencies.
    - It is sensitive to outliers where a few outliers could notably affect the correlation coefficient.
    - It is limited to identifying redundancy only within feature pairs. When three or more variables are linearly
    dependent, it may fail to spot this complex relationship.
    - The top 10 result filter might not fully capture the richness of the data; an option to configure the number of
    retained results could be helpful.
    """

    name = "pearson_correlation"
    required_inputs = ["dataset"]
    default_params = {"max_threshold": 0.3}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "data_quality", "correlation"]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        """The high pearson correlation test returns results like these:
        [
            {
                "values": {
                    "correlations": [
                        {"column": "NumOfProducts", "correlation": -0.3044645622389459}
                    ]
                },
                "column": "Balance",
                "passed": false,
            }
        ]
        """
        results_table = [
            {
                "Columns": f'({result.column}, {result.values["correlations"][0]["column"]})',
                "Coefficient": result.values["correlations"][0]["correlation"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="High Pearson Correlation Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        corr = self.inputs.dataset.df.corr(numeric_only=True)

        # Create a table of correlation coefficients and column pairs
        corr_table = corr.unstack().sort_values(
            kind="quicksort", key=abs, ascending=False
        )
        corr_df = pd.DataFrame(corr_table).reset_index()
        corr_df.columns = ["Column1", "Column2", "Coefficient"]

        # Remove duplicate correlations and self-correlations
        corr_df = corr_df.loc[corr_df["Column1"] < corr_df["Column2"]]

        # Assign Pass/Fail based on correlation coefficient
        corr_df["Pass/Fail"] = np.where(
            corr_df["Coefficient"].abs() <= self.params["max_threshold"], "Pass", "Fail"
        )

        # Only keep the top 10 correlations. TODO: configurable
        corr_df = corr_df.head(10)

        passed = corr_df["Pass/Fail"].eq("Pass").all()

        results = [
            ThresholdTestResult(
                column=col1,
                values={
                    "correlations": [
                        {
                            "column": col2,
                            "correlation": coeff,
                        }
                    ]
                },
                passed=pass_fail == "Pass",
            )
            for _, (col1, col2, coeff, pass_fail) in corr_df.iterrows()
        ]

        return self.cache_results(results, passed=passed)
