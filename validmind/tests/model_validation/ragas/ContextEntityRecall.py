# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import context_entity_recall


def ContextEntityRecall(dataset):
    result = evaluate(Dataset.from_pandas(dataset._df), metrics=[context_entity_recall])

    return result.to_pandas()["context_entity_recall"].to_list()
