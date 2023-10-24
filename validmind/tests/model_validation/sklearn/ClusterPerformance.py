# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from sklearn import metrics

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class ClusterPerformance(Metric):
    """
    Evaluates clustering performance of an ML model using various metrics such as homogeneity, completeness, and
    silhouette coefficient.

    **Purpose**: The ClusterPerformance class measures various aspects of clustering performance for the provided model
    and dataset. These aspects include homogeneity, completeness, variance (V measure), adjusted rand index, adjusted
    mutual information, Fowlkes-Mallows scores, and silhouette coefficient. The primary motive of such measurements is
    to gauge the performance and the accuracy of a clustering-based machine learning model.

    **Test Mechanism**: The class accesses the model and training, testing datasets. It converts all the true and
    predicted values for training and testing to a similar data type. The measurements for the aforementioned
    performance aspects are then calculated for both the training and testing datasets using the respective
    scikit-learn metrics functions. If the metric is 'Silhouette Coefficient', the method metric is set as 'euclidean'.
    Eventually, a summary of all calculated values for each metric is returned.

    **Signs of High Risk**:
    - Significant discrepancy between the performance metrics on the train and test sets, implying overfitting.
    - Low value for Homogeneity Score indicating that all of the clusters contain only data points which are members of
    a single class.
    - Low value for Completeness Score which implies all data points that are members of a given class are elements of
    the same cluster.
    - Low value for V Measure, Adjusted Rand Index, Adjusted Mutual Information, which suggests poor-quality clustering.
    - Fowlkes-Mallows scores close to 0 imply randomly labeled data.
    - Negative Silhouette Coefficient indicates incorrect clustering.

    **Strengths**:
    - Provides multiple performance measurements for cluster-based models, offering comprehensive insight into the
    model.
    - Utilizes the Scikit-learn metrics library which is reliable and robust.
    - Metrics applied are independent of the absolute values of the labels: a permutation of the class or cluster label
    values won't change the score value in any way.

    **Limitations**:
    - Some metrics (for example, Silhouette Coefficient) assume the clusters being measured are convex and isotropic,
    which is not always the case.
    - Dependencies on external libraries leave the class vulnerable to any limitations in the external library (in this
    case, Scikit-learn).
    - Cluster_perfomance_metrics method results are sensitive to the number of clusters and do not correct for chance.
    Hence, a model with more clusters might get a higher score.
    - Certain metrics require the true labels to be known, which can be a problem since clustering is often used in the
    context of unsupervised learning where we don't have pre-defined labels.
    """

    name = "cluster_performance_metrics"
    required_inputs = ["model", "model.train_ds", "model.test_ds"]
    metadata = {
        "task_types": ["clustering"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }
    clustering_metrics = {
        "Homogeneity Score": metrics.homogeneity_score,
        "Completeness Score": metrics.completeness_score,
        "V Measure": metrics.v_measure_score,
        "Adjusted Rand Index": metrics.adjusted_rand_score,
        "Adjusted Mutual Information": metrics.adjusted_mutual_info_score,
        "Fowlkes-Mallows scores": metrics.fowlkes_mallows_score,
        "Silhouette Coefficient": metrics.silhouette_score,
    }

    def cluser_performance_metrics(
        self, y_true_train, y_pred_train, y_true_test, y_pred_test, samples
    ):
        y_true_train = y_true_train.astype(y_pred_train.dtype).flatten()
        y_true_test = y_true_test.astype(y_pred_test.dtype).flatten()

        results = []
        for metric_name, metric_fcn in self.clustering_metrics.items():

            for sample in samples:
                if metric_name == "Silhouette Coefficient":
                    train_value = metric_fcn(
                        self.model.train_ds.x, y_pred_train, metric="euclidean"
                    )
                    test_value = metric_fcn(
                        self.model.test_ds.x, y_pred_test, metric="euclidean"
                    )
                else:
                    train_value = metric_fcn(y_true_train, y_pred_train)
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
            for key, value in result.items():
                table_records.append(
                    {
                        "Metric": key,
                        "TRAIN": result[key]["train"],
                        "TEST": result[key]["test"],
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def run(self):
        y_true_train = self.model.y_train_true
        class_pred_train = self.model.y_train_predict
        y_true_train = y_true_train.astype(class_pred_train.dtype)

        y_true_test = self.model.y_test_true
        class_pred_test = self.model.y_test_predict
        y_true_test = y_true_test.astype(class_pred_test.dtype)
        samples = ["train", "test"]
        results = self.cluser_performance_metrics(
            y_true_train, class_pred_train, y_true_test, class_pred_test, samples
        )
        return self.cache_results(metric_value=results)
