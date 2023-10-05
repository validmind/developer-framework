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
    Evaluates text generation models' performance by calculating precision, recall, and F1 score based on BERT
    contextual embeddings.

    **Purpose**: The BERTScore metric is deployed to evaluate the competence of text generation models by focusing on
    the similarity between the reference and the generated text. It employs the contextual embeddings from BERT models
    to assess the similarity of the contents. This measures the extent to which a model has learned and can generate
    contextually relevant results.

    **Test Mechanism**: The true values derived from the model's test dataset and the model's predictions are employed
    in this metric. BERTScore calculates the precision, recall, and F1 score of the model considering the contextual
    similarity between the reference and the produced text. These scores are computed for each token in the predicted
    sentences as compared to the reference sentences, while considering the cosine similarity with BERT embeddings. A
    line plot depicting the score changes across row indexes is generated for each metric i.e., Precision, Recall, and
    F1 Score.

    **Signs of High Risk**:
    - Observable downward trend in Precision, Recall, or F1 Score.
    - Noticeable instability or fluctuation in these metrics. Lower Precision implies that predictions often
    incorporate irrelevant contexts.
    - Declining Recall suggests that the model frequently omits relevant contexts during predictions.
    - Lower F1 score signals poor overall performance in both precision and recall.

    **Strengths**:
    - BERTScore efficiently detects the quality of text that requires to comprehend the context, a common requirement
    in natural language processing tasks.
    - This metric advances beyond the simple n-gram matching and considers the semantic similarity in the context,
    thereby providing more meaningful evaluation results.
    - The integrated visualization function allows tracking of the performance trends across different prediction sets.

    **Limitations**:
    - Dependence on BERT model embeddings for BERTScore implies that if the base BERT model is not suitable for a
    specific task, it might impair the accuracy of BERTScore.
    - Despite being good at understanding semantics, it might be incapable of capturing certain nuances in text
    similarity that other metrics like BLEU or ROUGE could detect.
    - Can be computationally expensive due to the utilization of BERT embeddings.
    """

    name = "bert_score"
    required_inputs = ["model", "model.test_ds"]

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
