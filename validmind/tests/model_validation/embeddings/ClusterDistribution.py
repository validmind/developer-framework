# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import plotly.express as px
from sklearn.cluster import KMeans

from validmind.vm_models import Figure, Metric


class ClusterDistribution(Metric):
    """
    Assesses the distribution of text embeddings across clusters produced by a model using KMeans clustering.

    **Purpose:** The purpose of this metric is to analyze the distribution of the clusters produced by a text embedding
    model. By dividing the text embeddings into different clusters, we can understand how the model is grouping or
    categorizing the text data. This aids in visualizing the organization and segregation of the data and thus gives an
    understanding of how the model is processing the data.

    **Test Mechanism:** The metric applies the KMeans clustering algorithm on the predictions made by the model on the
    testing dataset and divides the text embeddings into a pre-defined number of clusters. By default, this number is
    set to 5 but can be customized as per requirements. The output of this test is a histogram plot that shows the
    distribution of embeddings across these clusters.

    **Signs of High Risk:**

    - If the embeddings are skewed towards one or two clusters, that would indicate that the model is not effectively
    differentiating the various categories in the text data.
    - Uniform distribution of the embeddings across the clusters might show a lack of proper categorization.

    **Strengths:**

    - Great tool to visualize the text data categorization by the model. It provides a way to assess if the model is
    distinguishing the categories effectively or not.
    - It is flexible with the number of clusters (classes), so can be used on various types of data regardless of the
    number of categories.

    **Limitations:**

    - The success or failure of this test is based on visual interpretation, which might not be enough for making solid
    conclusions or determining the exact points of failure.
    - It assumes that the division of text embeddings across clusters should ideally be homogeneous, which might not
    always be the case depending on the nature of the text data.
    - It only applies to text embedding models, reducing its utility across various ML models.
    - This test uses the KMeans clustering algorithm, which assumes that clusters are convex and isotropic. Thus, this
    test may not work as intended if the true clusters in the data are not of this shape.
    """

    name = "Text Embeddings Cluster Distribution"
    required_inputs = ["model", "dataset"]
    default_params = {
        "num_clusters": 5,
    }
    metadata = {
        "task_types": ["feature_extraction"],
        "tags": ["llm", "text_data", "text_embeddings", "visualization"],
    }

    def run(self):
        # run kmeans clustering on embeddings
        kmeans = KMeans(n_clusters=self.params["num_clusters"]).fit(
            self.inputs.dataset.y_pred(self.inputs.model.input_id)
        )

        # plot the distribution
        fig = px.histogram(
            kmeans.labels_,
            nbins=self.params["num_clusters"],
            title="Embeddings Cluster Distribution",
        )

        return self.cache_results(
            figures=[
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                )
            ],
        )
