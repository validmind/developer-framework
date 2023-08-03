# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Metrics functions for any Pandas-compatible datasets
"""

from collections import Counter
from dataclasses import dataclass
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

from ....vm_models import (
    Figure,
    Metric,
    VMDataset,
)


@dataclass
class CommonWords(Metric):
    name = "common_words"
    required_context = ["dataset", "dataset.text_column"]

    def description(self):
        return """The purpose of the common words test is to analyze a dataset and identify the most common
        words within a specified text column.
        This test allows users to understand the prevalent words within the dataset's text column and gain
        insights into the dataset's language patterns."""

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("CommonWords requires a validmind Dataset object")

        def create_corpus(df, text_column):
            corpus = []
            for x in df[text_column].str.split():
                for i in x:
                    corpus.append(i)
            return corpus

        text_column = self.dataset.text_column
        corpus = create_corpus(self.dataset.df, text_column=text_column)

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
