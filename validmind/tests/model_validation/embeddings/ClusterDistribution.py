# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.express as px
from sklearn.cluster import KMeans

from validmind.vm_models import Figure, Metric


class ClusterDistribution(Metric):
    """
    Analyze the distribution of the clusters produced by a text embedding model
    """

    name = "Text Embeddings Cluster Distribution"
    required_inputs = ["model", "model.test_ds"]
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
            self.model.y_test_predict.values
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
