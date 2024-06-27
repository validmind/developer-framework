# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from abc import abstractmethod
from typing import List

import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity

from validmind.logging import get_logger
from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)

logger = get_logger(__name__)


class StabilityAnalysis(ThresholdTest):
    """Base class for embeddings stability analysis tests"""

    required_inputs = ["model", "dataset"]
    default_params = {
        "mean_similarity_threshold": 0.7,
    }
    tasks = ["feature_extraction"]
    tags = ["llm", "text_data", "text_embeddings", "visualization"]

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
        original = self.inputs.dataset.df
        perturbed = original.copy()
        perturbed.update(
            perturbed.select_dtypes(include="object").applymap(self.perturb_data)
        )

        logger.debug(f"Original data: {original}")
        logger.debug(f"Perturbed data: {perturbed}")

        # Compute embeddings for the original and perturbed dataset
        original_embeddings = self.inputs.dataset.y_pred(self.inputs.model)
        perturbed_embeddings = np.stack(self.inputs.model.predict(perturbed))

        # Compute cosine similarities between original and perturbed embeddings
        similarities = cosine_similarity(
            original_embeddings, perturbed_embeddings
        ).diagonal()

        mean = np.mean(similarities)
        min = np.min(similarities)
        max = np.max(similarities)
        median = np.median(similarities)
        std = np.std(similarities)

        # Determine if the test passed based on the mean similarity and threshold
        passed = mean > self.params["mean_similarity_threshold"]

        figures = [
            px.histogram(
                x=similarities.flatten(),
                nbins=100,
                title="Cosine Similarity Distribution",
                labels={"x": "Cosine Similarity"},
            ),
            px.density_contour(
                x=similarities.flatten(),
                nbinsx=100,
                title="Cosine Similarity Density",
                labels={"x": "Cosine Similarity"},
                marginal_x="histogram",
            ),
            px.box(
                x=similarities.flatten(),
                labels={"x": "Cosine Similarity"},
                title="Cosine Similarity Box Plot",
            ),
        ]

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
                for fig in figures
            ],
            passed=passed,
        )
