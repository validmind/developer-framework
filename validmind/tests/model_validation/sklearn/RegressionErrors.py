# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
from sklearn import metrics

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class RegressionErrors(Metric):

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

        mae_train = metrics.mean_absolute_error(y_true_train, class_pred_train)
        mae_test = metrics.mean_absolute_error(y_true_test, class_pred_test)

        results = []
        results.append(
            {
                "Mean Absolute Error (MAE)": {
                    "train": mae_train,
                    "test": mae_test,
                }
            }
        )

        mse_train = metrics.mean_squared_error(y_true_train, class_pred_train)
        mse_test = metrics.mean_squared_error(y_true_test, class_pred_test)
        results.append(
            {
                "Mean Squared Error (MSE)": {
                    "train": mse_train,
                    "test": mse_test,
                }
            }
        )
        results.append(
            {
                "Root Mean Squared Error (RMSE)": {
                    "train": np.sqrt(mse_train),
                    "test": np.sqrt(mse_test),
                }
            }
        )

        mape_train = (
            np.mean(np.abs((y_true_train - class_pred_train) / y_true_train)) * 100
        )
        mape_test = np.mean(np.abs((y_true_test - class_pred_test) / y_true_test)) * 100
        results.append(
            {
                "Mean Absolute Percentage Error (MAPE)": {
                    "train": mape_train,
                    "test": mape_test,
                }
            }
        )

        mbd_train = np.mean(class_pred_train - y_true_train)
        mbd_test = np.mean(class_pred_test - y_true_test)
        results.append(
            {
                "Mean Bias Deviation (MBD)": {
                    "train": mbd_train,
                    "test": mbd_test,
                }
            }
        )

        return self.cache_results(metric_value=results)
