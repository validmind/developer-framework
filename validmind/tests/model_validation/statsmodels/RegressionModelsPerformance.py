# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from sklearn.metrics import mean_squared_error, r2_score

from validmind.vm_models import (
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


@dataclass
class RegressionModelsPerformance(Metric):
    """
    Test that outputs the comparison of stats library regression models.
    """

    name = "regression_models_performance"

    def description(self):
        return """
        This section shows the in-sample and out-of-sample comparison of regression models. In-sample comparison involves comparing the performance of different regression models on the same dataset that was used to train the models. Out-of-sample comparison evaluates the performance of the models on unseen data. This is typically done by calculating goodness-of-fit statistics such as R-squared and mean squared error (MSE) for each model, and then comparing these statistics to determine which model has the best fit to the data.
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

        in_sample_results = self._in_sample_performance_ols(all_models)
        out_of_sample_results = self._out_sample_performance_ols(all_models)

        return self.cache_results(
            {
                "in_sample_performance": in_sample_results,
                "out_of_sample_performance": out_of_sample_results,
            }
        )

    def _in_sample_performance_ols(self, models):
        evaluation_results = []

        for i, model in enumerate(models):
            X_columns = model.train_ds.get_features_columns()
            y_true = model.train_ds.y
            y_pred = model.model.predict(model.train_ds.x)

            # Extract R-squared and Adjusted R-squared
            r2 = r2_score(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            adj_r2 = 1 - ((1 - r2) * (len(y_true) - 1)) / (
                len(y_true) - len(X_columns) - 1
            )

            # Append the results to the evaluation_results list
            evaluation_results.append(
                {
                    "Model": f"Model {i + 1}",
                    "Independent Variables": X_columns,
                    "R-Squared": r2,
                    "Adjusted R-Squared": adj_r2,
                    "MSE": mse,
                }
            )

        return evaluation_results

    def _out_sample_performance_ols(self, models):
        evaluation_results = []

        for i, model in enumerate(models):
            X_columns = model.train_ds.get_features_columns()
            y_true = model.test_ds.y
            y_pred = model.model.predict(model.test_ds.x)

            # Extract R-squared and Adjusted R-squared
            r2 = r2_score(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            adj_r2 = 1 - ((1 - r2) * (len(y_true) - 1)) / (
                len(y_true) - len(X_columns) - 1
            )

            # Append the results to the evaluation_results list
            evaluation_results.append(
                {
                    "Model": f"Model {i + 1}",
                    "Independent Variables": X_columns,
                    "R-Squared": r2,
                    "Adjusted R-Squared": adj_r2,
                    "MSE": mse,
                }
            )

        return evaluation_results

    def summary(self, metric_value):
        """
        Build a table for summarizing the in-sample and out-of-sample performance results
        """
        summary_in_sample_performance = metric_value["in_sample_performance"]
        summary_out_of_sample_performance = metric_value["out_of_sample_performance"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_in_sample_performance,
                    metadata=ResultTableMetadata(title="In-Sample Performance Results"),
                ),
                ResultTable(
                    data=summary_out_of_sample_performance,
                    metadata=ResultTableMetadata(
                        title="Out-of-Sample Performance Results"
                    ),
                ),
            ]
        )
