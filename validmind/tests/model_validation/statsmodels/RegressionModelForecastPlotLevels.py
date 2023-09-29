# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from validmind.vm_models import Figure, Metric


@dataclass
class RegressionModelForecastPlotLevels(Metric):
    """
    **Purpose:**
    The purpose of `RegressionModelForecastPlotLevels` is to visually evaluate the performance of a given list of
    regression models. It does this by plotting the forecasts of these models against the observed data in their
    training and test datasets. It evaluates the model's ability to produce accurate and reliable forecasts when faced
    with certain input features. The measure of accuracy here is the proximity of the forecasted values to the actual
    observed values. In case of any transformations specified, the metric also handles transforming the data before the
    comparison.

    **Test Mechanism:**
    The Python class in consideration accepts `transformation` as a parameter, which defaults to None. First, it checks
    for the presence of model objects and raises a `ValueError` if none are provided. Next, it loops through each
    model, generating predictive forecasts for the model's training and testing datasets. These forecasts are then
    plotted against the actual (observed) values. If a transformation, such as "integrate", is specified, the class
    carries out the transformation operation (i.e., it performs cumulative sums to create a new series). Finally, plots
    are created comparing observed and forecasted values for both the original and transformed datasets.

    **Signs of High Risk:**
    High risk or failure in the model's performance can be inferred from the generated plots. If the forecasted values
    deviate significantly from the observed values in either the training or test datasets, it suggests high risk. A
    significant deviation could be a sign of overfitting or underfitting, which would be a cause for concern. Such
    discrepancies could limit the model's ability to produce accurate and generalizable results.

    **Strengths:**
    - Visual evaluation: The metric provides a graphical way of evaluating the regression models, allowing easier
    interpretation and assessment of the forecasting accuracy.
    - Handles multiple models: The metric enables evaluation of multiple models at once, providing a comparative
    overview of all models.
    - Handles transformations: Ability to handle transformations such as "integrate" allows for broader scope and
    flexibility in model evaluations.
    - Detailed insight: The metric provides a detailed perspective by looking at the performance on both training and
    testing datasets.

    **Limitations:**
    - Visual subjectivity: The metric relies heavily on visual evaluations, and interpretation can vary from person to
    person.
    - Limitation in transformations: Currently supports "integrate" transformation only. More complex transformation
    might not be covered.
    - Overhead: Plotting for large datasets might be computationally expensive and could increase runtime.
    - Lack of numerical metrics: While visualization is useful, a corresponding numerical measure to support
    observations would be beneficial.
    """

    name = "regression_forecast_plot_levels"
    default_params = {
        "transformation": None,
    }
    metadata = {
        "task_types": ["regression"],
        "tags": ["forecasting", "visualization"],
    }

    def run(self):
        transformation = self.params["transformation"]

        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        for model in self.models:
            all_models.append(model)

        figures = self._plot_forecast(all_models, transformation)

        return self.cache_results(figures=figures)

    def integrate_diff(self, series_diff, start_value):
        series_diff = np.array(series_diff)
        series_orig = np.cumsum(series_diff)
        series_orig += start_value
        return series_orig

    def _plot_forecast(
        self,
        model_list,
        transformation=None,
    ):
        figures = []

        for i, fitted_model in enumerate(model_list):
            feature_columns = fitted_model.train_ds.get_features_columns()
            train_ds = fitted_model.train_ds
            test_ds = fitted_model.test_ds

            y_pred = fitted_model.predict(fitted_model.train_ds.x)
            y_pred_test = fitted_model.predict(fitted_model.test_ds.x)

            all_dates = pd.concat([pd.Series(train_ds.index), pd.Series(test_ds.index)])

            if all_dates.empty:
                raise ValueError(
                    "No dates in the data. Unable to determine start and end dates."
                )

            fig, axs = plt.subplots(2, 2)

            # train vs forecast
            axs[0, 0].plot(
                train_ds.index, train_ds.y, label="Train Dataset", color="grey"
            )
            axs[0, 0].plot(train_ds.index, y_pred, label="Train Forecast")
            axs[0, 0].set_title(f"Forecast vs Observed for features {feature_columns}")
            axs[0, 0].legend()

            # test vs forecast
            axs[0, 1].plot(test_ds.index, test_ds.y, label="Test Dataset", color="grey")
            axs[0, 1].plot(test_ds.index, y_pred_test, label="Test Forecast")
            axs[0, 1].set_title(f"Forecast vs Observed for features {feature_columns}")
            axs[0, 1].legend()

            if transformation == "integrate":
                train_ds_y_transformed = self.integrate_diff(
                    train_ds.y_df().values, start_value=train_ds.y[0]
                )

                test_ds_y_transformed = self.integrate_diff(
                    test_ds.y_df().values, start_value=test_ds.y[0]
                )

                # Use the first value of the transformed train dataset as the start_value for predicted datasets

                y_pred_transformed = self.integrate_diff(
                    y_pred, start_value=train_ds_y_transformed[0]
                )
                y_pred_test_transformed = self.integrate_diff(
                    y_pred_test, start_value=test_ds_y_transformed[0]
                )

                # Create copies of the original datasets and update them to reflect transformed data
                train_ds_transformed = train_ds.copy
                train_ds_transformed["y"] = train_ds_y_transformed

                test_ds_transformed = test_ds.copy
                test_ds_transformed["y"] = test_ds_y_transformed

                # transformed train vs forecast
                axs[1, 0].plot(
                    train_ds.index,
                    train_ds_y_transformed,
                    label="Train Dataset",
                    color="grey",
                )

                axs[1, 0].plot(
                    train_ds.index, y_pred_transformed, label="Train Forecast"
                )

                axs[1, 0].set_title(
                    f"Integrated Forecast vs Observed for features {feature_columns}"
                )
                axs[1, 0].legend()

                # transformed test vs forecast
                axs[1, 1].plot(
                    test_ds.index,
                    test_ds_y_transformed,
                    label="Test Dataset",
                    color="grey",
                )

                axs[1, 1].plot(
                    test_ds.index, y_pred_test_transformed, label="Test Forecast"
                )
                axs[1, 1].set_title(
                    f"Integrated Forecast vs Observed for features {feature_columns}"
                )
                axs[1, 1].legend()

            figures.append(
                Figure(for_object=self, key=f"{self.key}:{i}", figure=fig, metadata={})
            )

            # Close the figure to prevent it from displaying
            plt.close(fig)

        return figures
