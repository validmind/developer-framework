# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class GINITable(Metric):
    """
    **Purpose**: This metric 'GINITable' is used to calculate and display the AUC (Area under the ROC Curve), GINI
    coefficient, and KS (Kolmogorov-Smirnov) statistic for both training and testing datasets. These metrics are used
    to evaluate the performance of a classification model and quantify its discriminatory power, i.e., its ability to
    distinguish between different classes.

    **Test Mechanism**: A dict is created to store performance metrics for both training and testing datasets. The
    algorithm loops over these datasets and computes the metrics for each. The Area under the ROC (Receiver Operating
    Characteristic) Curve (AUC) is calculated by invoking the compute_auc method, which uses the roc_auc_score function
    from Scikit-Learn. The GINI coefficient, a measure of statistical dispersion, is computed by doubling the AUC and
    subtracting 1. The Kolmogorov-Smirnov (KS) statistic is computed using the roc_curve function of Scikit-Learn,
    subtracting False Positive Rate (FPR) from True Positive Rate (TPR), and then finding the maximum value from the
    resulting dataset. The calculated metrics are stored in a pandas DataFrame for neat display.

    **Signs of High Risk**: High risk is indicated when performance metrics values are low or there is a substantial
    discrepancy between the performance in training and testing datasets. A low AUC indicates poor classification
    performance, while a low GINI coefficient suggests low discriminatory power. High KS value, on the other hand, may
    indicate potential overfitting as it signifies a substantial gap between positive and negative distributions.

    **Strengths**:
    1. This test provides multiple metrics (AUC, GINI, and KS) giving a broader perspective on the model's performance.
    2. It compares the performance of the model on both training and testing datasets, offering insight into potential
    overfitting or underfitting.
    3. The metrics used are invariant to class distribution and can effectively measure model performance even for
    imbalanced datasets.
    4. Displays the metrics in a user-friendly, neatly formatted table.

    **Limitations**:
    1. The GINI coefficient and KS statistic are reliant on the AUC value, meaning any error in AUC calculation will
    propagate and affect these metrics too.
    2. It is mainly suitable for binary classification models and may require adjustments for multi-class scenarios.
    3. The metrics used are threshold-dependent and may vary significantly based on chosen cut-off points.
    4. The test does not contain any method to handle missing or inefficient data which might lead to inaccurate
    metrics if data is not preprocessed efficiently.
    """

    name = "gini_table"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["visualization", "model_performance"],
    }

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
