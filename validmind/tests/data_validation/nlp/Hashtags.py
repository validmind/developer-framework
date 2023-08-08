# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""

import re
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns

from validmind.vm_models import (
    VMDataset,
    Figure,
    ThresholdTest,
)


@dataclass
class Hashtags(ThresholdTest):
    """
    The purpose of this test is to identify and analyze the most frequently used hashtags in a given text column of a dataset.
    """

    category = "data_quality"
    name = "hashtags"
    required_context = ["dataset", "dataset.text_column"]
    default_params = {"top_hashtags": 25}

    def description(self):
        return """The Hashtags test analyzes the dataset by extracting the text column and applying a regular expression pattern
        to identify hashtags within the text. It then counts the occurrences of each hashtag and selects the top hashtags based
        on a specified parameter or the default value. The results are visualized using a bar plot, where the x-axis represents
        the hashtags and the y-axis represents their frequency counts.
        It aims to identify the most commonly used hashtags in a given text column and provide visual representation of their
        frequencies."""

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("Hashtags requires a validmind Dataset object")

        text_column = self.dataset.text_column

        def find_hash(text):
            line = re.findall(r"(?<=#)\w+", text)
            return " ".join(line)

        temp = (
            self.dataset.df[text_column]
            .apply(lambda x: find_hash(x))
            .value_counts()[:][1 : self.params["top_hashtags"]]
        )
        temp = (
            temp.to_frame()
            .reset_index()
            .rename(columns={"index": "Hashtag", text_column: "count"})
        )

        figures = []
        if not temp.empty:
            fig = plt.figure()
            sns.barplot(x="Hashtag", y="count", data=temp)
            plt.xticks(rotation=90)
            figures.append(
                Figure(
                    for_object=self,
                    key=self.name,
                    figure=fig,
                )
            )
            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

        return self.cache_results([], passed=True, figures=figures)
