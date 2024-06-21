# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
from sklearn import metrics

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class RegressionErrors(Metric):
    """
    **Purpose**: This metric is used to measure the performance of a regression model. It gauges the model's accuracy
    by computing several error metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared
    Error (RMSE), Mean Absolute Percentage Error (MAPE), and Mean Bias Deviation (MBD) on both the training and testing
    dataset.

    **Test Mechanism**: The test computes each of the aforementioned metrics. MAE calculates the average of the
    absolute difference between the true value and the predicted value. MSE squares the difference before averaging it.
    RMSE then takes the square root of the MSE. MAPE evaluates the average of the absolute difference between true and
    predicted values divided by the true value, expressed as a percentage. Lastly, MBD is a measure of average bias in
    the prediction. The results are compared between the training dataset and the testing dataset.

    **Signs of High Risk**: High values for any of the metrics, or particularly different metric outcomes for the
    training set versus the test set, are signs of high risk. Specifically, high MAE, MSE, RMSE, or MAPE values could
    indicate poor model performance and overfitting. If MBD is significantly different from zero, it could signify that
    the model's predictions are systematically biased.

    **Strengths**: These metrics collectively provide a comprehensive view of model performance and error distribution.
    Individually, MAE provides a linear score that could be more interpretable, while MSE gives more weight to larger
    errors. RMSE is useful because it is in the same unit as the target variable. MAPE expresses error as a percentage,
    making it a good measure of prediction accuracy. MBD helps to detect systematic bias in predictions.

    **Limitations**: Each of these metrics has its own limitations. MAE and MSE are sensitive to outliers. While RMSE
    is good for giving high weight to larger errors, it might too heavily penalize these errors. MAPE might be biased
    if actual values are near zero, and MBD would not work well if the difference between predictions and actual values
    changes with the magnitude of the actual values. Overall, these metrics will not capture all model performance
    nuances, and they should be used with contextual understanding of the problem at hand.
    """

    name = "regression_errors"
    required_inputs = ["model", "datasets"]
    tasks = ["regression"]
    tags = [
        "sklearn",
        "model_performance",
    ]

    def summary(self, raw_results):
        """
        Returns a summarized representation of the dataset split information
        """
        table_records = []
        for result in raw_results:
            for key, _ in result.items():
                table_records.append(
                    {
                        "Metric": key,
                        "TRAIN": result[key]["train"],
                        "TEST": result[key]["test"],
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def regression_errors(
        self, y_true_train, class_pred_train, y_true_test, class_pred_test
    ):
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
        return results

    def run(self):
        y_train_true = self.inputs.datasets[0].y
        y_train_pred = self.inputs.datasets[0].y_pred(self.inputs.model)
        y_train_true = y_train_true.astype(y_train_pred.dtype)

        y_test_true = self.inputs.datasets[1].y
        y_test_pred = self.inputs.datasets[1].y_pred(self.inputs.model)
        y_test_true = y_test_true.astype(y_test_pred.dtype)

        results = self.regression_errors(
            y_train_true, y_train_pred, y_test_true, y_test_pred
        )

        return self.cache_results(metric_value=results)
