# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class GINITable(Metric):
    """
    Compute and display the AUC, GINI, and KS for train and test sets.
    """

    name = "gini_table"
    required_inputs = ["model"]

    def run(self):
        model = self.model[0] if isinstance(self.model, list) else self.model

        X_train = model.train_ds.x
        y_train = model.train_ds.y

        X_test = model.test_ds.x
        y_test = model.test_ds.y

        summary_metrics = self.compute_metrics(model, X_train, y_train, X_test, y_test)

        return self.cache_results(
            {
                "metrics_summary": summary_metrics.to_dict(orient="records"),
            }
        )

    def compute_metrics(self, model, X_train, y_train, X_test, y_test):
        """Computes AUC, GINI, and KS for train and test sets."""

        metrics_dict = {"Dataset": ["Train", "Test"], "AUC": [], "GINI": [], "KS": []}

        for dataset, X, y in zip(
            ["Train", "Test"], [X_train, X_test], [y_train, y_test]
        ):
            y_scores = model.predict(X)

            print("Predicted scores obtained...")

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
        print("Computing AUC...")
        auc = roc_auc_score(y_true, y_scores)
        return auc

    def compute_gini(self, y_true, y_scores):
        """Computes the Gini coefficient."""
        print("Computing GINI...")
        auc = self.compute_auc(y_true, y_scores)
        gini = 2 * auc - 1
        return gini

    def compute_ks(self, y_true, y_scores):
        """Computes the Kolmogorov-Smirnov (KS) statistic."""
        print("Computing KS...")
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
