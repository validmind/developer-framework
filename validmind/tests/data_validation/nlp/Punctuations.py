# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Metrics functions for any Pandas-compatible datasets
"""

from collections import defaultdict
from dataclasses import dataclass
import string
import matplotlib.pyplot as plt

from validmind.vm_models import (
    Figure,
    Metric,
    Dataset,
)


@dataclass
class Punctuations(Metric):
    name = "punctuations"
    required_context = ["dataset", "dataset.text_column"]

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, Dataset):
            raise ValueError("Punctuations requires a validmind Dataset object")

        def create_corpus(df, text_column):
            corpus = []
            for x in df[text_column].str.split():
                for i in x:
                    corpus.append(i)
            return corpus

        text_column = self.dataset.text_column
        corpus = create_corpus(self.dataset.df, text_column=text_column)

        dic = defaultdict(int)
        special = string.punctuation
        for i in corpus:
            if i in special:
                dic[i] += 1

        fig = plt.figure()
        x, y = zip(*dic.items())
        plt.bar(x, y, color="#17C37B")

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return self.cache_results(
            figures=[
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                )
            ]
        )
