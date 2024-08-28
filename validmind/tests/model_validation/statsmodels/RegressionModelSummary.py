# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

from .statsutils import adj_r2_score


@dataclass
class RegressionModelSummary(Metric):
    """
    Evaluates regression model performance using metrics including R-Squared, Adjusted R-Squared, MSE, and RMSE.

    ### Purpose

    The Regression Model Summary test evaluates the performance of regression models by measuring their predictive
    ability regarding dependent variables given changes in the independent variables. It uses conventional regression
    metrics such as R-Squared, Adjusted R-Squared, Mean Squared Error (MSE), and Root Mean Squared Error (RMSE) to
    assess the model's accuracy and fit.

    ### Test Mechanism

    This test employs the 'train_ds' attribute of the model to gather and analyze the training data. Initially, it
    fetches the independent variables and uses the model to make predictions on these given features. Subsequently, it
    calculates several standard regression performance metrics including R-Squared, Adjusted R-Squared, Mean Squared
    Error (MSE), and Root Mean Squared Error (RMSE), which quantify the approximation of the predicted responses to the
    actual responses.

    ### Signs of High Risk

    - Low R-Squared and Adjusted R-Squared values.
    - High MSE and RMSE values.

    ### Strengths

    - Offers an extensive evaluation of regression models by combining four key measures of model accuracy and fit.
    - Provides a comprehensive view of the model's performance.
    - Both the R-Squared and Adjusted R-Squared measures are readily interpretable.

    ### Limitations

    - Applicable exclusively to regression models.
    - RMSE and MSE might be sensitive to outliers.
    - A high R-Squared or Adjusted R-Squared may not necessarily indicate a good model, especially in cases of
    overfitting.
    """

    name = "regression_model_summary"
    required_inputs = ["model", "dataset"]
    tasks = ["regression"]
    tags = ["model_metadata", "model_comparison"]

    def run(self):
        X_columns = self.inputs.dataset.feature_columns

        y_true = self.inputs.dataset.y
        y_pred = self.inputs.dataset.y_pred(self.inputs.model)

        r2 = r2_score(y_true, y_pred)
        adj_r2 = adj_r2_score(y_true, y_pred, len(y_true), len(X_columns))
        mse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=True)
        rmse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False)

        results = {
            "Independent Variables": X_columns,
            "R-Squared": r2,
            "Adjusted R-Squared": adj_r2,
            "MSE": mse,
            "RMSE": rmse,
        }
        summary_regression = pd.DataFrame(results)

        return self.cache_results(
            {
                "regression_analysis": summary_regression.to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the regression analysis results
        """
        summary_regression = metric_value["regression_analysis"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_regression,
                    metadata=ResultTableMetadata(title="Regression Analysis Results"),
                ),
            ]
        )
