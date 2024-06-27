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
    Compares and visualizes forecasted and actual values of regression models on both raw and transformed datasets.

    **Purpose:**
    The `RegressionModelForecastPlotLevels` metric is designed to visually assess a series of regression models'
    performance. It achieves this by contrasting the models' forecasts with the observed data from the respective
    training and test datasets. The gauge of accuracy here involves determining the extent of closeness between
    forecasted and actual values. Accordingly, if any transformations are specified, the metric will handle
    transforming the data before making this comparison.

    **Test Mechanism:**
    The `RegressionModelForecastPlotLevels` class in Python initiates with a `transformation` parameter, which default
    aggregates to None. Initially, the class checks for the presence of model objects and raises a `ValueError` if none
    are found. Each model is then processed, creating predictive forecasts for both its training and testing datasets.
    These forecasts are then contrasted with the actual values and plotted. In situations where a specified
    transformation, like "integrate," is specified, the class navigates the transformation steps (performing cumulative
    sums to generate a novel series, for instance). Finally, plots are produced that compare observed and forecasted
    values for both the raw and transformed datasets.

    **Signs of High Risk:**
    Indications of high risk or failure in the model's performance can be derived from checking the generated plots.
    When the forecasted values dramatically deviate from the observed values in either the training or testing
    datasets, it suggests a high risk situation. A significant deviation could be a symptom of either overfitting or
    underfitting, both scenarios are worrying. Such discrepancies could inhibit the model's ability to create precise,
    generalized results.

    **Strengths:**

    - Visual Evaluations: The metric provides a visual and comparative way of assessing multiple regression models at
    once. This allows easier interpretation and evaluation of their forecasting accuracy.
    - Transformation Handling: This metric can handle transformations like "integrate," enhancing its breadth and
    flexibility in evaluating different models.
    - Detailed Perspective: By looking at the performance on both datasets (training and testing), the metric may give
    a detailed overview of the model.

    **Limitations:**

    - Subjectivity: Relying heavily on visual interpretations; assessments may differ from person to person.
    - Limited Transformation Capability: Currently, only the "integrate" transformation is supported, implying complex
    transformations might go unchecked or unhandled.
    - Overhead: The plotting mechanism may become computationally costly when applying to extensive datasets,
    increasing runtime.
    - Numerical Measurement: Although visualization is instrumental, a corresponding numerical measure would further
    reinforce the observations. However, this metric does not provide numerical measures.
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
