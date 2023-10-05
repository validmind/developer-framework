# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

from .statsutils import adj_r2_score


@dataclass
class RegressionModelInsampleComparison(Metric):
    """
    Evaluates and compares in-sample performance of multiple regression models using R-Squared, Adjusted R-Squared,
    MSE, and RMSE.

    **Purpose**: The RegressionModelInsampleComparison test metric is utilized to evaluate and compare the performance
    of multiple regression models trained on the same dataset. Key performance indicators for this comparison include
    statistics related to the goodness of fit - R-Squared, Adjusted R-Squared, Mean Squared Error (MSE), and Root Mean
    Squared Error (RMSE).

    **Test Mechanism**: The methodology behind this test is as follows -
    - Firstly, a verification that the list of models to be tested is indeed not empty occurs.
    - Once confirmed, the In-Sample performance of the models is calculated by a private function,
    `_in_sample_performance_ols`, that executes the following steps:
      - Iterates through each model in the supplied list.
      - For each model, the function extracts the features (`X`) and the target (`y_true`) from the training dataset
    and computes the predicted target values (`y_pred`).
      - The performance metrics for the model are calculated using formulas for R-Squared, Adjusted R-Squared, MSE, and
    RMSE.
      - The results, including the computed metrics, variables of the model, and the model's identifier, are stored in
    a dictionary that is appended to a list.
    - The collected results are finally returned as a pandas dataframe.

    **Signs of High Risk**:
    - Significantly low values for R-Squared or Adjusted R-Squared.
    - Significantly high values for MSE and RMSE.
    Please note that what constitutes as "low" or "high" will vary based on the specific context or domain in which the
    model is being utilized.

    **Strengths**:
    - Enables comparison of in-sample performance across different models on the same dataset, providing insights into
    which model fits the data the best.
    - Utilizes multiple evaluation methods (R-Squared, Adjusted R-Squared, MSE, RMSE), offering a comprehensive review
    of a model's performance.

    **Limitations**:
    - The test measures only in-sample performance, i.e., how well a model fits the data it was trained on. However, it
    does not give any information on the performance of the model on new, unseen, or out-of-sample data.
    - Higher in-sample performance might be a result of overfitting, where the model is just memorizing the training
    data. This test is sensitive to such cases.
    - The test does not consider additional key factors such as the temporal dynamics of the data, that is, the pattern
    of changes in data over time.
    - The test does not provide an automated mechanism to determine if the reported metrics are within acceptable
    ranges, necessitating human judgment.
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
