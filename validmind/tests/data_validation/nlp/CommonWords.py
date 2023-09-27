# Copyright © 2023 ValidMind Inc. All rights reserved.

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
    **Purpose**: The CommonWords metric is used to identify and visualize the most prevalent words within a specified
    text column of a dataset, giving insights into the prevalent language patterns and vocabulary. This is particularly
    useful for Natural Language Processing (NLP) tasks such as text classification and text summarization.

    **Test Mechanism**: The methodology for this test involves splitting the specified text column's entries into words
    and collating them into a corpus. Subsequently, the frequency of each word is counted using Counter functionality.
    The forty most commonly occurring words that aren't categorized as English stopwords are then visualized in a bar
    chart. The x-axis shows formulated words and the y-axis indicates their frequency of appearance.

    **Signs of High Risk**: Indicators of high risk may include a lack of distinct words within the list, or common
    words primarily encompassing stopwords. In addition, the frequent appearance of irrelevant or inappropriate words
    could indicate a poorly curated or noisy data set. Lastly, if the test returns an error due to the absence of a
    valid Dataset object, it signifies a high risk as it can't be effectively implemented.

    **Strengths**: This metric offers a clear insight into the language features – specifically, the word frequency –
    of unstructured text data. It can reveal prominent vocabulary and language patterns, which can be vital for
    effective feature extraction in NLP tasks. The visualization aspect aids in quickly capturing the patterns and
    getting an intuitive feel of the data.

    **Limitations**: This test is solely focused on word frequency and disregards semantic or context-related
    information. It deliberately ignores stopwords, which, in some cases, might carry important significance.
    Furthermore, it may only be applicable to English language text data as it uses English stopwords for filtering,
    and does not account for data in other languages. The metric also requires a valid Dataset object, indicating a
    dependency condition that limits applicability.
    """

    name = "common_words"
    required_inputs = ["dataset", "dataset.text_column"]
    metadata = {
        "task_types": ["text_classification", "text_summarization"],
        "tags": ["nlp", "text_data", "visualization", "frequency_analysis"],
    }

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
