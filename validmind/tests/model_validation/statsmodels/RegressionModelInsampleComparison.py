# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

from validmind.statsutils import adj_r2_score
from validmind.vm_models import (
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


@dataclass
class RegressionModelInsampleComparison(Metric):
    """
    Test that output the comparison of stats library regression models.
    """

    name = "regression_insample_performance"

    def description(self):
        return """
        This section shows In-sample comparison of regression models involves comparing
        the performance of different regression models on the same dataset that was used
        to train the models. This is typically done by calculating a goodness-of-fit statistic
        such as the R-squared or mean squared error (MSE) for each model, and then comparing
        these statistics to determine which model has the best fit to the data.
        """

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
        results = self._in_sample_performance_ols(all_models)
        return self.cache_results(
            {
                "in_sample_performance": pd.DataFrame(results).to_dict(
                    orient="records"
                ),
            }
        )

    def _in_sample_performance_ols(self, models):
        """
        Computes the in-sample performance evaluation metrics for a list of OLS models.
        Args:
        models (list): A list of statsmodels OLS models.
        Returns:
        list: A list of dictionaries containing the evaluation results for each model.
        Each dictionary contains the following keys:
        - 'Model': A string identifying the model.
        - 'Independent Variables': A list of strings identifying the independent variables used in the model.
        - 'R-Squared': The R-squared value of the model.
        - 'Adjusted R-Squared': The adjusted R-squared value of the model.
        - 'MSE': The mean squared error of the model.
        - 'RMSE': The root mean squared error of the model.
        """
        evaluation_results = []

        for i, model in enumerate(models):
            X_columns = model.train_ds.get_features_columns()
            y_true = self.model.train_ds.y
            y_pred = self.model.model.predict(self.model.train_ds.x)

            # Extract R-squared and Adjusted R-squared
            r2 = r2_score(y_true, y_pred)
            adj_r2 = adj_r2_score(y_true, y_pred, len(y_true), len(X_columns))
            mse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=True)
            rmse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False)

            # Append the results to the evaluation_results list
            evaluation_results.append(
                {
                    "Model": f"Model {i + 1}",
                    "Independent Variables": X_columns,
                    "R-Squared": r2,
                    "Adjusted R-Squared": adj_r2,
                    "MSE": mse,
                    "RMSE": rmse,
                }
            )

        return evaluation_results

    def summary(self, metric_value):
        """
        Build one table for summarizing the in-sample performance results
        """
        summary_in_sample_performance = metric_value["in_sample_performance"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_in_sample_performance,
                    metadata=ResultTableMetadata(title="In-Sample Performance Results"),
                ),
            ]
        )
