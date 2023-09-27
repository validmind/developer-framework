# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import nltk
import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class ContextualRecall(Metric):
    """
    Contextual recall
    """

    name = "contextual_recall"
    required_inputs = ["model", "model.test_ds"]

    def description(self):
        return """
        Contextual recall is a metric used to evaluate the ability of a natural language generation (NLG)
        model to generate text that is consistent and coherent with a given context or prompt. It measures
        how well the generated text recalls or reflects the context provided. To compute contextual recall,
        you typically follow these steps:

        Prepare Reference and Candidate Texts:

        Gather your reference text(s), which represent the expected or desired output given a context or prompt.
        Generate candidate text(s) using your NLG model for the same context or prompt.
        Tokenization and Preprocessing:

        Tokenize both the reference and candidate texts into individual words or tokens. You can use libraries
        like NLTK or spaCy for this task.

        Compute Contextual Recall:
        Calculate the number of overlapping tokens (words or subword units) between the reference and candidate texts.
        Divide the number of overlapping tokens by the total number of tokens in the reference text to compute the
        contextual recall score.
        """

    def run(self):
        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict

        score_list = []
        for y_t, y_p in zip(y_true, y_pred):
            # Tokenize the reference and candidate texts
            reference_tokens = nltk.word_tokenize(y_t.lower())
            candidate_tokens = nltk.word_tokenize(y_p.lower())

            # Calculate overlapping tokens
            overlapping_tokens = set(reference_tokens) & set(candidate_tokens)

            # Compute contextual recall
            score_list.append(len(overlapping_tokens) / len(reference_tokens))

        metrics_df = pd.DataFrame(score_list, columns=["Contextual Recall"])
        figures = []
        # Visualization part
        fig = go.Figure()

        # Adding the line plots
        fig.add_trace(
            go.Scatter(
                x=metrics_df.index,
                y=metrics_df["Contextual Recall"],
                mode="lines+markers",
                name="Contextual Recall",
            )
        )
        fig.update_layout(
            title="Contextual Recall scores for each row",
            xaxis_title="Row Index",
            yaxis_title="Score",
        )
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )

        return self.cache_results(figures=figures)
