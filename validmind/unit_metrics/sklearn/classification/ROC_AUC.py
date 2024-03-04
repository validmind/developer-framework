# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn.metrics import roc_auc_score

from validmind.vm_models import UnitMetric


@dataclass
class ROC_AUC(UnitMetric):
    def __init__(
        self,
        inputs=None,
        metric_id=None,
        params=None,
        test_id="ROC_AUC Test",
    ):
        # Pass test_id and any other necessary parameters to the superclass
        super().__init__(
            test_id=test_id,
        )

        self.metric_id = metric_id
        self.metric_inputs = inputs
        self.params = params if params is not None else {}

    def run(self):
        y_true = self.metric_inputs["dataset"].y
        y_pred = self._y_pred()

        value = roc_auc_score(y_true, y_pred, **self.params)

        return self.cache_results(metric_value=value)

    def _y_pred(self):
        # Access the dataset and model directly, as their existence is guaranteed
        dataset = self.metric_inputs["dataset"]
        model = self.metric_inputs["model"]
        model_id = model.input_id

        # Attempt to obtain the pre-computed prediction column and model ID from the dataset
        prediction_column = self.get_prediction_column(dataset, model_id)
        print(f"model_id: {model_id}, prediction_column: {prediction_column}")

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
            raise ValueError(
                "Model must have a 'predict' method to compute predictions."
            )

        return y_pred
