# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from validmind.vm_models import Figure, Metric, Model


@dataclass
class RegressionModelForecastPlotLevels(Metric):
    """
    This metric creates a plot of forecast vs observed for each model in the list.
    """

    name = "regression_forecast_plot_levels"
    default_params = {
        "transformation": None,
    }

    def description(self):
        return """
        This section shows plots of training and test datasets vs forecast training and test.
        """

    def run(self):
        transformation = self.params["transformation"]

        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        for model in self.models:
            if not Model.is_supported_model(model.model):
                raise ValueError(
                    f"{Model.model_library(model.model)}.{Model.model_class(model.model)} \
                                 is not supported by ValidMind framework yet"
                )
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

            y_pred = fitted_model.model.predict(fitted_model.train_ds.x)
            y_pred_test = fitted_model.model.predict(fitted_model.test_ds.x)

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
