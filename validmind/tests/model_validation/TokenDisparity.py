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
    Assess and visualize token count disparity between model's predicted and actual dataset.

    **Purpose**:
    The Token Disparity metric is designed to assess the distributional congruence between the model's predicted
    outputs and the actual data. This is achieved by constructing histograms that illustrate the disparity in token
    count between the two columns. Additionally, this metric is used to measure the model's verbosity in comparison to
    the genuine dataset.

    **Test Mechanism**:
    The mechanism of running this test involves tokenizing both columns: one containing the actual data and the other
    containing the model's predictions. The BERT tokenizer is used for tokenizing the contents of each column. After
    tokenization, tokens in each column are counted and represented in two distinct histograms to facilitate the
    visualization of token count distribution in the actual and predicted data. To quantify the difference in
    distribution, the histogram of the actual tokens is compared with the histogram of the predicted tokens.

    **Signs of High Risk**:
    High risk or potential failure in model performance may be suggested by:

    - Significant incongruities in distribution patterns between the two histograms.
    - Marked divergence of the predicted histogram from the reference histogram, indicating that the model may be
    generating output with unexpected verbosity.
    - This might result in an output that has a significantly higher or lower number of tokens than expected.

    **Strengths**:
    Strengths of the Token Disparity metric include:

    - It provides a clear and visual comparison of predicted versus actual token distributions, enhancing understanding
    of the model's output consistency and verbosity.
    - It is able to detect potential issues with the model's output generation capability, such as over-production or
    under-production of tokens compared to the actual data set.

    **Limitations**:
    Limitations of the Token Disparity metric include:

    - The metric focuses solely on token count, disregarding the semantics behind those tokens. Consequently, it may
    miss out on issues related to relevance or meaningfulness of produced tokens.
    - The assumption that similar token count between predicted and actual data suggests accurate output, which is not
    always the case.
    - Dependence on the BERT tokenizer, which may not always be the optimum choice for all types of text data.
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
