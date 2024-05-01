# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_relevancy


def ContextRelevancy(dataset):
    result = evaluate(Dataset.from_pandas(dataset._df), metrics=[context_relevancy])

    return result.to_pandas()["context_relevancy"].to_list()
