# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

from validmind.logging import get_logger
from validmind.vm_models import Figure, Metric, Model

logger = get_logger(__name__)


@dataclass
class RegressionModelSensitivityPlot(Metric):
    """
    This metric performs sensitivity analysis applying shocks to one variable at a time.
    """

    name = "regression_sensitivity_plot"
    default_params = {
        "transformation": None,
        "shocks": [0.1],
    }

    def run(self):
        logger.info(self.params)

        transformation = self.params["transformation"]
        shocks = self.params["shocks"]

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
            y_pred = model.model.predict(shocked_dataset)
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

    def description(self):
        return """
        The sensitivity analysis metric applies various shocks or adjustments to one variable at a time while keeping all other variables constant. This allows for the examination of how changes in a specific variable affect the overall outcome or response of the system being analyzed.
        """
