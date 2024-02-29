# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn import metrics

from .ClusterPerformance import ClusterPerformance


@dataclass
class AdjustedRandIndex(ClusterPerformance):
    """
    Measures the similarity between two data clusters using the Adjusted Rand Index (ARI) metric in clustering machine
    learning models.

    **1. Purpose:**
    The Adjusted Rand Index (ARI) metric is intended to measure the similarity between two data clusters. This metric
    is specifically being used for clustering machine learning models to validly quantify how well the model is
    clustering and producing data groups. It involves comparing the model's produced clusters against the actual (true)
    clusters found in the dataset.

    **2. Test Mechanism:**
    The Adjusted Rand Index (ARI) is calculated by using the `adjusted_rand_score` method from the sklearn metrics in
    Python. The test requires inputs including the model itself and the model's training and test datasets. The model's
    computed clusters and the true clusters are compared, and the similarities are measured to compute the ARI.

    **3. Signs of High Risk:**
    - If the ARI is close to zero, it signifies that the model's cluster assignments are random and don't match the
    actual dataset clusters, indicating a high risk.
    - An ARI of less than zero indicates that the model's clustering performance is worse than random.

    **4. Strengths:**
    - ARI is normalized and it hence gives a consistent metric between -1 and +1, irrespective of raw cluster sizes or
    dataset size variations.
    - It doesn’t require a ground truth for computation which makes it ideal for unsupervised learning model
    evaluations.
    - It penalizes for false positives and false negatives, providing a robust measure of clustering quality.

    **5. Limitations:**
    - In real-world situations, true clustering is often unknown, which can hinder the practical application of the ARI.
    - The ARI requires all individual data instances to be independent, which may not always hold true.
    - It may be difficult to interpret the implications of an ARI score without a context or a benchmark, as it is
    heavily dependent on the characteristics of the dataset used.
    """

    name = "adjusted_rand_index"
    required_inputs = ["model", "datasets"]
    metadata = {
        "task_types": ["clustering"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }

    def metric_info(self):
        return {"Adjusted Rand Index": metrics.adjusted_rand_score}
