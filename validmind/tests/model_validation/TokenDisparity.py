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
    **Purpose**: The purpose of the Token Disparity metric is to evaluate the distributional match between the
    predicted and actual outputs (tokens) of the model. This is done by creating a comparison through histograms that
    outline the disparity in the number of tokens in both columns. The metric is also used to assess the verbosity of
    the model's predictions in comparison to the actual data.

    **Test Mechanism**: The test is implemented by tokenizing the two columns: one for the real data and the other for
    the generated or predicted data. It uses the BERT tokenizer to tokenize the content of each column. Then, it counts
    the tokens in each column. These counts are then arranged into two different histograms to visualize the
    distribution of token counts in the real data and the generated data. The metric quantifies the distribution
    disparity by comparing the histogram of the true tokens with the histogram of predicted tokens.

    **Signs of High Risk**: High risk or failures might be indicated by significant differences in distribution
    typologies between the two histograms, especially if the predicted histogram considerably diverges from the
    reference histogram. It may signify that the model is generating outputs with unexpected verbosity, resulting in
    either far too many or too few tokens than expected.

    **Strengths**: The primary strength of this metric is that it provides a clear and visual comparison of predicted
    versus actual token distributions in the model. It helps in understanding the consistency and quality of the
    model's output in terms of length and verbosity. It also allows detection of potential issues in the model's output
    generation capabilities, such as over-generation or under-generation of tokens compared to the actual data.

    **Limitations**: This metric focuses strictly on the count of tokens without considering the semantics behind the
    tokens. Therefore, it may overlook issues related to the meaningfulness or relevance of the produced tokens.
    Furthermore, it assumes that a similar distribution of token counts between predicted and actual data implies
    accurate output, which may not always hold true. Also, it depends on the BERT tokenizer which may not be the best
    tokenizer for all kinds of text data.
    """

    name = "token_disparity"
    required_inputs = ["model", "model.test_ds"]

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
