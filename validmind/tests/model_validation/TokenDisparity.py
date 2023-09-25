# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from transformers import BertTokenizer

from validmind.vm_models import Figure, Metric


@dataclass
class TokenDisparity(Metric):
    """
    Token disparity histogram
    """

    name = "token_disparity"
    required_inputs = ["model", "model.test_ds"]

    def description(self):
        return """
        """

    def run(self):
        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict

        df = pd.DataFrame({"reference_column": y_true, "generated_column": y_pred})

        fig = self.token_disparity_histograms(df)
        figures = []
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )
        return self.cache_results(figures=figures)

    def token_disparity_histograms(self, df):
        """
        Visualize the token counts distribution of two given columns using histograms.

        :param df: DataFrame containing the text columns.
        :param params: Dictionary with the keys ["reference_column", "generated_column"].
        """

        reference_column = "reference_column"
        generated_column = "generated_column"

        # Initialize the tokenizer
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        # Tokenize the columns and get the number of tokens
        df["tokens_1"] = df[reference_column].apply(
            lambda x: len(tokenizer.tokenize(x))
        )
        df["tokens_2"] = df[generated_column].apply(
            lambda x: len(tokenizer.tokenize(x))
        )

        # Create subplots: 1 row, 2 columns
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=(
                f"Tokens in {reference_column}",
                f"Tokens in {generated_column}",
            ),
        )

        # Add histograms
        fig.add_trace(
            go.Histogram(
                x=df["tokens_1"],
                marker_color="blue",
                name=f"Tokens in {reference_column}",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Histogram(
                x=df["tokens_2"],
                marker_color="red",
                name=f"Tokens in {generated_column}",
            ),
            row=1,
            col=2,
        )

        # Update layout
        fig.update_layout(title_text="Token Distributions", bargap=0.1)

        fig.update_yaxes(title_text="Number of Documents")
        fig.update_xaxes(title_text="Number of Tokens", row=1, col=1)
        fig.update_xaxes(title_text="Number of Tokens", row=1, col=2)

        return fig
