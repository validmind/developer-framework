# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class RegressionModelForecastPlot(Metric):
    """
    Generates plots to visually compare the forecasted outcomes of one or more regression models against actual
    observed values over a specified date range.

    ### Purpose

    The "regression_forecast_plot" is intended to visually depict the performance of one or more regression models by
    comparing the model's forecasted outcomes against actual observed values within a specified date range. This metric
    is especially useful in time-series models or any model where the outcome changes over time, allowing direct
    comparison of predicted vs actual values.

    ### Test Mechanism

    This test generates a plot for each fitted model in the list. The x-axis represents the date ranging from the
    specified "start_date" to the "end_date", while the y-axis shows the value of the outcome variable. Two lines are
    plotted: one representing the forecasted values and the other representing the observed values. The "start_date"
    and "end_date" can be parameters of this test; if these parameters are not provided, they are set to the minimum
    and maximum date available in the dataset. The test verifies that the provided date range is within the limits of
    the available data.

    ### Signs of High Risk

    - High risk or failure signs could be deduced visually from the plots if the forecasted line significantly deviates
    from the observed line, indicating the model's predicted values are not matching actual outcomes.
    - A model that struggles to handle the edge conditions like maximum and minimum data points could also be
    considered a sign of risk.

    ### Strengths

    - Visualization: The plot provides an intuitive and clear illustration of how well the forecast matches the actual
    values, making it straightforward even for non-technical stakeholders to interpret.
    - Flexibility: It allows comparison for multiple models and for specified time periods.
    - Model Evaluation: It can be useful in identifying overfitting or underfitting situations, as these will manifest
    as discrepancies between the forecasted and observed values.

    ### Limitations

    - Interpretation Bias: Interpretation of the plot is subjective and can lead to different conclusions by different
    evaluators.
    - Lack of Precision: Visual representation might not provide precise values of the deviation.
    - Inapplicability: Limited to cases where the order of data points (time-series) matters, it might not be of much
    use in problems that are not related to time series prediction.
    """

    name = "regression_forecast_plot"
    required_inputs = ["models", "datasets"]
    default_params = {"start_date": None, "end_date": None}
    tasks = ["regression"]
    tags = ["forecasting", "visualization"]

    def run(self):
        start_date = self.params["start_date"]
        end_date = self.params["end_date"]

        # Check models list is not empty
        if not self.inputs.models:
            raise ValueError("List of models must be provided in the models parameter")
        all_models = []
        for model in self.inputs.models:
            all_models.append(model)

        figures = self._plot_forecast(
            all_models, self.inputs.datasets, start_date, end_date
        )

        return self.cache_results(figures=figures)

    def _plot_forecast(self, model_list, datasets, start_date=None, end_date=None):
        # Convert start_date and end_date to pandas Timestamp for comparison
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        # Initialize a list to store figures
        figures = []

        for i, fitted_model in enumerate(model_list):
            feature_columns = datasets[0].feature_columns

            train_ds = datasets[0]
            test_ds = datasets[1]

            y_pred = train_ds.y_pred(fitted_model)
            y_pred_test = test_ds.y_pred(fitted_model)

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
