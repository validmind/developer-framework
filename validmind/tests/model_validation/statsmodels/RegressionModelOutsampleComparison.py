# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelOutsampleComparison(Metric):
    """
    Computes MSE and RMSE for multiple regression models using out-of-sample test to assess model's prediction accuracy
    on unseen data.

    **Purpose**: The RegressionModelOutsampleComparison test is designed to evaluate the predictive performance of
    multiple regression models by means of an out-of-sample test. The primary aim of this test is to validate the
    model's ability to generalize to unseen data, a common challenge in the context of overfitting. It does this by
    computing two critical metrics — Mean Squared Error (MSE) and Root Mean Squared Error (RMSE), which provide a
    quantifiable measure of the model's prediction accuracy on the testing dataset.

    **Test Mechanism**: This test requires multiple models (specifically Ordinary Least Squares - OLS regression
    models) and a test dataset as inputs. Each model generates predictions using the test dataset. The residuals are
    then calculated and used to compute the MSE and RMSE for each model. The test outcomes, which include the model's
    name, its MSE, and RMSE, are recorded and returned in a structured dataframe format.

    **Signs of High Risk**:
    - High values of MSE or RMSE indicate significant risk, signifying that the model's predictions considerably
    deviate from the actual values in the test dataset.
    - Consistently large discrepancies between training and testing performance across various models may indicate an
    issue with the input data itself or the model selection strategies employed.

    **Strengths**:
    - This test offers a comparative evaluation of multiple models' out-of-sample performance, enabling the selection
    of the best performing model.
    - The use of both MSE and RMSE provides insights into the model's prediction error. While MSE is sensitive to
    outliers, emphasizing larger errors, RMSE provides a more interpretable measure of average prediction error given
    that it's in the same unit as the dependent variable.

    **Limitations**:
    - The applicability of this test is limited to regression tasks, specifically OLS models.
    - The test operates under the assumption that the test dataset is a representative sample of the population. This
    might not always hold true and can result in less accurate insights.
    - The interpretability and the objectivity of the output (MSE and RMSE) can be influenced when the scale of the
    dependent variable varies significantly, or the distribution of residuals is heavily skewed or contains outliers.
    """

    name = "regression_outsample_performance"
    metadata = {
        "task_types": ["regression"],
        "tags": ["model_comparison"],
    }

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
            y_pred = fitted_model.predict(X_test)

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
