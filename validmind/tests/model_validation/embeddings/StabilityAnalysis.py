# Copyright © 2023 ValidMind Inc. All rights reserved.

from abc import abstractmethod
from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


class StabilityAnalysis(ThresholdTest):
    """Base class for embeddings stability analysis tests"""

    category = "model_diagnosis"
    required_inputs = ["model", "model.test_ds"]
    default_params = {
        "mean_distance_threshold": 0.1,
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
                "Mean Distance": result.values["mean_distance"],
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
        col = self.model.test_ds.text_column
        perturbed_data_df = self.model.test_ds.df.copy()
        perturbed_data_df[col] = perturbed_data_df[col].apply(self.perturb_data)

        # Compute embeddings for the perturbed dataset
        perturbed_embeddings = self.model.predict(perturbed_data_df)

        # Compute cosine similarities between original and perturbed embeddings
        similarities = cosine_similarity(
            self.model.y_test_predict.values,
            perturbed_embeddings,
        ).diagonal()

        # Determine if the test passed based on the mean distance and threshold
        mean_distance = np.mean(1 - similarities)
        passed = mean_distance < self.params["mean_distance_threshold"]

        # For this example, we are not caching the results as done in the reference `run` method
        return self.cache_results(
            [
                ThresholdTestResult(
                    passed=passed,
                    values={
                        "mean_distance": mean_distance,
                    },
                )
            ],
            passed=passed,
        )
