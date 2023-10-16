# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import evaluate
import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class BertScoreAggregate(Metric):
    """
    Evaluates the aggregate performance of text generation models by computing the average precision, recall,
    and F1 score based on BERT contextual embeddings.

    **Purpose**: The BERTScore Aggregate metric provides an overall assessment of text generation models by
    averaging the similarity scores between the reference and the generated text over the entire dataset.
    Using contextual embeddings from BERT models, it gives a high-level view of the contextual relevance
    of the model's outputs.

    **Test Mechanism**: This metric takes the true values from the model's test dataset and the model's
    predictions to compute the average BERTScore. It showcases the aggregate precision, recall, and F1 score
    for the entire test set, providing an overview of the model's overall contextual accuracy.

    **Signs of High Risk**:
    - Average Precision, Recall, or F1 Score that is significantly low.
    - A low Precision average suggests the model's tendency to include irrelevant contexts.
    - A low Recall average indicates the model's propensity to miss relevant contexts.
    - A low F1 score average denotes a general deficiency in both precision and recall.

    **Strengths**:
    - Provides a holistic view of the model's performance in terms of contextual similarity.
    - Factors in the semantic similarity in context, advancing beyond basic n-gram matching.
    - The single aggregate score for each metric simplifies the evaluation process and aids in quick insights.

    **Limitations**:
    - As an average, it might obscure individual instances where the model performed exceptionally well or poorly.
    - Relies on BERT model embeddings, so the quality of the base BERT model can affect results.
    - May miss nuances in text similarity that detailed metrics or other evaluations like BLEU or ROUGE might catch.
    - Computationally demanding due to the use of BERT embeddings.
    """

    name = "bert_score_aggregate"
    required_inputs = ["model", "model.test_ds"]

    def run(self):
        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict

        bert = evaluate.load("bertscore")
        bert_s = bert.compute(predictions=y_pred, references=y_true, lang="en")
        metrics_df = pd.DataFrame(bert_s)

        mean_precision = metrics_df["precision"].mean()
        mean_recall = metrics_df["recall"].mean()
        mean_f1 = metrics_df["f1"].mean()

        fig = go.Figure(
            data=[
                go.Bar(
                    name="Precision",
                    x=["Precision"],
                    y=[mean_precision],
                    marker_color="blue",
                ),
                go.Bar(
                    name="Recall", x=["Recall"], y=[mean_recall], marker_color="green"
                ),
                go.Bar(
                    name="F1 Score", x=["F1 Score"], y=[mean_f1], marker_color="red"
                ),
            ]
        )

        fig.update_layout(
            title="Aggregated Bert Scores",
            xaxis_title="Metric",
            yaxis_title="Score",
            showlegend=False,
            width=600,
            height=600,
        )

        figures = [Figure(for_object=self, key=self.key, figure=fig)]
        return self.cache_results(figures=figures)
