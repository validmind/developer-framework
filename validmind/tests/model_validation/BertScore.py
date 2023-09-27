# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import evaluate
import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class BertScore(Metric):
    """
    Bert Score
    """

    name = "bert_score"
    required_inputs = ["model", "model.test_ds"]

    def description(self):
        return """BERTScore is a metric used to evaluate the quality of generated text or translations,
        focusing on the similarity between the reference text and the generated text. It uses contextual
        embeddings from BERT (Bidirectional Encoder Representations from Transformers) to compare the
        two texts.
        BERTScore is an automatic evaluation metric for text generation that computes a similarity score
        for each token in the candidate sentence with each token in the reference sentence. It leverages
        the pre-trained contextual embeddings from BERT models and matches words in candidate and reference
        sentences by cosine similarity.
        """

    def run(self):
        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict

        # Load the bert evaluation metric
        bert = evaluate.load("bertscore")

        # Compute the BLEU score
        bert_s = bert.compute(
            predictions=y_pred,
            references=y_true,
            lang="en",
        )

        metrics_df = pd.DataFrame(bert_s)
        figures = []

        # Visualization part
        fig = go.Figure()

        # Adding the line plots
        fig.add_trace(
            go.Scatter(
                x=metrics_df.index,
                y=metrics_df["precision"],
                mode="lines+markers",
                name="Precision",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=metrics_df.index,
                y=metrics_df["recall"],
                mode="lines+markers",
                name="Recall",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=metrics_df.index,
                y=metrics_df["f1"],
                mode="lines+markers",
                name="F1 Score",
            )
        )

        fig.update_layout(
            title="Bert Scores for Each Row",
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
