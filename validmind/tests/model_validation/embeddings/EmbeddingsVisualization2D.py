# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.express as px
from sklearn.manifold import TSNE

from validmind.vm_models import Figure, Metric


class EmbeddingsVisualization2D(Metric):
    """
    Analyze the embeddings produced by a text embedding model using 2D visualization
    """

    name = "2D Visualization of Text Embeddings"
    required_inputs = ["model", "model.test_ds"]
    default_params = {
        "perplexity": 30,
    }
    metadata = {
        "task_types": ["feature_extraction"],
        "tags": ["llm", "text_data", "text_embeddings", "visualization"],
    }

    def run(self):
        # use TSNE to reduce dimensionality of embeddings
        num_samples = len(self.model.y_test_predict.values)

        if self.params["perplexity"] >= num_samples:
            perplexity = num_samples - 1
        else:
            perplexity = self.params["perplexity"]

        reduced_embeddings = TSNE(
            n_components=2,
            perplexity=perplexity,
        ).fit_transform(self.model.y_test_predict.values)

        # create a scatter plot from the reduced embeddings
        fig = px.scatter(
            x=reduced_embeddings[:, 0],
            y=reduced_embeddings[:, 1],
            title="2D Visualization of Text Embeddings",
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
