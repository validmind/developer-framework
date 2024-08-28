# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.spatial.distance import cdist
from sklearn.metrics import silhouette_score

from validmind.errors import SkipTestError
from validmind.vm_models import Figure, Metric


@dataclass
class KMeansClustersOptimization(Metric):
    """
    Optimizes the number of clusters in K-means models using Elbow and Silhouette methods.

    ### Purpose

    This metric is used to optimize the number of clusters used in K-means clustering models. It intends to measure and
    evaluate the optimal number of clusters by leveraging two methodologies, namely the Elbow method and the Silhouette
    method. This is crucial as an inappropriate number of clusters can either overly simplify or overcomplicate the
    structure of the data, thereby undermining the effectiveness of the model.

    ### Test Mechanism

    The test mechanism involves iterating over a predefined range of cluster numbers and applying both the Elbow method
    and the Silhouette method. The Elbow method computes the sum of the minimum euclidean distances between data points
    and their respective cluster centers (distortion). This value decreases as the number of clusters increases; the
    optimal number is typically at the 'elbow' point where the decrease in distortion becomes less pronounced.
    Meanwhile, the Silhouette method calculates the average silhouette score for each data point in the dataset,
    providing a measure of how similar each item is to its own cluster compared to other clusters. The optimal number
    of clusters under this method is the one that maximizes the average silhouette score. The results of both methods
    are plotted for visual inspection.

    ### Signs of High Risk

    - A high distortion value or a low silhouette average score for the optimal number of clusters.
    - No clear 'elbow' point or plateau observed in the distortion plot, or a uniformly low silhouette average score
    across different numbers of clusters, suggesting the data is not amenable to clustering.
    - An optimal cluster number that is unreasonably high or low, suggestive of overfitting or underfitting,
    respectively.

    ### Strengths

    - Provides both a visual and quantitative method to determine the optimal number of clusters.
    - Leverages two different methods (Elbow and Silhouette), thereby affording robustness and versatility in assessing
    the data's clusterability.
    - Facilitates improved model performance by allowing for an informed selection of the number of clusters.

    ### Limitations

    - Assumes that a suitable number of clusters exists in the data, which may not always be true, especially for
    complex or noisy data.
    - Both methods may fail to provide definitive answers when the data lacks clear cluster structures.
    - Might not be straightforward to determine the 'elbow' point or maximize the silhouette average score, especially
    in larger and complicated datasets.
    - Assumes spherical clusters (due to using the Euclidean distance in the Elbow method), which might not align with
    the actual structure of the data.
    """

    name = "clusters_optimize_elbow_method"
    required_inputs = ["model", "dataset"]
    tasks = ["clustering"]
    tags = ["sklearn", "model_performance", "kmeans"]

    default_params = {"n_clusters": None}

    def run(self):
        n_clusters = self.params["n_clusters"]
        if n_clusters is None:
            raise SkipTestError("n_clusters parameter must be provide in list format")
        model = self.inputs.model.model

        distortions = {}
        silhouette_avg = {}

        for k in n_clusters:
            # Building and fitting the model
            kmeanModel = model.set_params(n_clusters=k)
            kmeanModel = kmeanModel.fit(self.inputs.dataset.x)
            # Calculate silhouette coefficients for each data point
            silhouette_avg[k] = silhouette_score(
                self.inputs.dataset.x,
                kmeanModel.predict(self.inputs.dataset.x),
            )

            distortions[k] = (
                sum(
                    np.min(
                        cdist(
                            self.inputs.dataset.x,
                            kmeanModel.cluster_centers_,
                            "euclidean",
                        ),
                        axis=1,
                    )
                )
                / self.inputs.dataset.x.shape[0]
            )
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=(
                "The Silhouette value of each cluster",
                "The Elbow Method using Distortion",
            ),
        )

        fig.add_trace(
            go.Scatter(x=list(silhouette_avg.keys()), y=list(silhouette_avg.values())),
            row=1,
            col=1,
        )
        fig.update_xaxes(title_text="Number of clusters", row=1, col=1)
        fig.update_yaxes(title_text="Avg Silhouette Score", row=1, col=1)

        fig.add_trace(
            go.Scatter(x=list(distortions.keys()), y=list(distortions.values())),
            row=1,
            col=2,
        )
        # Update xaxis properties
        fig.update_xaxes(title_text="Number of clusters", showgrid=False, row=1, col=2)
        fig.update_yaxes(title_text="Distortion", showgrid=False, row=1, col=2)

        fig.update_layout(showlegend=False)

        figures = [
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        ]

        return self.cache_results(figures=figures)
