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
    **Purpose**: The Contextual Recall metric is utilized to gauge the proficiency of a natural language generation
    (NLG) model in crafting textual content that remains coherent and consistent with the presented context or prompt.
    It quantifies the model's aptitude to recollect and mirror the foundational context in its resultant output. In the
    realm of NLP tasks, it's paramount that models generate text reflecting contextual relevance.

    **Test Mechanism**:

    1. **Prepare Reference and Candidate Texts**:
    - **Reference Texts**: Gather your reference text(s) which epitomize the expected or ideal output for a designated
    context or prompt.
    - **Candidate Texts**: Using the same context, generate candidate text(s) from the NLG model under evaluation.

    2. **Tokenization and Preprocessing**:
    - Tokenize both the reference and candidate texts into discernible words or tokens, using established libraries
    like NLTK.

    3. **Compute Contextual Recall**:
    - Ascertain the overlap of tokens between the reference and candidate texts.
    - The Contextual Recall score is deduced by dividing the number of overlapping tokens by the total token count of
    the reference text. The assessment is made for each test dataset instance, resulting in an array of scores. This
    series of scores is then illustrated via a line plot, showing score variations across rows.

    **Signs of High Risk**: Low contextual recall scores are red flags. They imply that the model isn't efficiently
    echoing the original context in its generated content, culminating in outputs that are incoherent or contextually
    off-track. A persistent trend of low recall scores could presage model underperformance.

    **Strengths**: The standout attribute of the contextual recall metric is its ability to quantifiably gauge a
    model's adherence to, and recollection of, both the context and factual elements in the generated narrative. This
    proves invaluable in applications demanding profound context comprehension, such as text continuation or
    interactive dialogue systems. The accompanying line plot visualization offers a lucid and intuitive representation
    of score variations.

    **Limitations**: Although potent, the Contextual Recall metric might not holistically represent all dimensions of
    NLG model performance. Its predominant focus on word overlap might award high scores to texts that employ numerous
    common words, even if they lack coherence or meaningful context. It also bypasses the significance of word order,
    which might lead to inflated scores for scrambled outputs. Lastly, infrequent words, despite being used aptly,
    might not match as often, potentially undervaluing models proficient in their application.
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
