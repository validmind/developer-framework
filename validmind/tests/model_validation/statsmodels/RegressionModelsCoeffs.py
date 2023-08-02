# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd

from validmind.vm_models import (
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


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

    def extract_coef_stats(self, summary, model_name):
        table = summary.tables[1].data
        headers = table.pop(0)
        headers[0] = "Feature"
        df = pd.DataFrame(table, columns=headers)
        df["Model"] = model_name
        return df

    def extract_coefficients_summary(self, summaries):
        coef_stats_df = pd.DataFrame()

        for i, summary in enumerate(summaries):
            model_name = f"Model {i+1}"
            coef_stats_df = pd.concat(
                [coef_stats_df, self.extract_coef_stats(summary, model_name)]
            )

        # Reorder columns to have 'Model' as the first column and reset the index
        coef_stats_df = coef_stats_df.reset_index(drop=True)[
            ["Model"] + [col for col in coef_stats_df.columns if col != "Model"]
        ]

        return coef_stats_df

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []

        if self.models is not None:
            all_models.extend(self.models)

        for m in all_models:
            if not Model.is_supported_model(m.model):
                raise ValueError(
                    f"{Model.model_library(m.model)}.{Model.model_class(m.model)} \
                              is not supported by ValidMind framework yet"
                )

        summaries = [m.model.summary() for m in all_models]
        coef_stats_df = self.extract_coefficients_summary(summaries)

        return self.cache_results(
            {
                "coefficients_summary": coef_stats_df.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the regression models' coefficients
        """
        summary_coefficients = metric_value["coefficients_summary"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_coefficients,
                    metadata=ResultTableMetadata(
                        title="Regression Models' Coefficients"
                    ),
                ),
            ]
        )
