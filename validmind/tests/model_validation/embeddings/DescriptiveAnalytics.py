# Copyright © 2023 ValidMind Inc. All rights reserved.

import plotly.express as px

from validmind.vm_models import Figure, Metric


class DescriptiveAnalytics(Metric):
    """
    Goal: Understand basic properties and statistics of the embeddings.

    Dimensionality: Document the size of the embeddings.
    Distributions: Plot distributions of mean, median, and standard deviation of
    embedding values. This can give insight into any strange patterns or values.
    """

    name = "Descriptive Analytics for Text Embeddings Models"
    required_inputs = ["model", "model.test_ds"]
    metadata = {
        "task_types": ["feature_extraction"],
        "tags": ["llm", "text_data", "text_embeddings", "visualization"],
    }

    def run(self):
        mean = self.model.y_test_predict.mean(axis=1)
        median = self.model.y_test_predict.median(axis=1)
        std = self.model.y_test_predict.std(axis=1)

        return self.cache_results(
            figures=[
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=px.histogram(mean, title="Distribution of Embedding Means"),
                ),
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=px.histogram(
                        median, title="Distribution of Embedding Medians"
                    ),
                ),
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=px.histogram(
                        std, title="Distribution of Embedding Standard Deviations"
                    ),
                ),
            ],
        )
