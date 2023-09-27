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
    **Purpose**: BERTScore is a metric used to evaluate the quality of text generation models, focusing on the
    similarity between the reference text and the generated text. It leverages the contextual embeddings from BERT
    models to evaluate the similarity of the contents. Therefore, it distinctively measures how well a model has
    learned and can generate context-relevant results.

    **Test Mechanism**: This metric derives the true values from the model's testing set and the model's predictions.
    BERTScore evaluates the precision, recall, and F1 score of the model according to the contextual similarity between
    the reference and the generated text. These scores are calculated for each token in the candidate sentences as
    compared to the reference sentences, taking into account cosine similarity with BERT embeddings. A line plot is
    generated for each metric (Precision, Recall and F1 Score), which visualizes the score changes across row indexes.

    **Signs of High Risk**: If there's a general downward trend in Precision, Recall, or F1 Score or any noticeable
    instability/fluctuation in these metrics, it indicates high risk. A low Precision implies that predictions often
    include irrelevant contexts. A low Recall implies the models miss relevant contexts in predictions. A low F1 score
    indicates poor overall performance in both precision and recall.

    **Strengths**: BERTScore is potent in detecting the quality of text that requires understanding the context, which
    is a typical demand in natural language processing tasks. This metric goes beyond simple n-gram matching and
    considers the semantic similarity in the context, which provides more meaningful evaluation results. The
    visualization allows observing the performance trends across different sets of predictions.

    **Limitations**: BERTScore is dependent on BERT model embeddings; therefore, if the base BERT model is not
    well-suited for a specific task, it may impact the accuracy of BERTScore. In addition, although good at semantic
    understanding, it might not capture some nuances in text similarity that other metrics like BLEU or ROUGE can
    detect. Finally, it can be computationally expensive due to the use of BERT embeddings.
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
