# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import GridSearchCV

from validmind.errors import SkipTestError
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class HyperParametersTuning(Metric):
    """
    Exerts exhaustive grid search to identify optimal hyperparameters for the model, improving performance.

    **Purpose:** The "HyperParametersTuning" metric being used here is intended to find the optimal set of
    hyperparameters for a given model. The test essentially aims to enhance the performance of the model under scrutiny
    by determining the best configuration of hyperparameters. The parameters that are being optimized are defined by
    the parameter grid that is passed to the metric.

    **Test Mechanism:** The HyperParametersTuning test employs a grid search mechanism using the function GridSearchCV
    from the scikit-learn library. The grid search algorithm is exhaustive: it systematically works through multiple
    combinations of the parameter tunes, cross-validated to determine which tune gives the best model performance. The
    chosen model and the parameters grid that are to be passed for tuning are the required inputs. Once the grid search
    is complete, the test caches and returns the details of the best model and its associated parameters.

    **Signs of High Risk:**
    - The test raises a SkipTestError if the param_grid is not supplied. This suggests that there are no specific
    parameters to optimize, which is a risk in certain model types that rely heavily on parameter tuning.
    - Poorly chosen scoring metrics that don't align well with the specific model or problem at hand might also reflect
    as a potential risk or failure in achieving the best performance.

    **Strengths:**
    - The test is a comprehensive exploratory mechanism that figures out the best set of hyperparameters for the
    supplied model, thereby helping improve its performance.
    - The implementation of GridSearchCV simplifies and automates the time-consuming task of hyperparameter tuning.

    **Limitations:**
    - The grid search algorithm can be computationally expensive, particularly with a large dataset or complex models.
    This grid search approach can be time-consuming as it tries out all possible combinations within the specified
    parameter grid.
    - The suitability of the tuning heavily relies on the quality of the data and it only accepts datasets with
    numerical or ordered categories.
    - The functionality assumes that the same set of hyperparameters is optimal for all problem sets, which may not
    hold true in every scenario.
    - There is a potential risk of overfitting the model if the training set is not representative of the data the
    model will be applied to.
    """

    name = "hyper_parameters_tuning"
    required_inputs = ["model", "dataset"]
    tasks = ["classification", "clustering"]
    tags = ["sklearn", "model_performance"]
    default_params = {"param_grid": None, "scoring": None}

    def run(self):
        param_grid = self.params["param_grid"]
        if param_grid is None:
            raise SkipTestError(
                "param_grid in dictnary format must be provide to run hyper parameter tuning"
            )
        model = self.inputs.model.model
        estimators = GridSearchCV(
            model, param_grid=param_grid, scoring=self.params["scoring"]
        )
        estimators.fit(self.inputs.dataset.x, self.inputs.dataset.y)

        results = [
            {
                "Best Model": f"{estimators.best_estimator_}",
                "Best Parameters": estimators.best_params_,
            }
        ]
        return self.cache_results(
            {
                "parameters_tuning": pd.DataFrame(results).to_dict(orient="records"),
            }
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the hyper parameters tunning
        """
        summary_regression = metric_value["parameters_tuning"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_regression,
                    metadata=ResultTableMetadata(
                        title="Hyper Parameters Tuning Results"
                    ),
                ),
            ]
        )
