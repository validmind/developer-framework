# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn import metrics

from .ClusterPerformance import ClusterPerformance


@dataclass
class VMeasure(ClusterPerformance):
    """
    Evaluates homogeneity and completeness of a clustering model using the V Measure Score.

    **1. Purpose:**
    The purpose of this metric, V Measure Score (V Score), is to evaluate the performance of a clustering model. It
    measures the homogeneity and completeness of a set of cluster labels, where homogeneity refers to each cluster
    containing only members of a single class and completeness meaning all members of a given class are assigned to the
    same cluster.

    **2. Test Mechanism:**
    ClusterVMeasure is a class that inherits from another class, ClusterPerformance. It uses the v_measure_score
    function from the sklearn module's metrics package. The required inputs to perform this metric are the model, train
    dataset, and test dataset. The test is appropriate for models tasked with clustering.

    **3. Signs of High Risk:**

    - Low V Measure Score: A low V Measure Score indicates that the clustering model has poor homogeneity or
    completeness, or both. This might signal that the model is failing to correctly cluster the data.

    **4. Strengths:**

    - The V Measure Score is a harmonic mean between homogeneity and completeness. This ensures that both attributes
    are taken into account when evaluating the model, providing an overall measure of its cluster validity.

    - The metric does not require knowledge of the ground truth classes when measuring homogeneity and completeness,
    making it applicable in instances where such information is unavailable.

    **5. Limitations:**

    - The V Score can be influenced by the number of clusters, which means that it might not always reflect the quality
    of the clustering. Partitioning the data into many small clusters could lead to high homogeneity but low
    completeness, leading to a low V Score even if the clustering might be useful.

    - It assumes equal importance of homogeneity and completeness. In some applications, one may be more important than
    the other. The V Score does not provide flexibility in assigning different weights to homogeneity and completeness.
    """

    name = "v_measure_score"
    required_inputs = ["model", "datasets"]
    metadata = {
        "task_types": ["clustering"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }

    def metric_info(self):
        return {"V Measure": metrics.v_measure_score}
