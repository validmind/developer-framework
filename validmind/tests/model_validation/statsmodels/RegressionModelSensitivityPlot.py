# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class RegressionModelSensitivityPlot(Metric):
    """
    Assesses the sensitivity of a regression model to changes in independent variables by applying shocks and
    visualizing the impact.

    ### Purpose

    The Regression Sensitivity Plot test is designed to perform sensitivity analysis on regression models. This test
    aims to measure the impact of slight changes (shocks) applied to individual variables on the system's outcome while
    keeping all other variables constant. By doing so, it analyzes the effects of each independent variable on the
    dependent variable within the regression model, helping identify significant risk factors that could substantially
    influence the model's output.

    ### Test Mechanism

    This test operates by initially applying shocks of varying magnitudes, defined by specific parameters, to each of
    the model's features, one at a time. With all other variables held constant, a new prediction is made for each
    dataset subjected to shocks. Any changes in the model's predictions are directly attributed to the shocks applied.
    If the transformation parameter is set to "integrate," initial predictions and target values undergo transformation
    via an integration function before being plotted. Finally, a plot demonstrating observed values against predicted
    values for each model is generated, showcasing a distinct line graph illustrating predictions for each shock.

    ### Signs of High Risk

    - Drastic alterations in model predictions due to minor shocks to an individual variable, indicating high
    sensitivity and potential over-dependence on that variable.
    - Unusually high or unpredictable shifts in response to shocks, suggesting potential model instability or
    overfitting.

    ### Strengths

    - Helps identify variables that strongly influence model outcomes, aiding in understanding feature importance.
    - Generates visual plots, making results easily interpretable even to non-technical stakeholders.
    - Useful in identifying overfitting and detecting unstable models that react excessively to minor variable changes.

    ### Limitations

    - Operates on the assumption that all other variables remain unchanged during the application of a shock, which may
    not reflect real-world interdependencies.
    - Best compatible with linear models and may not effectively evaluate the sensitivity of non-linear models.
    - Provides a visual representation without a numerical risk measure, potentially introducing subjectivity in
    interpretation.
    """

    name = "regression_sensitivity_plot"
    required_inputs = ["models", "datasets"]
    default_params = {
        "transformation": None,
        "shocks": [0.1],
    }
    tasks = ["regression"]
    tags = ["senstivity_analysis", "visualization"]

    def run(self):
        logger.info(self.params)

        transformation = self.params["transformation"]
        shocks = self.params["shocks"]

        if not self.inputs.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        for model in self.inputs.models:
            all_models.append(model)

        figures = []
        for i, model in enumerate(all_models):
            features_df = self.inputs.datasets[1].x_df()
            target_df = self.inputs.datasets[1].y_df()  # series

            shocked_datasets = self.apply_shock(features_df, shocks)

            predictions = self.predict_shocked_datasets(shocked_datasets, model)

            if transformation == "integrate":
                transformed_predictions = []
                start_value = self.inputs.datasets[0].y[0]
                transformed_target = self.integrate_diff(
                    self.inputs.datasets[1].y_df().values, start_value
                )

                predictions = self.predict_shocked_datasets(shocked_datasets, model)
                transformed_predictions = self.transform_predictions(
                    predictions, start_value
                )

            else:
                transformed_target = target_df.values
                transformed_predictions = predictions

            fig = self._plot_predictions(
                target_df.index, transformed_target, transformed_predictions
            )
            figures.append(
                Figure(for_object=self, key=f"{self.key}:{i}", figure=fig, metadata={})
            )
        return self.cache_results(figures=figures)

    def transform_predictions(self, predictions, start_value):
        transformed_predictions = (
            {}
        )  # Initialize an empty dictionary to store the transformed predictions

        for (
            label,
            pred,
        ) in predictions.items():  # Here, label is the key, pred is the value
            transformed_pred = self.integrate_diff(pred, start_value)
            transformed_predictions[
                label
            ] = transformed_pred  # Store transformed dataframe in the new dictionary

        return transformed_predictions

    def predict_shocked_datasets(self, shocked_datasets, model):
        predictions = {}

        for label, shocked_dataset in shocked_datasets.items():
            y_pred = model.predict(shocked_dataset)
            predictions[label] = y_pred

        return predictions

    def _plot_predictions(self, index, target, predictions):
        fig = plt.figure()

        # Plot the target
        plt.plot(index, target, label="Observed")

        # Plot each prediction
        for label, pred in predictions.items():
            plt.plot(index, pred, label=label)

        plt.legend()

        # Close the figure to prevent it from displaying
        plt.close(fig)
        return fig

    def integrate_diff(self, series_diff, start_value):
        series_diff = np.asarray(series_diff, dtype=np.float64)  # Convert to float64
        series = np.cumsum(series_diff)
        series += start_value
        return series

    def apply_shock(self, df, shocks):
        shocked_dfs = {"Baseline": df.copy()}  # Start with the original dataset
        cols_to_shock = df.columns  # All columns

        # Apply shock one variable at a time
        for shock in shocks:
            for col in cols_to_shock:
                temp_df = df.copy()
                temp_df[col] = temp_df[col] * (1 + shock)
                shocked_dfs[
                    f"Shock of {shock} to {col}"
                ] = temp_df  # Include shock value in the key

        return shocked_dfs
