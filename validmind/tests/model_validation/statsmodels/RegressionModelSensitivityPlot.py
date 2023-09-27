# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric

logger = get_logger(__name__)


@dataclass
class RegressionModelSensitivityPlot(Metric):
    """
    **Purpose**: The Regression Sensitivity Plot metric is designed to facilitate sensitivity analysis for regression
    models. It is primarily utilized for examining the outcome change of a system when alterations(shocks) are applied
    to one variable at a time, keeping all other variables constant. Its core focus is to analyze the effect of each
    independent variable on the dependent variable in the regression model, and thus aids in identifying critical risk
    factors in the model that could significantly influence the output.

    **Test Mechanism**: This test begins by applying shocks of varying magnitudes (as per defined parameters) to each
    feature of the model, one at a time. A new prediction is then made for each shocked dataset. Since these shocks are
    applied while keeping all other variables constant, the resulting changes in the model's predictions can be
    attributed to the shocks. If a transformation parameter is set to "integrate", the initial predictions and target
    values are transformed using an integration function before being plotted. In the end, a plot of observed values
    versus predicted values is generated for each model, with a distinct line graph illustrating predictions for each
    shock.

    **Signs of High Risk**: If the plot shows drastic changes in model predictions with small shocks to an individual
    variable, it may be an indication of high risk. This could suggest a high sensitivity of the model to changes in
    that variable, potentially signaling over-reliance on the variable to make predictions. Unusually high or erratic
    shifts in the response of the model concerning shocks may also suggest potential model instability or overfitting.

    **Strengths**: This metric holds the value by enabling the identification of those variables that have a major
    effect on the model outcomes, thus paving the way towards feature importance understanding. It also generates
    visual plots, making the results understandable, clear, and interpretable even to non-technical stakeholders. It's
    beneficial for spotting overfitting and detecting unstable models that too responsive to small changes in variables.

    **Limitations**: This metric assumes that all other variables remain constant when a shock is applied, which may
    not always reflect real-world conditions where variables might have complex interdependencies. It is also best
    suited for linear models and may not always appropriately evaluate the sensitivity of non-linear models.
    Additionally, it does not provide a numerical measure of risk, it only provides a visual indication, which might be
    subjective.
    """

    name = "regression_sensitivity_plot"
    default_params = {
        "transformation": None,
        "shocks": [0.1],
    }
    metadata = {
        "task_types": ["regression"],
        "tags": ["senstivity_analysis", "visualization"],
    }

    def run(self):
        logger.info(self.params)

        transformation = self.params["transformation"]
        shocks = self.params["shocks"]

        if not self.models:
            raise ValueError("List of models must be provided in the models parameter")

        all_models = []
        for model in self.models:
            all_models.append(model)

        figures = []
        for i, model in enumerate(all_models):
            features_df = model.test_ds.x_df()
            target_df = model.test_ds.y_df()  # series

            shocked_datasets = self.apply_shock(features_df, shocks)

            predictions = self.predict_shocked_datasets(shocked_datasets, model)

            if transformation == "integrate":
                transformed_predictions = []
                start_value = model.train_ds.y[0]
                transformed_target = self.integrate_diff(
                    model.test_ds.y_df().values, start_value
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
