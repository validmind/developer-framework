# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from sklearn import metrics

from validmind.tests.model_validation.statsmodels.statsutils import adj_r2_score
from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class RegressionR2Square(Metric):

    category = "model_performance"
    name = "regression_errors"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["regression"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }

    def summary(self, raw_results):

        """
        Returns a summarized representation of the dataset split information
        """
        table_records = []
        for result in raw_results:
            for key, value in result.items():
                table_records.append(
                    {
                        "Metric": key,
                        "TRAIN": result[key]["train"],
                        "TEST": result[key]["test"],
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def run(self):
        y_true_train = self.model.y_train_true
        class_pred_train = self.model.y_train_predict
        y_true_train = y_true_train.astype(class_pred_train.dtype)

        y_true_test = self.model.y_test_true
        class_pred_test = self.model.y_test_predict
        y_true_test = y_true_test.astype(class_pred_test.dtype)

        r2s_train = metrics.r2_score(y_true_train, class_pred_train)
        r2s_test = metrics.r2_score(y_true_test, class_pred_test)

        results = []
        results.append(
            {
                "R-squared (R2) Score": {
                    "train": r2s_train,
                    "test": r2s_test,
                }
            }
        )

        X_columns = self.model.train_ds.get_features_columns()
        adj_r2_train = adj_r2_score(
            y_true_train, class_pred_train, len(y_true_train), len(X_columns)
        )
        adj_r2_test = adj_r2_score(
            y_true_test, class_pred_test, len(y_true_test), len(X_columns)
        )
        results.append(
            {
                "Adjusted R-squared (R2) Score": {
                    "train": adj_r2_train,
                    "test": adj_r2_test,
                }
            }
        )
        return self.cache_results(metric_value=results)
