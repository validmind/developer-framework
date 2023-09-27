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
    rouge Metric
    """

    name = "rouge_metric"
    required_inputs = ["model", "model.test_ds"]
    default_params = {
        "rouge_metrics": ["rouge-1", "rouge-2", "rouge-l", "rouge-s"],
    }

    def description(self):
        return """
        ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics used for the automatic
        evaluation of machine-generated text, particularly in the context of natural language generation tasks
        such as text summarization, machine translation, and text generation. ROUGE measures the quality of
        generated text by comparing it to reference (human-generated) text. The primary goal of ROUGE is to
        assess the effectiveness of machine-generated text in capturing key information and concepts from the
        reference text.

        Here are the key components and metrics within the ROUGE family:

        ROUGE-N (N-gram Overlap): ROUGE-N measures the overlap of n-grams (contiguous sequences of n words)
        between the generated text and reference text. Common values for N are 1 (unigrams), 2 (bigrams), and
        3 (trigrams). ROUGE-N typically includes precision, recall, and F1-score components.

        ROUGE-L (Longest Common Subsequence): ROUGE-L measures the longest common subsequence between the generated
        text and reference text. It considers the longest sequence of words that appears in both texts and evaluates
        how well the generated text captures important phrases.

        ROUGE-S (Skip-bigram): ROUGE-S focuses on measuring the overlap of skip-bigrams, which are pairs of words
        that appear within a certain window of words in the text. It accounts for the order of words while allowing
        for some word skipping.

        ROUGE metrics are widely used in the evaluation of text generation systems, especially in research and
        development of natural language processing models. They provide a quantitative way to assess the quality
        of generated text by comparing it to human-authored references. Researchers and practitioners often report
        multiple ROUGE scores (e.g., ROUGE-1, ROUGE-2, ROUGE-L) to provide a comprehensive evaluation of their models'
        performance.
        """

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
