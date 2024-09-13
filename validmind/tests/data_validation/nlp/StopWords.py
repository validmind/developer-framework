# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""
Threshold based tests
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk.corpus import stopwords

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class StopWords(ThresholdTest):
    """
    Evaluates and visualizes the frequency of English stop words in a text dataset against a defined threshold.

    ### Purpose

    The StopWords threshold test is a tool designed for assessing the quality of text data in an ML model. It focuses
    on the identification and analysis of "stop words" in a given dataset. Stop words are frequent, common, yet
    semantically insignificant words (for example: "the", "and", "is") in a language. This test evaluates the
    proportion of stop words to the total word count in the dataset, in essence, scrutinizing the frequency of stop
    word usage. The core objective is to highlight the prevalent stop words based on their usage frequency, which can
    be instrumental in cleaning the data from noise and improving ML model performance.

    ### Test Mechanism

    The StopWords test initiates on receiving an input of a 'VMDataset' object. Absence of such an object will trigger
    an error. The methodology involves inspection of the text column of the VMDataset to create a 'corpus' (a
    collection of written texts). Leveraging the Natural Language Toolkit's (NLTK) stop word repository, the test
    screens the corpus for any stop words and documents their frequency. It further calculates the percentage usage of
    each stop word compared to the total word count in the corpus. This percentage is evaluated against a predefined
    'min_percent_threshold'. If this threshold is breached, the test returns a failed output. Top prevailing stop words
    along with their usage percentages are returned, facilitated by a bar chart visualization of these stop words and
    their frequency.

    ### Signs of High Risk

    - A percentage of any stop words exceeding the predefined 'min_percent_threshold'.
    - High frequency of stop words in the dataset which may adversely affect the application's analytical performance
    due to noise creation.

    ### Strengths

    - The ability to scrutinize and quantify the usage of stop words.
    - Provides insights into potential noise in the text data due to stop words.
    - Directly aids in enhancing model training efficiency.
    - Includes a bar chart visualization feature to easily interpret and action upon the stop words frequency
    information.

    ### Limitations

    - The test only supports English stop words, making it less effective with datasets of other languages.
    - The 'min_percent_threshold' parameter may require fine-tuning for different datasets, impacting the overall
    effectiveness of the test.
    - Contextual use of the stop words within the dataset is not considered, potentially overlooking their significance
    in certain contexts.
    - The test focuses specifically on the frequency of stop words, not providing direct measures of model performance
    or predictive accuracy.
    """

    name = "stop_words"
    required_inputs = ["dataset"]
    default_params = {"min_percent_threshold": 0.5, "num_words": 25}
    tasks = ["text_classification", "text_summarization"]
    tags = ["nlp", "text_data", "visualization", "frequency_analysis"]

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        # Create a DataFrame from the data
        df = pd.DataFrame(results[0].values, columns=["Word", "Percentage"])

        return ResultSummary(
            results=[
                ResultTable(
                    data=df,
                    metadata=ResultTableMetadata(
                        title=f"Stop words results for column '{self.inputs.dataset.target_column}'"
                    ),
                )
            ]
        )

    def run(self):
        text_column = self.inputs.dataset.text_column

        def create_corpus(df, text_column):
            corpus = []
            for x in df[text_column].str.split():
                for i in x:
                    corpus.append(i)
            return corpus

        corpus = create_corpus(self.inputs.dataset.df, text_column=text_column)

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
            ThresholdTestResult(
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
