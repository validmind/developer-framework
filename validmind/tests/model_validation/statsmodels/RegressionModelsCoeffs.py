# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.errors import SkipTestError
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelsCoeffs(Metric):
    """
    Test that outputs the coefficients of stats library regression models.
    """

    name = "regression_models_coefficients"

    def description(self):
        return """
        This section shows the coefficients of different regression models that were
        trained on the same dataset. This can be useful for comparing how different
        models weigh the importance of various features in the dataset.
        """

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
