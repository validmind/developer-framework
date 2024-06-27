# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd

from validmind.errors import SkipTestError
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelsCoeffs(Metric):
    """
    Compares feature importance by evaluating and contrasting coefficients of different regression models.

    **Purpose**: The 'RegressionModelsCoeffs' metric is utilized to evaluate and compare coefficients of different
    regression models trained on the same dataset. By examining how each model weighted the importance of different
    features during training, this metric provides key insights into which factors have the most impact on the model's
    predictions and how these patterns differ across models.

    **Test Mechanism**: The test operates by extracting the coefficients of each regression model using the
    'regression_coefficients()' method. These coefficients are then consolidated into a dataframe, with each row
    representing a model and columns corresponding to each feature's coefficient. It must be noted that this test is
    exclusive to 'statsmodels' and 'R' models, other models will result in a 'SkipTestError'.

    **Signs of High Risk**:
    - Discrepancies in how different models weight the same features
    - Unexpectedly high or low coefficients
    - The test is inapplicable to certain models because they are not from 'statsmodels' or 'R' libraries

    **Strengths**:
    - Enables insight into the training process of different models
    - Allows comparison of feature importance across models
    - Through the review of feature coefficients, the test provides a more transparent evaluation of the model and
    highlights significant weights and biases in the training procedure

    **Limitations**:
    - The test is only compatible with 'statsmodels' and 'R' regression models
    - While the test provides contrast in feature weightings among models, it does not establish the most appropriate
    or accurate weighting, thus remaining subject to interpretation
    - It does not account for potential overfitting or underfitting of models
    - The computed coefficients might not lead to effective performance on unseen data
    """

    name = "regression_models_coefficients"
    required_inputs = ["models"]
    tasks = ["regression"]
    tags = ["model_comparison"]

    def _build_model_summaries(self, all_coefficients):
        all_models_df = pd.DataFrame()

        for i, coefficients in enumerate(all_coefficients):
            model_name = f"Model {i+1}"
            # The coefficients summary object needs an additional "Model" column at the beginning
            coefficients["Model"] = model_name
            all_models_df = pd.concat([all_models_df, coefficients])

        # Reorder columns to have 'Model' as the first column and reset the index
        all_models_df = all_models_df.reset_index(drop=True)[
            ["Model"] + [col for col in all_models_df.columns if col != "Model"]
        ]

        return all_models_df

    def run(self):
        # Check models list is not empty
        if not self.inputs.models or len(self.inputs.models) == 0:
            raise ValueError("List of models must be provided in the models parameter")

        for model in self.inputs.models:
            if model.library != "statsmodels":
                raise SkipTestError(
                    "Only statsmodels models are supported for this metric"
                )

        coefficients = [m.regression_coefficients() for m in self.inputs.models]
        all_models_summary = self._build_model_summaries(coefficients)

        return self.cache_results(
            {
                "coefficients_summary": all_models_summary.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the regression models' coefficients
        """
        coefficients_summary = metric_value["coefficients_summary"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=coefficients_summary,
                    metadata=ResultTableMetadata(
                        title="Regression Models' Coefficients"
                    ),
                ),
            ]
        )
