# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import re
from dataclasses import dataclass

import numpy as np
from sklearn import metrics

from validmind.errors import SkipTestError
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelsPerformanceComparison(Metric):
    """
    Compares and evaluates the performance of multiple regression models using five different metrics: MAE, MSE, RMSE,
    MAPE, and MBD.

    **1. Purpose:**
    The Regression Models Performance Comparison metric is used to measure and compare the performance of regression
    models. It calculates multiple evaluation metrics, including Mean Absolute Error (MAE), Mean Squared Error (MSE),
    Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), and Mean Bias Deviation (MBD), thereby
    enabling a comprehensive view of model performance.

    **2. Test Mechanism:**
    The test starts by sourcing the true and predicted values from the models. It then computes the MAE, MSE, RMSE,
    MAPE, and MBD. These calculations encapsulate both the direction and the magnitude of error in predictions, thereby
    providing a multi-faceted view of model accuracy. It captures these results in a dictionary and compares the
    performance of all models using these metrics. The results are then appended to a table for presenting a
    comparative summary.

    **3. Signs of High Risk:**

    - High values of MAE, MSE, RMSE, and MAPE, which indicate a high error rate and imply a larger departure of the
    model's predictions from the true values.
    - A large value of MBD, which shows a consistent bias in the model’s predictions.
    - If the test returns an error citing that no models were provided for comparison, it implies a risk in the
    evaluation process itself.

    **4. Strengths:**

    - The metric evaluates models on five different metrics offering a comprehensive analysis of model performance.
    - It compares multiple models simultaneously, aiding in the selection of the best-performing models.
    - It is designed to handle regression tasks and can be seamlessly integrated with libraries like sklearn.

    **5. Limitations:**

    - The metric only evaluates regression models and does not evaluate classification models.
    - The test assumes that the models have been trained and tested appropriately prior to evaluation. It does not
    handle pre-processing, feature selection, or other stages in the model lifecycle.
    - It may fail to run if it doesn't receive valid models as inputs. The models are passed externally and the test
    doesn't have an internal mechanism to verify their validity.
    - The test could exhibit performance limitations if a large number of models is input for comparison.
    """

    name = "models_performance_comparison"
    required_inputs = ["model", "dataset"]

    metadata = {
        "task_types": ["regression"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }

    def regression_errors(self, y_true_test, y_pred_test):
        mae_test = metrics.mean_absolute_error(y_true_test, y_pred_test)

        results = {}
        results["Mean Absolute Error (MAE)"] = mae_test

        mse_test = metrics.mean_squared_error(y_true_test, y_pred_test)
        results["Mean Squared Error (MSE)"] = mse_test
        results["Root Mean Squared Error (RMSE)"] = np.sqrt(mse_test)

        mape_test = np.mean(np.abs((y_true_test - y_pred_test) / y_true_test)) * 100
        results["Mean Absolute Percentage Error (MAPE)"] = mape_test

        mbd_test = np.mean(y_pred_test - y_true_test)
        results["Mean Bias Deviation (MBD)"] = mbd_test

        return results

    def summary(self, metric_value: dict):
        """
        This summary varies depending if we're evaluating a binary or multi-class model
        """
        results = []
        metrics = metric_value["model_0"].keys()
        error_table = []
        for metric_name in metrics:
            errors_dict = {}
            errors_dict["Errors"] = metric_name
            for m, m_v in metric_value.items():
                for metric in metrics:
                    res = re.findall(r"\(.*?\)", metric)
                    res[0][1:-1]
                    errors_dict[f"{res[0][1:-1]}-{m}"] = metric_value[m][metric]
            error_table.append(errors_dict)

        results.append(
            ResultTable(
                data=error_table,
                metadata=ResultTableMetadata(title="Regression Errors Comparison"),
            )
        )

        return ResultSummary(results=results)

    def run(self):
        # Check models list is not empty
        if not self.inputs.models:
            raise SkipTestError(
                "List of models must be provided as a `models` parameter to compare performance"
            )

        all_models = [self.inputs.model]

        if self.inputs.models is not None:
            all_models.extend(self.inputs.models)
        results = {}

        for idx, model in enumerate(all_models):
            result = self.regression_errors(
                y_true_test=self.inputs.dataset.y,
                y_pred_test=self.inputs.dataset.y_pred(model.input_id),
            )
            results["model_" + str(idx)] = result
        return self.cache_results(results)
