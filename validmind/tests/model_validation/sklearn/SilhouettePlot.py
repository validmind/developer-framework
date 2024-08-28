# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score

from validmind.vm_models import (
    Figure,
    Metric,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


@dataclass
class SilhouettePlot(Metric):
    """
    Calculates and visualizes Silhouette Score, assessing the degree of data point suitability to its cluster in ML
    models.

    ### Purpose

    This test calculates the Silhouette Score, which is a model performance metric used in clustering applications.
    Primarily, the Silhouette Score evaluates how similar a data point is to its own cluster compared to other
    clusters. The metric ranges between -1 and 1, where a high value indicates that the object is well matched to its
    own cluster and poorly matched to neighboring clusters. Thus, the goal is to achieve a high Silhouette Score,
    implying well-separated clusters.

    ### Test Mechanism

    The test first extracts the true and predicted labels from the model's training data. The test runs the Silhouette
    Score function, which takes as input the training dataset features and the predicted labels, subsequently
    calculating the average score. This average Silhouette Score is printed for reference. The script then calculates
    the silhouette coefficients for each data point, helping to form the Silhouette Plot. Each cluster is represented
    in this plot, with color distinguishing between different clusters. A red dashed line indicates the average
    Silhouette Score. The Silhouette Scores are also collected into a structured table, facilitating model performance
    analysis and comparison.

    ### Signs of High Risk

    - A low Silhouette Score, potentially indicating that the clusters are not well separated and that data points may
    not be fitting well to their respective clusters.
    - A Silhouette Plot displaying overlapping clusters or the absence of clear distinctions between clusters visually
    also suggests poor clustering performance.

    ### Strengths

    - The Silhouette Score provides a clear and quantitative measure of how well data points have been grouped into
    clusters, offering insights into model performance.
    - The Silhouette Plot provides an intuitive, graphical representation of the clustering mechanism, aiding visual
    assessments of model performance.
    - It does not require ground truth labels, so it's useful when true cluster assignments are not known.

    ### Limitations

    - The Silhouette Score may be susceptible to the influence of outliers, which could impact its accuracy and
    reliability.
    - It assumes the clusters are convex and isotropic, which might not be the case with complex datasets.
    - Due to the average nature of the Silhouette Score, the metric does not account for individual data point
    assignment nuances, so potentially relevant details may be omitted.
    - Computationally expensive for large datasets, as it requires pairwise distance computations.
    """

    name = "silhouette_plot"
    required_inputs = ["model", "dataset"]
    tasks = ["clustering"]
    tags = [
        "sklearn",
        "model_performance",
    ]

    def run(self):
        y_pred_train = self.inputs.dataset.y_pred(self.inputs.model)
        # Calculate the silhouette score
        silhouette_avg = silhouette_score(
            self.inputs.dataset.x,
            y_pred_train,
            metric="euclidean",
        )
        num_clusters = len(np.unique(y_pred_train))
        # Calculate silhouette coefficients for each data point
        sample_silhouette_values = silhouette_samples(
            self.inputs.dataset.x, y_pred_train
        )
        # Create a silhouette plot
        fig, ax = plt.subplots()
        y_lower = 10

        for i in range(num_clusters):
            # Aggregate the silhouette scores for samples belonging to cluster i
            ith_cluster_silhouette_values = sample_silhouette_values[y_pred_train == i]
            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
            color = plt.cm.viridis(float(i) / num_clusters)
            ax.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7,
            )

            # Label the silhouette plots with their cluster numbers at the middle
            ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            # Compute the new y_lower for the next plot
            y_lower = y_upper + 10

        ax.set_title("Silhouette Plot for Clusters")
        ax.set_xlabel("Silhouette Coefficient Values")
        ax.set_ylabel("Cluster Label")

        # The vertical line represents the average silhouette score
        ax.axvline(x=silhouette_avg, color="red", linestyle="--")

        figures = [
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        ]
        # Close the figure to prevent it from displaying
        plt.close(fig)

        return self.cache_results(
            metric_value={
                "silhouette_score": {
                    "silhouette_score": silhouette_avg,
                },
            },
            figures=figures,
        )

    def summary(self, metric_value):
        """
        Build one table for summarizing the Silhouette score results
        """
        silhouette_score = metric_value["silhouette_score"]

        table = []
        table.append(silhouette_score)
        return ResultSummary(
            results=[
                ResultTable(
                    data=table,
                    metadata=ResultTableMetadata(title="Silhouette Score"),
                ),
            ]
        )
