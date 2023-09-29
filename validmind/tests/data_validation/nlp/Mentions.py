# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""
import re
from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

from validmind.vm_models import Figure, ThresholdTest, VMDataset


@dataclass
class Mentions(ThresholdTest):
    """
    **Purpose**: The "Mentions" test focuses on the aspect of data quality in an NLP (Natural Language Processing) or
    text-based Machine Learning model. Its main objective is to identify and analyze the frequency of 'mentions' within
    a given dataset, particularly within a selected text column. 'Mentions' in this context are discrete elements of
    text that are preceded by '@'. The output would reveal the most frequently mentioned entities or usernames, which
    could be crucial to certain applications like social media analyses, customer sentiment analyses, etc.

    **Test Mechanism**: Upon validating the presence of a text column in the provided dataset, this test applies a
    regular expression pattern to extract these mentions. The number of occurrences for each unique mention is then
    counted. The top mentions, based on user-specified parameters or by default the top 25, are selected for
    representation. This thresholding process forms the main mechanism of this test, showcasing high-frequency
    elements. The results are visually rendered in a treemap plot, wherein each rectangle's size is indicative of the
    corresponding mention's frequency.

    **Signs of High Risk**: Execution failure for this test could be linked to the absence of a valid text column in
    the dataset. One other indicators of high risk includes the absence of mentions in the text data, meaning that
    there might not be any text preceded by '@'. This conditions could indicate sparse or poor-quality data, affecting
    the model's ability to generalize or learn appropriately.

    **Strengths**: This test is specifically optimized for textual datasets, making it particularly powerful in NLP
    contexts. It allows rapid identification of dominant elements, displaying them visually for easy interpretation.
    This allows potentially pivotal insights about the most mentioned entities or usernames to be extracted.

    **Limitations**: This test can be limited by its dependence on '@' for the identification of mentions. Aspects of
    text not preceded by '@' could be potentially useful, but remain overlooked by this test. Additionally, this test
    is not suitable for datasets without textual data. The test doesn't present insights on less frequently occurring
    data or outliers, potentially leaving important patterns unrevealed.
    """

    name = "mentions"
    category = "data_quality"
    required_inputs = ["dataset", "dataset.text_column"]
    default_params = {"top_mentions": 25}
    metadata = {
        "task_types": ["text_classification", "text_summarization"],
        "tags": ["nlp", "text_data", "visualization", "frequency_analysis"],
    }

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.dataset, VMDataset):
            raise ValueError("Mentions requires a validmind Dataset object")

        text_column = self.dataset.text_column

        def mentions(text):
            line = re.findall(r"(?<=@)\w+", text)
            return " ".join(line)

        b = (
            self.dataset.df[text_column]
            .apply(lambda x: mentions(x))
            .value_counts()[:][1 : self.params["top_mentions"]]
            .index.tolist()
        )
        a = (
            self.dataset.df[text_column]
            .apply(lambda x: mentions(x))
            .value_counts()[:][1 : self.params["top_mentions"]]
            .tolist()
        )
        row = pd.DataFrame({"scenario": []})
        row["scenario"] = b
        row["Percentage"] = a
        figures = []
        if not row.empty:
            fig = px.treemap(
                row, path=["scenario"], values="Percentage", title="Tree of Mentions"
            )
            figures.append(
                Figure(
                    for_object=self,
                    key=self.name,
                    figure=fig,
                )
            )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return self.cache_results(
            [],
            passed=True,
            figures=figures,
        )
