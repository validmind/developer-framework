# Copyright © 2023 ValidMind Inc. All rights reserved.

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
    VMDataset,
)


@dataclass
class StopWords(ThresholdTest):
    """
    **Purpose**: The StopWords test is a data quality assessment tool specifically designed for text data. It
    identifies and analyzes the usage of 'stop words' within a dataset. Stop words are frequent, common words in a
    language (e.g., "the", "and", "is"), which are typically considered insignificant for in-depth analysis. The test
    quantifies the frequency of each stop word in the dataset, further calculating their proportional usage compared to
    the total word count. Ultimately, it aims to highlight the prevailing stop words based on their usage frequency.

    **Test Mechanism**: The test triggers once it receives a 'VMDataset' object; in absence of which, it raises an
    error. The text column of the dataset undergoes an inspection for the creation of a 'corpus' (a collection of
    written texts representing the dataset). With the help of Natural Language Toolkit's (NLTK) stop word repository,
    the test screens the corpus for any stop words and logs their frequency. Each stop word, expressed as a percentage
    usage out of the total corpus, is compared against a 'min_percent_threshold'. If the percentage exceeds this
    threshold, the test is deemed as failed. The test returns the top prevailing stop words, decided by the 'num_words'
    parameter, and their percentages. It also provides a bar chart visualization of the top stop words and their usage
    frequency for intuitive understanding.

    **Signs of High Risk**: Potential signs indicating high risk are if the percentage of any stop words exceeds the
    predefined 'min_percent_threshold' and the application's context where a major presence of stop words could
    negatively impact the analytical performance due to noise generation.

    **Strengths**: The main strengths of the StopWords test include its ability to scrutinize and quantify the usage of
    stop words in a dataset, which might often be overlooked due to their insignificant semantic meaning. The test
    gives insights into potential noise in the text data, which could interfere with model training efficiency.
    Furthermore, the bar chart visualization provided by the test facilitates readily interpretable and actionable
    insights.

    **Limitations**: While robust for stop word analysis, the test does exhibit a few limitations. It only works with
    English stop words and therefore may not perform well on datasets in other languages. The effectiveness of the test
    depends on the 'min_percent_threshold', which might need to be fine-tuned for different datasets. Additionally, the
    test does not consider the context of the stop words used within the dataset, and hence, it might overlook their
    significance if used in certain contexts. Lastly, the test checks only the frequency of stop words and does not
    offer direct measures of model performance or predictive accuracy.
    """

    category = "data_quality"
    name = "stop_words"
    required_inputs = ["dataset"]
    default_params = {"min_percent_threshold": 0.5, "num_words": 25}
    metadata = {
        "task_types": ["text_classification", "text_summarization"],
        "tags": ["nlp", "text_data", "visualization", "frequency_analysis"],
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):

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
