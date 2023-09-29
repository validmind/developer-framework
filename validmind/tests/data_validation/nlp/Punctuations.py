# Copyright © 2023 ValidMind Inc. All rights reserved.

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
    **1. Purpose:** The main goal of the Punctuations Metric is to analyze the frequency of punctuation usage within a
    given text dataset. This heuristic is often used in Natural Language Processing tasks such as text classification
    and text summarization.

    **2. Test Mechanism:** The test begins by checking the input's eligibility, specifying that the "dataset" must be
    of a VMDataset type. The next step is to create a corpus of the dataset by splitting the text of the input dataset
    on spaces. Then, it tallies the usage of each unique punctuation character in the text corpus. The distribution of
    the frequencies of each punctuation symbol is subsequently depicted as a bar graph. Results are stored as Figures
    and associated with the main Punctuations object.

    **3. Signs of High Risk:** Given the nature of the test, risks are typically associated with the quality of text
    data. One sign of high risk might be an excessive or unusual frequency of certain punctuation marks, which may
    denote dubious quality, data corruption, or skewed data.

    **4. Strengths:** The primary strength of this metric is providing insights into the distribution of punctuation
    use in a text dataset. This could be valuable in validating the quality, consistency, and nature of data. It could
    also offer hints about the style or tonality of the text corpus (e.g., frequent exclamation use might signify a
    more informal, emotional context).

    **5. Limitations:** This test exclusively looks at punctuation usage and thus can overlook other crucial text
    characteristics. Additionally, it’s crucial not to make broad cultural or tonality assumptions based solely on
    punctuation distribution since these may vary widely across different languages and contexts. It may also be less
    effective when dealing with languages that employ non-standard or different punctuation. Finally, the visualized
    results may lack interpretability when there are many unique punctuation marks in the dataset.
    """

    name = "punctuations"
    required_inputs = ["dataset", "dataset.text_column"]
    metadata = {
        "task_types": ["text_classification", "text_summarization"],
        "tags": ["nlp", "text_data", "visualization", "frequency_analysis"],
    }

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
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
