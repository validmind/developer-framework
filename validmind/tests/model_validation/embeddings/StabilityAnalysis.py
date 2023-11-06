# Copyright © 2023 ValidMind Inc. All rights reserved.

from abc import abstractmethod
from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


class StabilityAnalysis(ThresholdTest):
    """Base class for embeddings stability analysis tests"""

    category = "model_diagnosis"
    required_inputs = ["model", "dataset"]
    default_params = {
        "text_column": None,
        "mean_similarity_threshold": 0.7,
    }
    metadata = {
        "task_types": ["feature_extraction"],
        "tags": ["llm", "text_data", "text_embeddings", "visualization"],
    }

    @abstractmethod
    def perturb_data(self, data: str) -> str:
        """Perturb a string of text (overriden by subclasses)"""
        pass

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        results_table = [
            {
                "Mean Similarity": result.values["mean_similarity"],
                "Min Similarity": result.values["min_similarity"],
                "Max Similarity": result.values["max_similarity"],
                "Median Similarity": result.values["median_similarity"],
                "Std Similarity": result.values["std_similarity"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="Stability Analysis Results for Embeddings Model"
                    ),
                )
            ]
        )

    def run(self):
        # Perturb the test dataset
        col = self.params.get("text_column")

        if col is None:
            raise ValueError(
                "The `text_column` parameter must be provided to the StabilityAnalysis test."
            )

        original_data_df = self.dataset.df[col]
        perturbed_data_df = original_data_df.copy()
        perturbed_data_df = perturbed_data_df.apply(self.perturb_data)

        # Compute embeddings for the original and perturbed dataset
        original_embeddings = self.model.predict(original_data_df)
        perturbed_embeddings = self.model.predict(perturbed_data_df)

        # Compute cosine similarities between original and perturbed embeddings
        similarities = cosine_similarity(
            original_embeddings,
            perturbed_embeddings,
        ).diagonal()

        mean = np.mean(similarities)
        min = np.min(similarities)
        max = np.max(similarities)
        median = np.median(similarities)
        std = np.std(similarities)

        # Determine if the test passed based on the mean similarity and threshold
        passed = mean > self.params["mean_similarity_threshold"]

        # Plot the distribution of cosine similarities using plotly
        import plotly.express as px

        fig = px.histogram(
            x=similarities.flatten(),
            nbins=100,
            title="Cosine Similarity Distribution",
            labels={"x": "Cosine Similarity"},
        )

        # For this example, we are not caching the results as done in the reference `run` method
        return self.cache_results(
            [
                ThresholdTestResult(
                    passed=passed,
                    values={
                        "mean_similarity": mean,
                        "min_similarity": min,
                        "max_similarity": max,
                        "median_similarity": median,
                        "std_similarity": std,
                    },
                )
            ],
            figures=[
                Figure(
                    for_object=self,
                    key=self.name,
                    figure=fig,
                )
            ],
            passed=passed,
        )
