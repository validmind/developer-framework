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

    ### Purpose:

    The "HyperParametersTuning" metric aims to find the optimal set of hyperparameters for a given model. The test is
    designed to enhance the performance of the model by determining the best configuration of hyperparameters. The
    parameters that are being optimized are defined by the parameter grid provided to the metric.

    ### Test Mechanism:

    The HyperParametersTuning test employs a grid search mechanism using the GridSearchCV function from the
    scikit-learn library. The grid search algorithm systematically works through multiple combinations of parameter
    values, cross-validating to determine which combination gives the best model performance. The chosen model and the
    parameter grid passed for tuning are necessary inputs. Once the grid search is complete, the test caches and
    returns details of the best model and its associated parameters.

    ### Signs of High Risk:

    - The test raises a SkipTestError if the param_grid is not supplied, indicating a lack of specific parameters to
    optimize, which can be risky for certain model types reliant on parameter tuning.
    - Poorly chosen scoring metrics that do not align well with the specific model or problem at hand could reflect
    potential risks or failures in achieving optimal performance.

    ### Strengths:

    - Provides a comprehensive exploration mechanism to identify the best set of hyperparameters for the supplied
    model, thereby enhancing its performance.
    - Implements GridSearchCV, simplifying and automating the time-consuming task of hyperparameter tuning.

    ### Limitations:

    - The grid search algorithm can be computationally expensive, especially with large datasets or complex models, and
    can be time-consuming as it tests all possible combinations within the specified parameter grid.
    - The effectiveness of the tuning is heavily dependent on the quality of data and only accepts datasets with
    numerical or ordered categories.
    - Assumes that the same set of hyperparameters is optimal for all problem sets, which may not be true in every
    scenario.
    - There's a potential risk of overfitting the model if the training set is not representative of the data that the
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
                "param_grid in dictonary format must be provided to run this test"
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
