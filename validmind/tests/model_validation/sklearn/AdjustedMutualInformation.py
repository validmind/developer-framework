# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn import metrics

from .ClusterPerformance import ClusterPerformance


@dataclass
class AdjustedMutualInformation(ClusterPerformance):
    """
    Evaluates clustering model performance by measuring mutual information between true and predicted labels, adjusting
    for chance.

    **1. Purpose**: The purpose of this metric (Adjusted Mutual Information) is to evaluate the performance of a
    machine learning model, more specifically, a clustering model. It measures the mutual information between the true
    labels and the ones predicted by the model, adjusting for chance.

    **2. Test Mechanism**: The Adjusted Mutual Information (AMI) uses sklearn's `adjusted_mutual_info_score` function.
    This function calculates the mutual information between the true labels and the ones predicted while correcting for
    the chance correlation expected due to random label assignments. This test requires the model, the training
    dataset, and the test dataset as inputs.

    **3. Signs of High Risk**:
    - Low Adjusted Mutual Information Score: This score ranges between 0 and 1. A low score (closer to 0) can indicate
    poor model performance as the predicted labels do not align well with the true labels.
    - In case of high dimensional data, if the algorithm shows high scores, this could also be a potential risk as AMI
    may not perform reliably.

    **4. Strengths**:
    - The AMI metric takes into account the randomness of the predicted labels, which makes it more robust than the
    simple Mutual Information.
    - The scale of AMI is not dependent on the sizes of the clustering, allowing for comparability between different
    datasets or models.
    - Good for comparing the output of clustering algorithms where the number of clusters is not known a priori.

    **5. Limitations**:
    - Adjusted Mutual Information does not take into account the continuous nature of some data. As a result, it may
    not be the best choice for regression or other continuous types of tasks.
    - AMI has the drawback of being biased towards clusterings with a higher number of clusters.
    - In comparison to other metrics, AMI can be slower to compute.
    - The interpretability of the score can be complex as it depends on the understanding of information theory
    concepts.
    """

    name = "adjusted_mutual_information"
    required_inputs = ["model", "datasets"]
    metadata = {
        "task_types": ["clustering"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }

    def metric_info(self):
        return {"Adjusted Mutual Information": metrics.adjusted_mutual_info_score}
