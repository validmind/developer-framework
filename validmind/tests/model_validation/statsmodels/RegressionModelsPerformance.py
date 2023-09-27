# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from sklearn.metrics import mean_squared_error, r2_score

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelsPerformance(Metric):
    """
    **Purpose**: This metric is intended to assess and compare the performance of different regression models. It
    offers an insightful look into the models' ability to predict dependent variables, both on the data used for
    training (in-sample) and new data (out-of-sample). Metrics such as R-squared, Adjusted R-squared, and Mean Squared
    Error (MSE) are employed.

    **Test Mechanism**: This test iterates over various regression models supplied as an input list. For each model, it
    evaluates their in-sample and out-of-sample performance by capturing predictions for the training and test datasets
    respectively, and comparing these predictions against actual values to calculate R-squared, Adjusted R-squared, and
    Mean Squared Error (MSE). The models are individually evaluated in this manner, with their results being stored and
    returned for comparison purposes.

    **Signs of High Risk**: High risk or potential failures in the model's performance might be indicated by
    excessively large MSE values, or unreasonably low R-squared and Adjusted R-squared values. If the model's
    performance drastically declines when moving from in-sample to out-of-sample evaluations, this could also signify a
    high risk of overfitting.

    **Strengths**: This metric is versatile and allows for the comparison of multiple models at once, providing an
    objective means of identifying the best-performing model. It provides both in-sample and out-of-sample evaluations,
    thus informing about the model's performance on unseen data. The use of R-squared and Adjusted R-squared values in
    addition to MSE provides a comprehensive view of the model's explainability and error rate.

    **Limitations**: This test presupposes that the regression model's residuals are normally distributed, *i.e.*, a
    key assumption of Ordinary Least Squares (OLS) regression. Thus, it may not appropriately assess models where this
    assumption is violated. Additionally, it does not account for situations where predictive performance might not
    directly correlate with higher R-squared or lower MSE values, especially in the event of excessively complex models.
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
