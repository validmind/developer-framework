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
class RegressionModelSummary(Metric):
    """
    Test that output the summary of regression models of statsmodel library.
    """

    name = "regression_model_summary"

    def run(self):
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                              is not supported by ValidMind framework yet"
            )

        X_columns = self.model.train_ds.get_features_columns()

        y_true = self.model.train_ds.y
        y_pred = self.model.model.predict(self.model.train_ds.x)

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
