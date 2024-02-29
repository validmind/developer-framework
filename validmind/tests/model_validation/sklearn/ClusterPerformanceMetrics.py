# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from sklearn import metrics

from validmind.vm_models import ResultSummary, ResultTable

from .ClusterPerformance import ClusterPerformance


@dataclass
class ClusterPerformanceMetrics(ClusterPerformance):
    """
    Evaluates the performance of clustering machine learning models using multiple established metrics.

    **Purpose:**

    The `ClusterPerformanceMetrics` test is used to assess the performance and validity of clustering machine learning
    models. It evaluates homogeneity, completeness, V measure score, the Adjusted Rand Index, the Adjusted Mutual
    Information, and the Fowlkes-Mallows score of the model. These metrics provide a holistic understanding of the
    model's ability to accurately form clusters of the given dataset.

    **Test Mechanism:**

    The `ClusterPerformanceMetrics` test runs a clustering ML model over a given dataset and then calculates six
    metrics using the Scikit-learn metrics computation functions: Homogeneity Score, Completeness Score, V Measure,
    Adjusted Rand Index (ARI), Adjusted Mutual Information (AMI), and Fowlkes-Mallows Score. It then returns the result
    as a summary, presenting the metric values for both training and testing datasets.

    **Signs of High Risk:**

    - Low Homogeneity Score: This indicates that the clusters formed contain a variety of classes, resulting in less
    pure clusters.
    - Low Completeness Score: This suggests that class instances are scattered across multiple clusters rather than
    being gathered in a single cluster.
    - Low V Measure: This would report a low overall clustering performance.
    - ARI close to 0 or Negative: This implies that clustering results are random or disagree with the true labels.
    - AMI close to 0: It means that clustering labels are random compared with the true labels.
    - Low Fowlkes-Mallows score: Signifies less precise and poor clustering performance in terms of precision and
    recall.

    **Strengths:**

    - Provides a comprehensive view of clustering model performance by examining multiple clustering metrics.
    - Uses established and widely accepted metrics from scikit-learn, providing reliability in the results.
    - Able to provide performance metrics for both training and testing datasets.
    - Clearly defined and human-readable descriptions of each score make it easy to understand what each score
    represents.

    **Limitations:**

    - It only applies to clustering models; not suitable for other types of machine learning models.
    - Does not test for overfitting or underfitting in the clustering model.
    - All the scores rely on ground truth labels, the absence or inaccuracy of which can lead to misleading results.
    - Does not consider aspects like computational efficiency of the model or its capability to handle high dimensional
    data.
    """

    name = "homogeneity_score"
    required_inputs = ["model", "datasets"]
    metadata = {
        "task_types": ["clustering"],
        "tags": [
            "sklearn",
            "model_performance",
        ],
    }
    default_metrics = {
        "Homogeneity Score": metrics.homogeneity_score,
        "Completeness Score": metrics.completeness_score,
        "V Measure": metrics.v_measure_score,
        "Adjusted Rand Index": metrics.adjusted_rand_score,
        "Adjusted Mutual Information": metrics.adjusted_mutual_info_score,
        "Fowlkes-Mallows score": metrics.fowlkes_mallows_score,
    }
    default_metrics_desc = {
        "Homogeneity Score": """The homogeneity score is a clustering evaluation metric that quantifies
        the degree to which each cluster within a clustering solution contains only data points that belong
        to a single true class or category. It provides a score within the range of 0 to 1, where a higher
        homogeneity score indicates that the clusters are more pure and internally consistent with respect
        to the ground truth labels, meaning that the data points within each cluster are closely related in
        terms of their actual class membership.
        """,
        "Completeness Score": """The completeness score is a clustering evaluation metric used to assess how
        well a clustering solution captures all data points that belong to a single true class or category.
        It quantifies the extent to which the data points of a given class are grouped into a single cluster.
        The completeness score ranges from 0 to 1, with a higher score indicating that the clustering solution
        effectively accounts for all data points within their actual class, emphasizing the comprehensiveness of
        the clustering results with respect to the ground truth labels.""",
        "V Measure": """The V-Measure score is a clustering evaluation metric that combines both homogeneity and
        completeness to provide a single measure of the overall quality of a clustering solution. It takes into
        account how well clusters are internally coherent (homogeneity) and how well they capture all data points
        from the true classes (completeness). The V-Measure score ranges from 0 to 1, where a higher score indicates
        a better clustering result. It balances the trade-off between cluster purity and the extent to which all data
        points from true classes are captured, offering a comprehensive evaluation of the clustering performance.""",
        "Adjusted Rand Index": """The Adjusted Rand Index (ARI) is a clustering evaluation metric used to measure the
        similarity between the cluster assignments in a clustering solution and the true class labels. It calculates a
        score that ranges from -1 to 1, with a higher score indicating a better clustering result. A score of 1 signifies
        perfect agreement between the clustering and the ground truth, while a score near 0 implies that the clustering
        is random with respect to the true labels, and negative values indicate disagreement. ARI accounts for chance
        clustering, making it a robust measure for assessing the quality of clustering solutions by considering both the
        extent of agreement and potential randomness in the assignments.""",
        "Adjusted Mutual Information": """The Adjusted Mutual Information (AMI) is a clustering evaluation metric used to
        quantify the degree of agreement between a clustering solution and the true class labels. It provides a score that
        ranges from 0 to 1, with a higher score indicating a better clustering result. A score of 1 signifies perfect agreement,
        while a score of 0 suggests that the clustering is random with respect to the true labels. AMI takes into account the
        potential randomness in the assignments and adjusts for chance, making it a robust measure that considers both the
        extent of agreement and the potential for random clustering.""",
        "Fowlkes-Mallows score": """The Fowlkes-Mallows score is a clustering evaluation metric used to assess the quality of
        a clustering solution by measuring the geometric mean of two fundamental clustering metrics: precision and recall. It
        provides a score that ranges from 0 to 1, where a higher score indicates a better clustering result. A score of 1 signifies
        perfect agreement with the true class labels, while lower scores suggest less precise and recall clustering performance.
        The Fowlkes-Mallows score offers a balanced evaluation of clustering quality by considering both the ability to correctly
        identify members of the same class (precision) and the ability to capture all members of the same class (recall).""",
    }

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
                        "Description": self.default_metrics_desc[key],
                        "TRAIN": result[key]["train"],
                        "TEST": result[key]["test"],
                    }
                )

        return ResultSummary(results=[ResultTable(data=table_records)])

    def metric_info(self):
        return self.default_metrics
