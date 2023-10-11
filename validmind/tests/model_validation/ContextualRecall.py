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
    Evaluates a Natural Language Generation model's ability to generate contextually relevant and factually correct
    text.

    **Purpose**:
    The Contextual Recall metric is used to evaluate the ability of a natural language generation (NLG) model to
    generate text that appropriately reflects the given context or prompt. It measures the model's capability to
    remember and reproduce the main context in its resulting output. This metric is critical in natural language
    processing tasks, as the coherency and contextuality of the generated text are essential.

    **Test Mechanism**:

    1. **Preparation of Reference and Candidate Texts**:
        - **Reference Texts**: Gather the reference text(s) which exemplify the expected or ideal output for a specific
    context or prompt.
        - **Candidate Texts**: Generate candidate text(s) from the NLG model under evaluation using the same context.
    2. **Tokenization and Preprocessing**:
        - Tokenize the reference and candidate texts into discernible words or tokens using libraries such as NLTK.
    3. **Computation of Contextual Recall**:
        - Identify the token overlap between the reference and candidate texts.
        - The Contextual Recall score is computed by dividing the number of overlapping tokens by the total number of
    tokens in the reference text. Scores are calculated for each test dataset instance, resulting in an array of
    scores. These scores are then visualized using a line plot to show score variations across different rows.

    **Signs of High Risk**:

    - Low contextual recall scores could indicate that the model is not effectively reflecting the original context in
    its output, leading to incoherent or contextually misaligned text.
    - A consistent trend of low recall scores could suggest underperformance of the model.

    **Strengths**:

    - The Contextual Recall metric provides a quantifiable measure of a model's adherence to the context and factual
    elements of the generated narrative.
    - This metric finds particular value in applications requiring deep comprehension of context, such as text
    continuation or interactive dialogue systems.
    - The line plot visualization provides a clear and intuitive representation of score fluctuations.

    **Limitations**:

    - Despite its effectiveness, the Contextual Recall could fail to comprehensively assess the performance of NLG
    models. Its focus on word overlap could result in high scores for texts that use many common words, even when these
    texts lack coherence or meaningful context.
    - This metric does not consider the order of words, which could lead to overestimated scores for scrambled outputs.
    - Models that effectively use infrequent words might be undervalued, as these words might not overlap as often.
    """

    name = "contextual_recall"
    required_inputs = ["model", "model.test_ds"]

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
