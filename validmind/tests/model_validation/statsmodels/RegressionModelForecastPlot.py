# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric, Model

logger = get_logger(__name__)


@dataclass
class RegressionModelForecastPlot(Metric):
    """
    This metric creates a plot of forecast vs observed for each model in the list.
    """

    name = "regression_forecast_plot"
    default_params = {"start_date": None, "end_date": None}

    def description(self):
        return """
        This section shows plots of training and test datasets vs forecast trainining and forecast test.
        """

    def run(self):
        start_date = self.params["start_date"]
        end_date = self.params["end_date"]

        # Check models list is not empty
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

        figures = self._plot_forecast(all_models, start_date, end_date)

        return self.cache_results(figures=figures)

    def _plot_forecast(self, model_list, start_date=None, end_date=None):
        # Convert start_date and end_date to pandas Timestamp for comparison
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        # Initialize a list to store figures
        figures = []

        for i, fitted_model in enumerate(model_list):
            feature_columns = fitted_model.train_ds.get_features_columns()

            train_ds = fitted_model.train_ds
            test_ds = fitted_model.test_ds

            y_pred = fitted_model.y_train_predict
            y_pred_test = fitted_model.y_test_predict

            # Check that start_date and end_date are within the data range
            all_dates = pd.concat([pd.Series(train_ds.index), pd.Series(test_ds.index)])

            # If start_date or end_date are None, set them to the min/max of all_dates
            if start_date is None:
                start_date = all_dates.min()
            else:
                start_date = pd.Timestamp(start_date)

            if end_date is None:
                end_date = all_dates.max()
            else:
                end_date = pd.Timestamp(end_date)

            # If start_date or end_date are None, set them to the min/max of all_dates
            if start_date is None:
                start_date = all_dates.min()
            else:
                start_date = pd.Timestamp(start_date)

            if end_date is None:
                end_date = all_dates.max()
            else:
                end_date = pd.Timestamp(end_date)

            if start_date < all_dates.min() or end_date > all_dates.max():
                raise ValueError(
                    "start_date and end_date must be within the range of dates in the data"
                )

            fig, ax = plt.subplots()
            ax.plot(train_ds.index, train_ds.y, label="Train Forecast")
            ax.plot(test_ds.index, test_ds.y, label="Test Forecast")
            ax.plot(train_ds.index, y_pred, label="Train Dataset", color="grey")
            ax.plot(test_ds.index, y_pred_test, label="Test Dataset", color="black")

            plt.title(f"Forecast vs Observed for features {feature_columns}")

            # Set the x-axis limits to zoom in/out
            plt.xlim(start_date, end_date)

            plt.legend()
            # TODO: define a proper key for each plot
            logger.info(f"Plotting forecast vs observed for model {fitted_model.model}")

            plt.close("all")

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{i}",
                    figure=fig,
                    metadata={"model": str(feature_columns)},
                )
            )

        return figures
