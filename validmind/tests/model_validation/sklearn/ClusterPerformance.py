# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from validmind.vm_models import Metric


@dataclass
class ClusterPerformance(Metric):
    """
    Evaluates and compares a clustering model's performance on training and testing datasets using multiple defined
    metrics.

    ### Purpose

    The Cluster Performance test evaluates the performance of a clustering model on both the training and testing
    datasets. It assesses how well the model defines, forms, and distinguishes clusters of data.

    ### Test Mechanism

    The test mechanism involves predicting the clusters of the training and testing datasets using the clustering
    model. After prediction, performance metrics defined in the `metric_info()` method are calculated against the true
    labels of the datasets. The results for each metric for both datasets are then collated and returned in a
    summarized table form listing each metric along with its corresponding train and test values.

    ### Signs of High Risk

    - High discrepancy between the performance metric values on the training and testing datasets.
    - Low performance metric values on both the training and testing datasets.
    - Consistent deterioration of performance across different metrics.

    ### Strengths

    - Tests the model's performance on both training and testing datasets, helping to identify overfitting or
    underfitting.
    - Allows for the use of a broad range of performance metrics, providing a comprehensive evaluation.
    - Returns a summarized table, making it easy to compare performance across different metrics and datasets.

    ### Limitations

    - The `metric_info()` method needs to be properly overridden in a subclass and metrics must be manually defined.
    - The test may not capture the model's performance well if clusters are not well-separated or the model struggles
    with certain clusters.
    - Does not consider the computational and time complexity of the model.
    - Binary comparison (train and test) might not capture performance changes under different circumstances or dataset
    categories.
    """

    name = "cluster_performance_metrics"
    required_inputs = ["model", "dataset"]
    tasks = ["clustering"]
    tags = [
        "sklearn",
        "model_performance",
    ]

    def cluster_performance_metrics(self, y_true_train, y_pred_train, metric_info):
        y_true_train = y_true_train.astype(y_pred_train.dtype).flatten()
        results = []
        for metric_name, metric_fcn in metric_info.items():
            train_value = metric_fcn(list(y_true_train), y_pred_train)
            results.append({metric_name: train_value})
        return results

    def metric_info(self):
        raise NotImplementedError

    def run(self):
        y_true_train = self.inputs.dataset.y
        class_pred_train = self.inputs.dataset.y_pred(self.inputs.model)
        y_true_train = y_true_train.astype(class_pred_train.dtype)

        results = self.cluster_performance_metrics(
            y_true_train,
            class_pred_train,
            self.metric_info(),
        )
        return self.cache_results(metric_value=results)
