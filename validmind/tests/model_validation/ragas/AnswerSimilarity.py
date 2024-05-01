# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_similarity


def AnswerSimilarity(dataset):
    result = evaluate(Dataset.from_pandas(dataset._df), metrics=[answer_similarity])

    return result.to_pandas()["answer_similarity"].to_list()
