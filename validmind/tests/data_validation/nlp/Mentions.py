# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Threshold based tests
"""
import re
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from validmind.vm_models import (
    VMDataset,
    Figure,
    ThresholdTest,
)


@dataclass
class Mentions(ThresholdTest):
    name = "mentions"
    category = "data_quality"
    required_context = ["dataset", "dataset.text_column"]
    default_params = {"top_mentions": 25}

    def description(self):
        return """The purpose of the Mentions test is to perform a data quality test focused on analyzing mentions within a dataset.
        It aims to identify the most frequently mentioned entities or usernames in a given text column and provides a visual representation
        of the results using a treemap.
        The Mentions test analyzes the dataset by extracting the text column and applying a regular expression pattern to identify mentions
        (text preceded by '@') within the text. It then counts the occurrences of each mention and selects the top mentions based on a specified
        parameter or the default value. The results are visualized using a treemap plot, where the size of each rectangle represents the
        frequency of the mention."""

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
        fig = px.treemap(
            row, path=["scenario"], values="Percentage", title="Tree of Mentions"
        )

        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return self.cache_results(
            [],
            passed=True,
            figures=[
                Figure(
                    for_object=self,
                    key=self.name,
                    figure=fig,
                )
            ],
        )
