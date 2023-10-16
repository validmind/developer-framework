# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from rouge import Rouge

from validmind.vm_models import Figure, Metric


@dataclass
class RougeMetrics(Metric):
    """
    Evaluates the quality of machine-generated text using various ROUGE metrics, and visualizes the results.

    **Purpose**: The ROUGE, or Recall-Oriented Understudy for Gisting Evaluation, is a metric employed to assess the
    quality of machine-generated text. This evaluation technique is mainly used in natural language processing tasks,
    such as text summarization, machine translation, and text generation. Its goal is to measure how well the
    machine-generated text reflects the key information and concepts in the human-crafted reference text.

    **Test Mechanism**:

    1. **Comparison Procedure**: The testing mechanism involves comparing machine-generated content with a reference
    human-constructed text.

    2. **Integral Metrics**:
       - **ROUGE-N (N-gram Overlap)**: This evaluates the overlap of n-grams (sequences of n words) between the
    generated and reference texts. The common n-values are 1 (unigrams), 2 (bigrams), and 3 (trigrams). Each metric
    calculates precision, recall, and F1-score.

       - **ROUGE-L (Longest Common Subsequence)**: This identifies the longest shared word sequence in both the machine
    and reference texts, thus evaluating the capability of the generated text to mirror key phrases.

       - **ROUGE-S (Skip-bigram)**: This measures the concurrence of skip-bigrams — word pairings that appear within a
    predefined word window in the text. This metric maintains sensitivity to word order while allowing for sporadic
    word omissions.

    3. **Visual Representation**: Precision, recall, and F1-score for all the metrics are visually charted, which makes
    the results easier to comprehend.

    **Signs of High Risk**:

    - Low scores across the suite of ROUGE metrics
    - Low precision might indicate redundant information in machine-produced text
    - Low recall may suggest the omission of important information from the reference text
    - Low F1 score could indicate an imbalanced performance between precision and recall
    - Persistent low scores could signal inherent flaws in the model

    **Strengths**:

    - Offers a multifaceted perspective on text quality using various evaluation metrics
    - Adapts to synonyms and rewording, thanks to n-gram-based evaluation
    - Encourages the retention of key word sequences using the longest common subsequence method
    - Visual representation of precision, recall, and F1-scores enhances understandability of model performance

    **Limitations**:

    - May fail to fully address the semantic coherence, fluency, or grammatical quality of the generated text
    - Tends to evaluate isolated phrases or n-grams rather than comprehensive sentences
    - May prove challenging when reference texts are difficult or impractical to obtain due to its reliance on
    comparisons with human-made references.
    """

    name = "rouge_metric"
    required_inputs = ["model", "model.test_ds"]
    default_params = {
        "rouge_metrics": ["rouge-1", "rouge-2", "rouge-l"],
    }

    def run(self):
        r_metrics = self.params["rouge_metrics"]
        if r_metrics is None:
            raise ValueError("rouge_metrics must be provided in params")

        # With all
        if not (
            set(self.default_params.get("rouge_metrics")).intersection(r_metrics)
            == set(r_metrics)
        ):
            raise ValueError(
                f"Invalid metrics from {self.default_params.get('rouge_metrics')}"
            )

        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict

        rouge = Rouge(metrics=r_metrics)

        score_list = []
        for y_t, y_p in zip(y_true, y_pred):
            scores = rouge.get_scores(y_p, y_t, avg=True)
            score_list.append(scores)

        metrics_df = pd.DataFrame(score_list)
        figures = []
        for m in metrics_df.columns:
            df_scores = pd.DataFrame(metrics_df[m].tolist())
            # Visualization part
            fig = go.Figure()

            # Adding the line plots
            fig.add_trace(
                go.Scatter(
                    x=df_scores.index,
                    y=df_scores["p"],
                    mode="lines+markers",
                    name="Precision",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df_scores.index,
                    y=df_scores["r"],
                    mode="lines+markers",
                    name="Recall",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df_scores.index,
                    y=df_scores["f"],
                    mode="lines+markers",
                    name="F1 Score",
                )
            )

            fig.update_layout(
                title="ROUGE Scores for Each Row",
                xaxis_title="Row Index",
                yaxis_title="Score",
            )
            k = m.replace("-", "")
            figures.append(
                Figure(
                    for_object=self,
                    key=k,
                    figure=fig,
                )
            )

        return self.cache_results(figures=figures)
