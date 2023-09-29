# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata

from .statsutils import adj_r2_score


@dataclass
class RegressionModelSummary(Metric):
    """
    **Purpose**: This metric test evaluates the performance of regression models, specifically capturing their ability
    to predict the dependent variable(s) given changes in the independent variable(s). It measures the quality of the
    model using classic regression metrics such as R-Squared, Adjusted R-Squared, Mean Squared Error (MSE), and Root
    Mean Squared Error (RMSE).

    **Test Mechanism**: This test utilizes the 'train_ds' attribute of the model to collect and assess the training
    data. It first retrieves the independent variables and uses the model to predict on the given features. The test
    calculates several standard regression performance metrics including R-Square, Adjusted R-Squared, Mean Squared
    Error (MSE), and Root Mean Squared Error (RMSE). These metrics quantify how close the predicted responses are to
    the true responses.

    **Signs of High Risk**: High risk or potentially problematic model performance could be indicated by low R-Squared
    and Adjusted R-Squared values, or high MSE and RMSE values. Low R-squared and adjusted R-squared values suggest a
    poor fit between the model predictions and the true responses, indicating the model explains a small portion of the
    variance in the target variable. High MSE or RMSE represents a high prediction error, which points to poor model
    performance.

    **Strengths**: This test offers an extensive evaluation of regression models as it combines four key measures of
    model accuracy and fit, offering a comprehensive view of the model's performance. Furthermore, both the R-Squared
    and the Adjusted R-Squared measures are readily interpretable, representing the proportion of total variation in
    the dependent variable that is explained by the independent variables.

    **Limitations**: This test only applies to regression models and cannot be used to evaluate binary classification
    models or time series models, limiting its scope. Furthermore, while RMSE and MSE are good measures of prediction
    error, they can be sensitive to outliers, which might lead to an overestimation of the model's prediction error.
    Lastly, high R-squared or adjusted R-squared doesn't necessarily imply a good model, especially in cases where the
    model is overfitting the data.
    """

    name = "regression_model_summary"
    metadata = {
        "task_types": ["regression"],
        "tags": ["model_metadata", "model_comparison"],
    }

    def run(self):
        X_columns = self.model.train_ds.get_features_columns()

        y_true = self.model.train_ds.y
        y_pred = self.model.predict(self.model.train_ds.x)

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
