# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
    Calculates and visualizes frequencies of '@' prefixed mentions in a text-based dataset for NLP model analysis.

    ### Purpose

    The "Mentions" test is designed to gauge the quality of data in a Natural Language Processing (NLP) or text-focused
    Machine Learning model. The primary objective is to identify and calculate the frequency of 'mentions' within a
    chosen text column of a dataset. A 'mention' in this context refers to individual text elements that are prefixed
    by '@'. The output of this test reveals the most frequently mentioned entities or usernames, which can be integral
    for applications such as social media analyses or customer sentiment analyses.

    ### Test Mechanism

    The test first verifies the existence of a text column in the provided dataset. It then employs a regular
    expression pattern to extract mentions from the text. Subsequently, the frequency of each unique mention is
    calculated. The test selects the most frequent mentions based on default or user-defined parameters, the default
    being the top 25, for representation. This process of thresholding forms the core of the test. A treemap plot
    visualizes the test results, where the size of each rectangle corresponds to the frequency of a particular mention.

    ### Signs of High Risk

    - The lack of a valid text column in the dataset, which would result in the failure of the test execution.
    - The absence of any mentions within the text data, indicating that there might not be any text associated with
    '@'. This situation could point toward sparse or poor-quality data, thereby hampering the model's generalization or
    learning capabilities.

    ### Strengths

    - The test is specifically optimized for text-based datasets which gives it distinct power in the context of NLP.
    - It enables quick identification and visually appealing representation of the predominant elements or mentions.
    - It can provide crucial insights about the most frequently mentioned entities or usernames.

    ### Limitations

    - The test only recognizes mentions that are prefixed by '@', hence useful textual aspects not preceded by '@'
    might be ignored.
    - This test isn't suited for datasets devoid of textual data.
    - It does not provide insights on less frequently occurring data or outliers, which means potentially significant
    patterns could be overlooked.
    """

    name = "mentions"

    required_inputs = ["dataset"]
    default_params = {"top_mentions": 25}
    tasks = ["text_classification", "text_summarization"]
    tags = ["nlp", "text_data", "visualization", "frequency_analysis"]

    def run(self):
        # Can only run this test if we have a Dataset object
        if not isinstance(self.inputs.dataset, VMDataset):
            raise ValueError("Mentions requires a validmind Dataset object")

        text_column = self.inputs.dataset.text_column

        def mentions(text):
            line = re.findall(r"(?<=@)\w+", text)
            return " ".join(line)

        b = (
            self.inputs.dataset.df[text_column]
            .apply(lambda x: mentions(x))
            .value_counts()[:][1 : self.params["top_mentions"]]
            .index.tolist()
        )
        a = (
            self.inputs.dataset.df[text_column]
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
