# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
    required_inputs = ["model", "datasets"]
    metadata = {
        "task_types": ["classification"],
        "tags": ["visualization", "model_performance"],
    }

    def run(self):

        summary_metrics = self.compute_metrics()

        return self.cache_results(
            {
                "metrics_summary": summary_metrics.to_dict(orient="records"),
            }
        )

    def compute_metrics(self):
        """Computes AUC, GINI, and KS for an arbitrary number of datasets."""
        # Initialize the dictionary to store results
        metrics_dict = {"Dataset": [], "AUC": [], "GINI": [], "KS": []}

        # Iterate over each dataset in the inputs
        for i, dataset in enumerate(self.inputs.datasets):
            dataset_label = (
                dataset.input_id
            )  # Use input_id as the label for each dataset
            metrics_dict["Dataset"].append(dataset_label)

            # Retrieve y_true and y_pred for the current dataset
            y_true = np.ravel(dataset.y)  # Flatten y_true to make it one-dimensional
            y_prob = dataset.y_prob(self.inputs.model)

            # Compute metrics
            y_true = np.array(y_true, dtype=float)
            y_prob = np.array(y_prob, dtype=float)

            fpr, tpr, _ = roc_curve(y_true, y_prob)
            ks = max(tpr - fpr)
            auc = roc_auc_score(y_true, y_prob)
            gini = 2 * auc - 1

            # Add the metrics to the dictionary
            metrics_dict["AUC"].append(auc)
            metrics_dict["GINI"].append(gini)
            metrics_dict["KS"].append(ks)

        # Create a DataFrame to store and return the results
        metrics_df = pd.DataFrame(metrics_dict)
        return metrics_df

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
