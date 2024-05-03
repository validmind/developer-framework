# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_precision


def ContextPrecision(
    dataset,
    question_column="question",
    answer_column="answer",
    ground_truth_column="ground_truth",
    contexts_column="contexts",
):
    required_columns = [
        question_column,
        answer_column,
        ground_truth_column,
        contexts_column,
    ]
    result = evaluate(
        Dataset.from_pandas(dataset.df[required_columns]), metrics=[context_precision]
    )

    return result.to_pandas()["context_precision"].to_list()
