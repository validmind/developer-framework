# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class ClusterPerformance(Metric):
    """
    Evaluates and compares a clustering model's performance on training and testing datasets using multiple defined
    metrics.

    **Purpose:** This metric, ClusterPerformance, evaluates the performance of a clustering model on both the training
    and testing datasets. It assesses how well the model defines, forms, and distinguishes clusters of data.

    **Test Mechanism:** The metric is applied by first predicting the clusters of the training and testing datasets
    using the clustering model. Next, performance metrics, defined in the method `metric_info()`, are calculated
    against the true labels of the datasets. The results for each metric for both datasets are then collated and
    returned in a summarized table form listing each metric along with its corresponding train and test values.

    **Signs of High Risk:**
    - High discrepancy between the performance metric values on the training and testing datasets. This could signify
    problems such as overfitting or underfitting.
    - Low performance metric values on the training and testing datasets. There might be a problem with the model
    itself or the chosen hyperparameters.
    - If the model's performance deteriorates consistently across different sets of metrics, this may suggest a broader
    issue with the model or the dataset.

    **Strengths:**
    - Tests the model's performance on both the training and testing datasets, which helps to identify issues such as
    overfitting or underfitting.
    - Allows for a broad range of performance metrics to be used, thus providing a comprehensive evaluation of the
    model's clustering capabilities.
    - Returns a summarized table, which makes it easy to compare the model's performance across different metrics and
    datasets.

    **Limitations:**
    - The method `metric_info()` needs to be properly overridden in a subclass for this class to be used, and the
    metrics to be used must be manually defined.
    - The performance metrics are calculated on predicted cluster labels, so the metric may not capture the model's
    performance well if the clusters are not well separated or if the model has difficulties with certain kinds of
    clusters.
    - Doesn't consider the computational and time complexity of the model. While the model may perform well in terms of
    the performance metrics, it might be time or resource-intensive. This metric does not account for such scenarios.
    - Because the comparison is binary (train and test), it might not capture scenarios where the performance changes
    drastically under different circumstances or categories within the dataset.
    """

    name = "cluster_performance_metrics"
    required_inputs = ["model", "datasets"]
    tasks = ["clustering"]
    tags = [
        "sklearn",
        "model_performance",
    ]

    def cluser_performance_metrics(
        self, y_true_train, y_pred_train, y_true_test, y_pred_test, samples, metric_info
    ):
        y_true_train = y_true_train.astype(y_pred_train.dtype).flatten()
        y_true_test = y_true_test.astype(y_pred_test.dtype).flatten()
        results = []
        for metric_name, metric_fcn in metric_info.items():
            for _ in samples:
                train_value = metric_fcn(list(y_true_train), y_pred_train)
                test_value = metric_fcn(list(y_true_test), y_pred_test)
            results.append(
                {
                    metric_name: {
                        "train": train_value,
                        "test": test_value,
                    }
                }
            )
        return results

    def summary(self, raw_results):
        """
        Returns a summarized representation of the dataset split information
        """
        table_records = []
        for result in raw_results:
            for key, _ in result.items():
                table_records.append(
                    {
                        "Metric": key,
                        "TRAIN": result[key]["train"],
                        "TEST": result[key]["test"],
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def metric_info(self):
        raise NotImplementedError

    def run(self):
        y_true_train = self.inputs.datasets[0].y
        class_pred_train = self.inputs.datasets[0].y_pred(self.inputs.model)
        y_true_train = y_true_train.astype(class_pred_train.dtype)

        y_true_test = self.inputs.datasets[1].y
        class_pred_test = self.inputs.datasets[1].y_pred(self.inputs.model)
        y_true_test = y_true_test.astype(class_pred_test.dtype)

        samples = ["train", "test"]
        results = self.cluser_performance_metrics(
            y_true_train,
            class_pred_train,
            y_true_test,
            class_pred_test,
            samples,
            self.metric_info(),
        )
        return self.cache_results(metric_value=results)
