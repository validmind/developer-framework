# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from sklearn.metrics import mean_squared_error, r2_score

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelsPerformance(Metric):
    """
    Evaluates and compares regression models' performance using R-squared, Adjusted R-squared, and MSE metrics.

    **Purpose**: This metric is used to evaluate and compare the performance of various regression models. Through the
    use of key statistical measures such as R-squared, Adjusted R-squared, and Mean Squared Error (MSE), the
    performance of different models in predicting dependent variables can be assessed both on the data used for
    training (in-sample) and new, unseen data (out-of-sample).

    **Test Mechanism**: The test evaluates a list of provided regression models. For each model, it calculates their
    in-sample and out-of-sample performance by deriving the model predictions for the training and testing datasets
    respectively, and then comparing these predictions to the actual values. In doing so, it calculates R-squared,
    Adjusted R-squared, and MSE for each model, stores the results, and returns them for comparison.

    **Signs of High Risk**:
    - High Mean Squared Error (MSE) values.
    - Strikingly low values of R-squared and Adjusted R-squared.
    - A significant drop in performance when transitioning from in-sample to out-of-sample evaluations, signaling a
    potential overfitting issue.

    **Strengths**:
    - The test permits comparisons of multiple models simultaneously, providing an objective base for identifying the
    top-performing model.
    - It delivers both in-sample and out-of-sample evaluations, presenting performance data on unseen data.
    - The utilization of R-squared and Adjusted R-squared in conjunction with MSE allows for a detailed view of the
    model's explainability and error rate.

    **Limitations**:
    - This test is built around the assumption that the residuals of the regression model are normally distributed,
    which is a fundamental requirement for Ordinary Least Squares (OLS) regression; thus, it could be not suitable for
    models where this assumption is broken.
    - The test does not consider cases where higher R-squared or lower MSE values do not necessarily correlate with
    better predictive performance, particularly in instances of excessively complex models.
    """

    name = "regression_models_performance"
    metadata = {
        "task_types": ["regression"],
        "tags": ["model_performance", "model_comparison"],
    }

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []

        if self.models is not None:
            all_models.extend(self.models)

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
            # R models will not predict the same number of rows as the test dataset
            y_pred = model.predict(model.train_ds.x)[0 : len(y_true)]

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
            # R models will not predict the same number of rows as the test dataset
            y_pred = model.predict(model.test_ds.x)[0 : len(y_true)]

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
