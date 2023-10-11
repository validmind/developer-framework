# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class GINITable(Metric):
    """
    Evaluates classification model performance using AUC, GINI, and KS metrics for training and test datasets.

    **Purpose**: The 'GINITable' metric is designed to evaluate the performance of a classification model by
    emphasizing its discriminatory power. Specifically, it calculates and presents three important metrics - the Area
    under the ROC Curve (AUC), the GINI coefficient, and the Kolmogov-Smirnov (KS) statistic - for both training and
    test datasets.

    **Test Mechanism**: Using a dictionary for storing performance metrics for both the training and test datasets, the
    'GINITable' metric calculates each of these metrics sequentially. The Area under the ROC Curve (AUC) is calculated
    via the `roc_auc_score` function from the Scikit-Learn library. The GINI coefficient, a measure of statistical
    dispersion, is then computed by doubling the AUC and subtracting 1. Finally, the Kolmogov-Smirnov (KS) statistic is
    calculated via the `roc_curve` function from Scikit-Learn, with the False Positive Rate (FPR) subtracted from the
    True Positive Rate (TPR) and the maximum value taken from the resulting data. These metrics are then stored in a
    pandas DataFrame for convenient visualization.

    **Signs of High Risk**:
    - Low values for performance metrics may suggest a reduction in model performance, particularly a low AUC which
    indicates poor classification performance, or a low GINI coefficient, which could suggest a decreased ability to
    discriminate different classes.
    - A high KS value may be an indicator of potential overfitting, as this generally signifies a substantial
    divergence between positive and negative distributions.
    - Significant discrepancies between the performance on the training dataset and the test dataset may present
    another signal of high risk.

    **Strengths**:
    - Offers three key performance metrics (AUC, GINI, and KS) in one test, providing a more comprehensive evaluation
    of the model.
    - Provides a direct comparison between the model's performance on training and testing datasets, which aids in
    identifying potential underfitting or overfitting.
    - The applied metrics are class-distribution invariant, thereby remaining effective for evaluating model
    performance even when dealing with imbalanced datasets.
    - Presents the metrics in a user-friendly table format for easy comprehension and analysis.

    **Limitations**:
    - The GINI coefficient and KS statistic are both dependent on the AUC value. Therefore, any errors in the
    calculation of the latter will adversely impact the former metrics too.
    - Mainly suited for binary classification models and may require modifications for effective application in
    multi-class scenarios.
    - The metrics used are threshold-dependent and may exhibit high variability based on the chosen cut-off points.
    - The test does not incorporate a method to efficiently handle missing or inefficiently processed data, which could
    lead to inaccuracies in the metrics if the data is not appropriately preprocessed.
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
