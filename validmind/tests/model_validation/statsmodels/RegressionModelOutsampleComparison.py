# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.vm_models import (
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


@dataclass
class RegressionModelOutsampleComparison(Metric):
    """
    Test that evaluates the performance of different regression models on a separate test dataset
    that was not used to train the models.
    """

    name = "regression_outsample_performance"

    def description(self):
        return """
        This section shows Out-of-sample comparison of regression models involves evaluating
        the performance of different regression models on a separate test dataset that was not
        used to train the models. This is typically done by calculating a goodness-of-fit statistic
        such as the R-squared or mean squared error (MSE) for each model, and then comparing these
        statistics to determine which model has the best fit to the test data.
        """

    def run(self):
        # Check models list is not empty
        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")
        all_models = []
        if self.model is not None:
            all_models.append(self.model)

        if self.models is not None:
            all_models.extend(self.models)

        for model in all_models:
            if not Model.is_supported_model(model.model):
                raise ValueError(
                    f"{Model.model_library(model.model)}.{Model.model_class(model.model)} \
                                is not supported by ValidMind framework yet"
                )
            if model.test_ds is None:
                raise ValueError(
                    "Test dataset is missing in the ValidMind Model object"
                )

        results = self._out_sample_performance_ols(
            all_models,
        )
        return self.cache_results(
            {
                "out_sample_performance": results.to_dict(orient="records"),
            }
        )

    def _out_sample_performance_ols(self, model_list):
        """
        Returns the out-of-sample performance evaluation metrics of a list of OLS regression models.
        Args:
        model_list (list): A list of OLS models to evaluate.
        test_data (pandas.DataFrame): The test dataset containing the independent and dependent variables.
        target_col (str): The name of the target variable column in the test dataset.
        Returns:
        pandas.DataFrame: A DataFrame containing the evaluation results of the OLS models. The columns are 'Model',
        'MSE' (Mean Squared Error), and 'RMSE' (Root Mean Squared Error).
        """

        # Initialize a list to store results
        results = []

        for fitted_model in model_list:
            # Extract the column names of the independent variables from the model
            independent_vars = fitted_model.train_ds.get_features_columns()

            # Separate the target variable and features in the test dataset
            X_test = fitted_model.test_ds.x
            y_test = fitted_model.test_ds.y

            # Predict the test data
            y_pred = fitted_model.model.predict(X_test)

            # Calculate the residuals
            residuals = y_test - y_pred

            # Calculate the mean squared error and root mean squared error
            mse = np.mean(residuals**2)
            rmse_val = np.sqrt(mse)

            # Store the results
            model_name_with_vars = f"({', '.join(independent_vars)})"
            results.append(
                {
                    "Model": model_name_with_vars,
                    "MSE": mse,
                    "RMSE": rmse_val,
                }
            )

        # Create a DataFrame to display the results
        results_df = pd.DataFrame(results)

        return results_df

    def summary(self, metric_value):
        """
        Build one table for summarizing the out-of-sample performance results
        """
        summary_out_sample_performance = metric_value["out_sample_performance"]

        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_out_sample_performance,
                    metadata=ResultTableMetadata(
                        title="Out-of-Sample Performance Results"
                    ),
                ),
            ]
        )
