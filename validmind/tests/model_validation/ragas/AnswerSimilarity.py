# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_similarity

from validmind.vm_models import Metric, ResultSummary, ResultTable


@dataclass
class AnswerSimilarity(Metric):

    name = "answer_similarity"
    required_inputs = ["model", "dataset"]
    default_params = {
        "question": "question",
        "answer": "answer",
        "ground_truth": "ground_truth",
        "contexts": "contexts",
    }

    def summary(self, metric_value):
        return ResultSummary(
            results=[
                ResultTable(data=metric_value),
            ]
        )

    def run(self):
        df = self.inputs.dataset.df
        Dataset.from_pandas(df)
        dataset = df[
            [
                self.params["question"],
                self.params["answer"],
                self.params["ground_truth"],
                self.params["contexts"],
            ]
        ]
        dataset = Dataset.from_pandas(dataset)
        score = evaluate(dataset, metrics=[answer_similarity])
        result = score.to_pandas()
        result = result.drop(columns=["__index_level_0__"])

        return self.cache_results(metric_value=result)
