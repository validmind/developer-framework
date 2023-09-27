# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class RegressionModelOutsampleComparison(Metric):
    """
    **Purpose**: The RegressionModelOutsampleComparison test is designed to evaluate the predictive performance of
    multiple regression models by means of an out-of-sample test. Crucially, the aim of this test is to validate the
    model's ability to generalize to unseen data, a need that arises from the challenge of overfitting. Two key
    metrics, Mean Squared Error (MSE) and Root Mean Squared Error (RMSE), are computed for this purpose to provide a
    quantifiable measure of the model's accuracy on the testing dataset.

    **Test Mechanism**: To perform this test, multiple models (in the form of Ordinary Least Squares, or OLS regression
    models) and a test dataset are required as inputs. For each model, predictions are made on the test dataset,
    following which, the residuals are calculated. These residuals are then used to compute the MSE and RMSE for each
    model. The outcomes of the test, including the model's descriptive name, its MSE, and RMSE, are stored and
    outputted in a structured dataframe format.

    **Signs of High Risk**: High values of MSE or RMSE indicate elevated risk, signifying that the model's predictions
    significantly deviate from the actual values in the test dataset. Furthermore, persistently significant
    discrepancies between training and testing performance across various models might suggest an issue with the input
    data or with the model selection strategies.

    **Strengths**: This test effectively provides a comparative evaluation of multiple models' out-of-sample
    performance, enabling the identification of the best performing model. Moreover, by leveraging both MSE and RMSE,
    one can gain insights about the model's prediction error. While MSE is sensitive to outliers, emphasising larger
    errors, RMSE (being in the same unit as the dependent variable) provides a more interpretable measurement of
    average prediction error.

    **Limitations**: While this test provides valuable insights about model generalization, its applicability is
    constrained to regression tasks, and specifically OLS models. Furthermore, it assumes that the test dataset is a
    representative sample of the population that the built model is intended to be generalized to, which might not
    always be the case. Lastly, the RMSE and MSE might be less meaningful when the dependent variable scale varies
    significantly, or the residuals' distribution is heavily skewed or contains outliers.
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
