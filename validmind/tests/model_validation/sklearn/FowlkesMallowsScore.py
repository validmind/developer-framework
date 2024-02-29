# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn import metrics

from .ClusterPerformance import ClusterPerformance


@dataclass
class FowlkesMallowsScore(ClusterPerformance):
    """
    Evaluates the similarity between predicted and actual cluster assignments in a model using the Fowlkes-Mallows
    score.

    **Purpose:**

    The FowlkesMallowsScore is a performance metric used to validate clustering algorithms within machine learning
    models. The score intends to evaluate the matching grade between two clusters. It measures the similarity between
    the predicted and actual cluster assignments, thus gauging the accuracy of the model's clustering capability.

    **Test Mechanism:**

    The FowlkesMallowsScore method applies the `fowlkes_mallows_score` function from the `sklearn` library to evaluate
    the model's accuracy in clustering different types of data. The test fetches the datasets from the model's training
    and testing datasets as inputs then compares the resulting clusters against the previously known clusters to obtain
    a score. A high score indicates a better clustering performance by the model.

    **Signs of High Risk:**

    - A low Fowlkes-Mallows score (near zero): This indicates that the model's clustering capability is poor and the
    algorithm isn't properly grouping data.
    - Inconsistently low scores across different datasets: this may indicate that the model's clustering performance is
    not robust and the model may fail when applied to unseen data.

    **Strengths:**

    - The Fowlkes-Mallows score is a simple and effective method for evaluating the performance of clustering
    algorithms.
    - This metric takes into account both precision and recall in its calculation, therefore providing a balanced and
    comprehensive measure of model performance.
    - The Fowlkes-Mallows score is non-biased meaning it treats False Positives and False Negatives equally.

    **Limitations:**

    - As a pairwise-based method, this score can be computationally intensive for large datasets and can become
    unfeasible as the size of the dataset increases.
    - The Fowlkes-Mallows score works best with balanced distribution of samples across clusters. If this condition is
    not met, the score can be skewed.
    - It does not handle mismatching numbers of clusters between the true and predicted labels. As such, it may return
    misleading results if the predicted labels suggest a different number of clusters than what is in the true labels.
    """

    name = "fowlkes_mallows_score"
    required_inputs = ["model", "datasets"]
    metadata = {
        "task_types": ["clustering"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }

    def metric_info(self):
        return {"Fowlkes-Mallows score": metrics.fowlkes_mallows_score}
