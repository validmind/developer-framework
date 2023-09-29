# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.errors import SkipTestError
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelsCoeffs(Metric):
    """
    **Purpose**: The 'RegressionModelsCoeffs' test is designed to evaluate and compare the coefficients of different
    regression models that were trained on the same dataset. This metric assesses how each model weighted the
    importance of various features during training, which is useful for analyzing which features influenced the model's
    outputs the most, and how these influence patterns vary between different models.

    **Test Mechanism**: This test measures the coefficients of each regression model by calling the
    'regression_coefficients()' method on the model. These coefficients are then compiled into a summary dataframe for
    all models. Each row in the dataframe corresponds to a model, with a column for each feature's coefficient. Note,
    this test is only applicable to 'statsmodels' and 'R' models, and will raise a 'SkipTestError' for models from
    other libraries.

    **Signs of High Risk**: Instances that might suggest high risk associated with this test include: discrepancies in
    the way different models weigh features, if any coefficient is unexpectedly high or low, or the test could not be
    applied to certain models because they are not of the 'statsmodels' or 'R' types.

    **Strengths**: This test is highly valuable for gaining insight into the training process of different models and
    for comparing how the models considered the importance of various features. By monitoring the feature coefficients,
    this test provides a more transparent evaluation of the model and surfaces crucial weights and biases in the
    training process.

    **Limitations**: The primary limitation of this test is its compatibility: it is only designed for use with
    'statsmodels' and 'R' regression models. Beyond this, while the test contrasts the ways various models weigh
    features, it does not indicate which weighting is most appropriate or accurate, leaving room for interpretation.
    Lastly, this test does not account for potential overfitting or underfitting of models, and the coefficients it
    produces might not translate to effective performance on unseen data.
    """

    name = "regression_models_coefficients"
    metadata = {
        "task_types": ["regression"],
        "tags": ["model_comparison"],
    }

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
        if not self.models or len(self.models) == 0:
            raise ValueError("List of models must be provided in the models parameter")

        for model in self.models:
            if model.model_class() != "statsmodels" and model.model_class() != "R":
                raise SkipTestError(
                    "Only statsmodels and R models are supported for this metric"
                )

        coefficients = [m.regression_coefficients() for m in self.models]
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
