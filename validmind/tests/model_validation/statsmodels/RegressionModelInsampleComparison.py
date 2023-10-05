# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

from .statsutils import adj_r2_score


@dataclass
class RegressionModelInsampleComparison(Metric):
    """
    **Purpose**: The purpose of this test metric, RegressionModelInsampleComparison, is to assess the performance of
    regression models on the same dataset that they were trained on. The performance of the models is compared against
    each other to identify which fits the data best. Evaluation metrics include goodness-of-fit statistics such as
    R-Squared, Adjusted R-Squared, Mean Squared Error (MSE) and Root Mean Squared Error (RMSE).

    **Test Mechanism**: The test's implementation involves the following steps;
    - First, a check is done to ensure that the list of models is not empty.
    - After confirmation, the In-Sample performance of the models is computed by using a private function
    `_in_sample_performance_ols`. This function:
      - Loops through each model in the list
      - For each model, it extracts the features (`X`) and target (`y_true`) from the training dataset and then
    predicts target values (`y_pred`)
      - The model's performance metrics are then computed using formulas for R-Squared, Adjusted R-Squared, MSE and
    RMSE.
      - The computed metrics, variables of the model and the model's identifier are saved in a dictionary and appended
    to a list.
    - The collected results are then saved and returned in form of a pandas dataframe.

    **Signs of High Risk**: A high risk or failure of the model's performance can be indicated by waiting significantly
    low values for R-Squared or Adjusted R-Squared and significantly high values for MSE and RMSE. The exact thresholds
    may vary based on the specific context or domain in which the model is being applied.

    **Strengths**:
    - Enables direct comparison of different models' in-sample performance on the same data set, providing a clear
    picture of which model is better suited to the data.
    - It computes multiple evaluation methods (R-Squared, Adjusted R-Squared, MSE, RMSE), which provides a
    comprehensive overview of the model's performance.

    **Limitations**:
    - This test only uses in-sample performance, i.e., how well a model fits the data it was trained on. It might not
    indicate how the model performs on unseen or out-of-sample data, which is a core aspect of modeling tasks.
    - It might be sensitive to overfitting as better in-sample performance might be a result of the model merely
    memorizing the training data.
    - It does not take into account other crucial factors like data's pattern of changes over time, also known as
    temporal dynamics.
    - The test doesn't offer a mechanism to automatically determine whether reported metrics are acceptable -
    human/judgement-based interpretation is needed.
    """

    name = "regression_insample_performance"
    metadata = {
        "task_types": ["regression"],
        "tags": ["model_comparison"],
    }

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")
        all_models = []

        if self.models is not None:
            all_models.extend(self.models)

        in_sample_performance = self._in_sample_performance_ols(all_models)
        in_sample_performance_df = pd.DataFrame(in_sample_performance)

        return self.cache_results(
            {
                "in_sample_performance": in_sample_performance_df.to_dict(
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
            X = model.train_ds.x
            y_true = model.train_ds.y
            y_pred = model.predict(X)

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
