# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
from sklearn import metrics

from validmind.vm_models import Metric


@dataclass
class RegressionErrors(Metric):
    """
    Assesses the performance and error distribution of a regression model using various error metrics.

    ### Purpose

    The purpose of the Regression Errors test is to measure the performance of a regression model by calculating
    several error metrics. This evaluation helps determine the model's accuracy and potential issues like overfitting
    or bias by analyzing differences in error metrics between the training and testing datasets.

    ### Test Mechanism

    The test computes the following error metrics:
    - **Mean Absolute Error (MAE)**: Average of the absolute differences between true values and predicted values.
    - **Mean Squared Error (MSE)**: Average of the squared differences between true values and predicted values.
    - **Root Mean Squared Error (RMSE)**: Square root of the mean squared error.
    - **Mean Absolute Percentage Error (MAPE)**: Average of the absolute differences between true values and predicted
    values, divided by the true values, and expressed as a percentage.
    - **Mean Bias Deviation (MBD)**: Average bias between true values and predicted values.

    These metrics are calculated separately for the training and testing datasets and compared to identify
    discrepancies.

    ### Signs of High Risk

    - High values for MAE, MSE, RMSE, or MAPE indicating poor model performance.
    - Large differences in error metrics between the training and testing datasets, suggesting overfitting.
    - Significant deviation of MBD from zero, indicating systematic bias in model predictions.

    ### Strengths

    - Provides a comprehensive overview of model performance through multiple error metrics.
    - Individual metrics offer specific insights, e.g., MAE for interpretability, MSE for emphasizing larger errors.
    - RMSE is useful for being in the same unit as the target variable.
    - MAPE allows the error to be expressed as a percentage.
    - MBD detects systematic bias in model predictions.

    ### Limitations

    - MAE and MSE are sensitive to outliers.
    - RMSE heavily penalizes larger errors, which might not always be desirable.
    - MAPE can be misleading when actual values are near zero.
    - MBD may not be suitable if bias varies with the magnitude of actual values.
    - These metrics may not capture all nuances of model performance and should be interpreted with domain-specific
    context.
    """

    name = "regression_errors"
    required_inputs = ["model", "dataset"]
    tasks = ["regression"]
    tags = [
        "sklearn",
        "model_performance",
    ]

    def regression_errors(self, y_true_train, class_pred_train):
        mae_train = metrics.mean_absolute_error(y_true_train, class_pred_train)

        results = []
        results.append({"Mean Absolute Error (MAE)": mae_train})

        mse_train = metrics.mean_squared_error(y_true_train, class_pred_train)
        results.append({"Mean Squared Error (MSE)": mse_train})
        results.append({"Root Mean Squared Error (RMSE)": np.sqrt(mse_train)})

        mape_train = (
            np.mean(np.abs((y_true_train - class_pred_train) / y_true_train)) * 100
        )
        results.append({"Mean Absolute Percentage Error (MAPE)": mape_train})

        mbd_train = np.mean(class_pred_train - y_true_train)
        results.append({"Mean Bias Deviation (MBD)": mbd_train})
        return results

    def run(self):
        y_train_true = self.inputs.dataset.y
        y_train_pred = self.inputs.dataset.y_pred(self.inputs.model)
        y_train_true = y_train_true.astype(y_train_pred.dtype)

        results = self.regression_errors(y_train_true, y_train_pred)

        return self.cache_results(metric_value=results)
