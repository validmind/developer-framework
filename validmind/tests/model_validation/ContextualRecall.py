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
    **Purpose**: The Contextual Recall metric is used to evaluate the proficiency of a natural language generation
    (NLG) model in generating textual content that is coherent and consistent with the provided context or prompt. It
    quantifies the model's ability to recollect and reflect the foundational context in its generated output. This is
    crucial in NLP tasks, where models should generate text that is contextually relevant.

    **Test Mechanism**: The contextual recall is computed using a series of steps. First, we collect a series of
    reference texts representative of desired outputs for a certain context. Using the same context, candidate texts
    are generated from the NLG model. Both reference and candidate texts are tokenized using NLTK into words/tokens.
    The overlap of tokens between the reference and candidate texts is computed. The Contextual Recall score is then
    achieved by dividing the number of overlapping tokens by the total number of tokens in the reference text. The
    score is calculated for each row of the model's test dataset, leading to a list of scores. This set of scores is
    subsequently visualized by a line plot that displays the variation in the scores for each row.

    **Signs of High Risk**: A low contextual recall score points towards a high risk. It indicates that the model is
    not adequately recalling and resonating the original context through its generated text, leading to incoherent and
    contextually disparate text generation. If the model consistently gives low recall scores, there is a high
    possibility of model underperformance.

    **Strengths**: The strength of the contextual recall metric is that it allows a quantifiable measurement of a
    model's ability to adhere to and recall both the context and facts in the generated text. This is especially useful
    in tasks requiring a deep understanding and reproduction of the context, such as continuing a text or generating
    responses in a dialogue system. The line plot visualization also provides an aesthetically pleasing and intuitive
    view of the variation in scores.

    **Limitations**: Though helpful, the Contextual Recall metric might not fully encapsulate all facets of NLG model
    performance. It focuses primarily on word overlap, which can result in high scores for generated texts that use
    many common words, even if they do not form coherent or meaningful sentences. Furthermore, it doesn't take into
    consideration the order of words, which might lead to high scores for jumbled text. Finally, rare words may be less
    likely to match, which could undermine models capable of using them appropriately.
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
