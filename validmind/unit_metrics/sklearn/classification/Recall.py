# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import Optional

from sklearn.metrics import recall_score

from validmind.vm_models import UnitMetric


@dataclass
class Recall(UnitMetric):
    def __init__(
        self,
        inputs=None,
        params=None,
        test_id="Recall Score",
    ):
        super().__init__(test_id=test_id)
        self.metric_inputs = inputs
        self.params = params if params is not None else {}
        self.type = "evaluation"
        self.scope = "model_accuracy"

    def run(self):
        y_pred, y_true = self.get_required_inputs()
        value = recall_score(y_true, y_pred, **self.params)
        return self.cache_results(metric_value=value)

    def get_required_inputs(self):
        y_pred = self._get_y_pred()
        y_true = self._get_y_true()
        return y_pred, y_true

    def _get_y_pred(self):
        dataset = self.metric_inputs.get("dataset")
        if self.metric_inputs.get("model") is not None:
            model = self.metric_inputs.get("model")
            if hasattr(model, "predict"):
                print(f"y_pred computed directly from model '{model.input_id}'")
                y_pred = model.predict(dataset._df[dataset.feature_columns])
            else:
                raise ValueError("Model must have a predict method.")
        else:
            model_id, prediction_column = self.get_prediction_column_and_model_id(dataset)
            print(f"y_pred obtained from pre-computed predictions in dataset column '{prediction_column}' from '{model_id}'")
            y_pred = dataset.y_pred(model_id=model_id)
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
            "Recall": f"{metric_value:.2f}",
        }
