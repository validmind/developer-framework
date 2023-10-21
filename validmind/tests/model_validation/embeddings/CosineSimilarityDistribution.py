# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity

from validmind.vm_models import Figure, Metric


class CosineSimilarityDistribution(Metric):
    """
    Compute the cosine similarity distribution between the embeddings produced by a
    text embedding model.
    """

    name = "Text Embeddings Cosine Similarity Distribution"
    required_inputs = ["model", "model.test_ds"]
    metadata = {
        "task_types": ["feature_extraction"],
        "tags": ["llm", "text_data", "text_embeddings", "visualization"],
    }

    def run(self):
        # Compute cosine similarity
        similarities = cosine_similarity(self.model.y_test_predict.values)

        # plot the distribution
        fig = px.histogram(
            x=similarities.flatten(),
            nbins=100,
            title="Cosine Similarity Distribution",
            labels={"x": "Cosine Similarity"},
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
