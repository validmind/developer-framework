# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from validmind.vm_models import Figure, Metric


@dataclass
class RegressionModelForecastPlotLevels(Metric):
    """
    Assesses the alignment between forecasted and observed values in regression models through visual plots, including
    handling data transformations.

    ### Purpose

    The `RegressionModelForecastPlotLevels` test aims to visually assess the performance of a series of regression
    models by comparing their forecasted values against the actual observed values in both training and test datasets.
    This test helps determine the accuracy of the models and can handle specific data transformations before making the
    comparison, providing a comprehensive evaluation of model performance.

    ### Test Mechanism

    The test mechanism involves initializing the `RegressionModelForecastPlotLevels` class with an optional
    `transformation` parameter. The class then:

    - Checks for the presence of model objects and raises a `ValueError` if none are found.
    - Processes each model to generate predictive forecasts for both training and testing datasets.
    - Contrasts these forecasts with the actual observed values.
    - Produces plots to visually compare forecasted and observed values for both raw and transformed datasets.
    - Handles specified transformations (e.g., "integrate") by performing cumulative sums to create a new series before
    plotting.

    ### Signs of High Risk

    - Significant deviation between forecasted and observed values in training or testing datasets.
    - Patterns suggesting overfitting or underfitting.
    - Large discrepancies in the plotted forecasts, indicating potential issues with model generalizability and
    precision.

    ### Strengths

    - **Visual Evaluations**: Provides an intuitive, visual way to assess multiple regression models, aiding in easier
    interpretation and evaluation of forecast accuracy.
    - **Transformation Handling**: Can process specified data transformations such as "integrate," enhancing
    flexibility.
    - **Detailed Perspective**: Assesses performance on both training and testing datasets, offering a comprehensive
    view of model behavior.

    ### Limitations

    - **Subjectivity**: Relies heavily on visual interpretation, which may vary between individuals.
    - **Limited Transformation Capability**: Supports only the "integrate" transformation; other complex
    transformations might not be handled.
    - **Overhead**: Plotting can be computationally intensive for large datasets, increasing runtime.
    - **Numerical Measurement**: Does not provide a numerical metric to quantify forecast accuracy, relying solely on
    visual assessment.
    """

    name = "regression_forecast_plot_levels"
    required_inputs = ["models", "datasets"]
    default_params = {
        "transformation": None,
    }
    tasks = ["regression"]
    tags = ["forecasting", "visualization"]

    def run(self):
        transformation = self.params["transformation"]

        if not self.inputs.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        for model in self.inputs.models:
            all_models.append(model)

        figures = self._plot_forecast(all_models, self.inputs.datasets, transformation)

        return self.cache_results(figures=figures)

    def integrate_diff(self, series_diff, start_value):
        series_diff = np.array(series_diff)
        series_orig = np.cumsum(series_diff)
        series_orig += start_value
        return series_orig

    def _plot_forecast(
        self,
        model_list,
        datasets,
        transformation=None,
    ):
        figures = []

        for i, fitted_model in enumerate(model_list):
            feature_columns = datasets[0].feature_columns

            train_ds = datasets[0]
            test_ds = datasets[1]

            y_pred = train_ds.y_pred(fitted_model)
            y_pred_test = test_ds.y_pred(fitted_model)

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
