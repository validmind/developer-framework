# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""

from collections import defaultdict
from typing import List
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

from validmind.vm_models import (
    VMDataset,
    TestResult,
    Figure,
    ThresholdTest,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)


@dataclass
class StopWords(ThresholdTest):

    category = "data_quality"
    name = "stop_words"
    required_context = ["dataset"]
    default_params = {"min_percent_threshold": 0.5, "num_words": 25}

    def description(self):
        return """The purpose of the StopWords test is to perform a data quality test focused on identifying and analyzing
        the usage of stop words within a dataset. Stop words are commonly used words in a language (e.g., "the", "and", "is")
        that are often considered insignificant for analysis.
        The StopWords test analyzes the dataset by creating a corpus of words from the specified text column.
        It then determines the frequency of each stop word in the corpus and calculates the percentage of each stop word in
        relation to the total number of words. The test results focus on identifying the top stop words based on their
        percentage in the corpus."""

    def summary(self, results: List[TestResult], all_passed: bool):

        # Create a DataFrame from the data
        df = pd.DataFrame(results[0].values, columns=["Word", "Percentage"])

        return ResultSummary(
            results=[
                ResultTable(
                    data=df,
                    metadata=ResultTableMetadata(
                        title=f"Class Imbalance Results for Column {self.dataset.target_column}"
                    ),
                )
            ]
        )

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("ClassImbalance requires a validmind Dataset object")

        text_column = self.dataset.text_column

        def create_corpus(df, text_column):
            corpus = []
            for x in df[text_column].str.split():
                for i in x:
                    corpus.append(i)
            return corpus

        corpus = create_corpus(self.dataset.df, text_column=text_column)

        nltk.download("stopwords")
        stop = set(stopwords.words("english"))
        dic = defaultdict(int)
        for word in corpus:
            if word in stop:
                dic[word] += 1
        # Calculate the total number of words in the corpus
        total_words = len(corpus)

        # Calculate the percentage of each word in the corpus
        word_percentages = {}
        for word, count in dic.items():
            percentage = (count / total_words) * 100
            word_percentages[word] = percentage

        passed = all(word_percentages.values()) < self.params["min_percent_threshold"]
        top = sorted(word_percentages.items(), key=lambda x: x[1], reverse=True)[
            : self.params["num_words"]
        ]

        test_results = [
            TestResult(
                passed=passed,
                values=top,
            )
        ]
        figures = []
        if top:
            fig, _ = plt.subplots()
            x, y = zip(*top)
            plt.bar(x, y)
            plt.xticks(rotation=90)

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures = []
            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}",
                    figure=fig,
                )
            )

        return self.cache_results(test_results, passed=passed, figures=figures)
