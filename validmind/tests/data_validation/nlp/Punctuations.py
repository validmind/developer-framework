# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Metrics functions for any Pandas-compatible datasets
"""

import string
from collections import defaultdict
from dataclasses import dataclass

import matplotlib.pyplot as plt

from validmind.vm_models import Figure, Metric, VMDataset


@dataclass
class Punctuations(Metric):
    """
    Analyzes and visualizes the frequency distribution of punctuation usage in a given text dataset.

    **1. Purpose:** The Punctuations Metric's primary purpose is to analyze the frequency of punctuation usage within a
    given text dataset. This is often used in Natural Language Processing tasks, such as text classification and text
    summarization.

    **2. Test Mechanism:** The test begins by verifying that the input "dataset" is of the type VMDataset. Following
    that, a corpus is created from the dataset by splitting its text on spaces. Each unique punctuation character in
    the text corpus is then tallied. Then, the frequency distribution of each punctuation symbol is visualized as a bar
    graph, with these results being stored as Figures and associated with the main Punctuations object.

    **3. Signs of High Risk:**

    - High risk can be indicated by the excessive or unusual frequency of specific punctuation marks, potentially
    denoting dubious quality, data corruption, or skewed data.

    **4. Strengths:**

    - The Punctuations Metric provides valuable insights into the distribution of punctuation usage in a text dataset.
    - This insight can be important in validating the quality, consistency, and nature of the data.
    - It can provide hints about the style or tonality of the text corpus. For example, frequent usage of exclamation
    marks may suggest a more informal and emotional context.

    **5. Limitations:**

    - The metric focuses solely on punctuation usage and can miss other important textual characteristics.
    - It's important not to make general cultural or tonality assumptions based solely on punctuation distribution,
    since these can vary greatly across different languages and contexts.
    - The metric may be less effective with languages that use non-standard or different punctuation.
    - The visualization may lack interpretability when there are many unique punctuation marks in the dataset.
    """

    name = "punctuations"
    required_inputs = ["dataset"]
    tasks = ["text_classification", "text_summarization"]
    tags = ["nlp", "text_data", "visualization", "frequency_analysis"]

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.inputs.dataset, VMDataset):
            raise ValueError("Punctuations requires a validmind Dataset object")

        def create_corpus(df, text_column):
            corpus = []
            for x in df[text_column].str.split():
                for i in x:
                    corpus.append(i)
            return corpus

        text_column = self.inputs.dataset.text_column
        corpus = create_corpus(self.inputs.dataset.df, text_column=text_column)

        special = string.punctuation
        dic = defaultdict(int, {key: 0 for key in special})
        for i in corpus:
            if i in special:
                dic[i] += 1
        figures = []
        # if dic:
        fig = plt.figure()
        x, y = zip(*dic.items())
        plt.bar(x, y, color="#17C37B")
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )
        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return self.cache_results(figures=figures)
