# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Metrics functions for any Pandas-compatible datasets
"""

from collections import Counter
from dataclasses import dataclass

import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

from ....vm_models import Figure, Metric, VMDataset


@dataclass
class CommonWords(Metric):
    """
    Assesses the most frequent non-stopwords in a text column for identifying prevalent language patterns.

    ### Purpose

    The CommonWords metric is used to identify and visualize the most prevalent words within a specified text column of
    a dataset. This provides insights into the prevalent language patterns and vocabulary, especially useful in Natural
    Language Processing (NLP) tasks such as text classification and text summarization.

    ### Test Mechanism

    The test methodology involves splitting the specified text column's entries into words, collating them into a
    corpus, and then counting the frequency of each word using the Counter. The forty most frequently occurring
    non-stopwords are then visualized in a bar chart, where the x-axis represents the words, and the y-axis indicates
    their frequency of occurrence.

    ### Signs of High Risk

    - A lack of distinct words within the list, or the most common words being stopwords.
    - Frequent occurrence of irrelevant or inappropriate words could point out a poorly curated or noisy dataset.
    - An error returned due to the absence of a valid Dataset object, indicating high risk as the metric cannot be
    effectively implemented without it.

    ### Strengths

    - The metric provides clear insights into the language features – specifically word frequency – of unstructured
    text data.
    - It can reveal prominent vocabulary and language patterns, which prove vital for feature extraction in NLP tasks.
    - The visualization helps in quickly capturing the patterns and understanding the data intuitively.

    ### Limitations

    - The test disregards semantic or context-related information as it solely focuses on word frequency.
    - It intentionally ignores stopwords, which might carry necessary significance in certain scenarios.
    - The applicability is limited to English-language text data as English stopwords are used for filtering, hence
    cannot account for data in other languages.
    - The metric requires a valid Dataset object, indicating a dependency condition that limits its broader
    applicability.
    """

    name = "common_words"
    required_inputs = ["dataset"]
    tasks = ["text_classification", "text_summarization"]
    tags = ["nlp", "text_data", "visualization", "frequency_analysis"]

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.inputs.dataset, VMDataset):
            raise ValueError("CommonWords requires a validmind Dataset object")

        def create_corpus(df, text_column):
            corpus = []
            for x in df[text_column].str.split():
                for i in x:
                    corpus.append(i)
            return corpus

        text_column = self.inputs.dataset.text_column
        corpus = create_corpus(self.inputs.dataset.df, text_column=text_column)

        counter = Counter(corpus)
        most = counter.most_common()
        x = []
        y = []
        nltk.download("stopwords")
        stop = set(stopwords.words("english"))
        for word, count in most[:40]:
            if word not in stop:
                x.append(word)
                y.append(count)
        fig = plt.figure()
        plt.bar(x, y, color="#17C37B")
        plt.xticks(rotation=90)
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
