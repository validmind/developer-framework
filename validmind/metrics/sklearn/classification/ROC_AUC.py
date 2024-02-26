# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass
from typing import Optional

from sklearn.metrics import roc_auc_score

from validmind.vm_models import UnitMetric


@dataclass
class ROC_AUC(UnitMetric):
    def __init__(
        self,
        inputs=None,
        params=None,
        test_id="ROC AUC Score",
    ):
        super().__init__(test_id=test_id)
        self.metric_inputs = inputs
        self.params = params if params is not None else {}
        self.type = "evaluation"
        self.scope = "model_accuracy"

    def run(self):
        y_pred, y_true = self.get_required_inputs()
        value = roc_auc_score(y_true, y_pred, **self.params)
        return self.cache_results(metric_value=value)

    def get_required_inputs(self):
        y_pred = self._get_y_pred()
        y_true = self._get_y_true()
        return y_pred, y_true

    def _get_y_pred(self):
        dataset = self.metric_inputs.get("dataset")
        if self.metric_inputs.get("model") is not None:
            model = self.metric_inputs.get("model")
            if hasattr(model, "predict_proba"):
                print("y_pred obtained from model probability predictions")
                y_pred = model.predict_proba(dataset._df[dataset.feature_columns])[
                    :, 1
                ]  # Assuming binary classification
            elif hasattr(model, "predict"):
                print("y_pred obtained from model predictions")
                y_pred = model.predict(dataset._df[dataset.feature_columns])
            else:
                raise ValueError("Model must have a predict or predict_proba method.")
        else:
            print(f"y_pred obtained from column: {dataset.prediction_column}")
            y_pred = dataset._df[dataset.prediction_column]
        return y_pred

    def _get_y_true(self):
        dataset = self.metric_inputs.get("dataset")
        print(f"y_true obtained from column: {dataset.target_column}")
        y_true = dataset._df[dataset.target_column]
        return y_true

    def summary(self, metric_value: Optional[dict] = None):
        if metric_value is None:
            return {"Error": "No metric calculated."}
        return {
            "ROC AUC": f"{metric_value:.2f}",
        }
