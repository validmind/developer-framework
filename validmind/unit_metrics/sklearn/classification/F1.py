# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import Optional

from sklearn.metrics import f1_score

from validmind.vm_models import UnitMetric


@dataclass
class F1(UnitMetric):
    def __init__(
        self,
        inputs=None,
        params=None,
        test_id="F1 Score",
    ):
        # Pass test_id and any other necessary parameters to the superclass
        super().__init__(
            test_id=test_id,
        )

        self.metric_inputs = inputs
        self.params = params if params is not None else {}

        # Initialize any additional properties specific to F1
        self.type = "evaluation"
        self.scope = "model_accuracy"

    def run(self):

        y_pred, y_true = self.get_required_inputs()

        value = f1_score(y_true, y_pred, **self.params)

        return self.cache_results(
            metric_value=value,
        )

    def get_required_inputs(self):

        y_pred = self._get_y_pred()
        y_true = self._get_y_true()

        return y_pred, y_true

    def _get_y_pred(self):
        # Access the dataset and model directly, as their existence is guaranteed
        dataset = self.metric_inputs["dataset"]
        model = self.metric_inputs["model"]
        model_id = model.input_id

        # Attempt to obtain the pre-computed prediction column and model ID from the dataset
        print(f"model_id: {model_id}, prediction_column: {prediction_column}")
        prediction_column = self.get_prediction_column(dataset, model_id)

        # If a prediction column specific to the model is found in the dataset, use those predictions
        if prediction_column:
            print(
                f"y_pred obtained from pre-computed predictions in dataset column '{prediction_column}' from '{model_id}'"
            )
            y_pred = dataset.y_pred(model_id=model_id)
        # If no pre-computed predictions are found, compute them directly from the model
        elif hasattr(model, "predict"):
            print(f"y_pred computed directly from model '{model.input_id}'")
            y_pred = model.predict(dataset._df[dataset.feature_columns])
        else:
            # If the model does not have a 'predict' method, raise an error
            raise ValueError("Model must have a predict method to compute predictions.")

        return y_pred

    def _get_y_true(self):
        dataset = self.metric_inputs.get("dataset")
        print(f"y_true obtained from column '{dataset.target_column}'")
        y_true = dataset.y
        return y_true

    def summary(self, metric_value: Optional[dict] = None):
        if metric_value is None:
            return {"Error": "No metric calculated."}

        return {
            "F1": f"{metric_value:.2f}",
        }
