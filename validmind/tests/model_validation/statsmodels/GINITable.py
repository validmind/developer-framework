# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from dataclasses import dataclass
from validmind.vm_models import (
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)
from sklearn.metrics import roc_auc_score, roc_curve


@dataclass
class GINITable(Metric):
    """
    Compute and display the AUC, GINI, and KS for train and test sets.
    """

    name = "gini_table"
    required_context = ["model"]

    def run(self):
        if not Model.is_supported_model(self.model.model):
            raise ValueError(
                f"{Model.model_library(self.model.model)}.{Model.model_class(self.model.model)} \
                              is not supported by ValidMind framework yet"
            )

        model = self.model

        X_train = self.model.train_ds.x
        y_train = self.model.train_ds.y

        X_test = self.model.test_ds.x
        y_test = self.model.test_ds.y

        summary_metrics = self.compute_metrics(model, X_train, y_train, X_test, y_test)

        return self.cache_results(
            {
                "metrics_summary": summary_metrics,
            }
        )

    def compute_metrics(self, model, X_train, y_train, X_test, y_test):
        """Computes AUC, GINI, and KS for train and test sets."""

        metrics_dict = {"Dataset": ["Train", "Test"], "AUC": [], "GINI": [], "KS": []}

        for dataset, X, y in zip(
            ["Train", "Test"], [X_train, X_test], [y_train, y_test]
        ):
            # Get predicted probabilities
            X = X[X_train.columns]  # Ensure X has the same columns as X_train
            y_scores = model.predict(X)

            # Compute AUC, GINI, and KS
            auc = self.compute_auc(y, y_scores)
            gini = self.compute_gini(y, y_scores)
            ks = self.compute_ks(y, y_scores)

            # Add the metrics to the dictionary
            metrics_dict["AUC"].append(auc)
            metrics_dict["GINI"].append(gini)
            metrics_dict["KS"].append(ks)

        # Convert dictionary to DataFrame for nicer display
        metrics_df = pd.DataFrame(metrics_dict)
        return metrics_df

    def compute_auc(self, y_true, y_scores):
        """Computes the Area Under the Curve (AUC)."""
        auc = roc_auc_score(y_true, y_scores)
        return auc

    def compute_gini(self, y_true, y_scores):
        """Computes the Gini coefficient."""
        auc = self.compute_auc(y_true, y_scores)
        gini = 2 * auc - 1
        return gini

    def compute_ks(self, y_true, y_scores):
        """Computes the Kolmogorov-Smirnov (KS) statistic."""
        fpr, tpr, _ = roc_curve(y_true, y_scores)
        ks = np.max(tpr - fpr)
        return ks

    def summary(self, metric_value):
        summary_metrics_table = metric_value["metrics_summary"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_metrics_table,
                    metadata=ResultTableMetadata(
                        title="AUC, GINI and KS for train and test datasets"
                    ),
                )
            ]
        )
