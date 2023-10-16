# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
from rouge import Rouge

from validmind.vm_models import Figure, Metric


@dataclass
class RougeMetricsAggregate(Metric):
    """
    Evaluates the average quality of machine-generated text using various ROUGE metrics and visualizes the aggregated results.

    **Purpose**: The ROUGE, or Recall-Oriented Understudy for Gisting Evaluation, remains a cornerstone for assessing
    machine-generated text quality. Predominantly used in tasks such as text summarization, machine translation,
    and text generation, the emphasis of ROUGE is to gauge the reflection of pivotal information and core concepts
    from human references in machine-produced content.

    **Test Mechanism**:

    1. **Comparison Procedure**: The evaluation requires contrasting machine-rendered text against a human-made reference.

    2. **Integral Metrics**:
       - **ROUGE-N (N-gram Overlap)**: Assesses the commonality of n-grams between both sets of texts. Regularly,
       metrics consider 1 (unigrams), 2 (bigrams), and 3 (trigrams), rendering precision, recall, and F1-score.

       - **ROUGE-L (Longest Common Subsequence)**: Discerns the lengthiest mutually inclusive word chain in both
       texts, ascertaining the machine text's efficacy in capturing essential phrases.

       - **ROUGE-S (Skip-bigram)**: Quantifies the concurrence of skip-bigrams. This metric cherishes word order
       but tolerates occasional omissions.

    3. **Visual Representation**: The aggregate approach underscores the visualization of average scores across
    precision, recall, and F1-score, enhancing result interpretation.

    **Signs of High Risk**:

    - Diminished average scores across ROUGE metrics
    - Depressed precision may highlight verbosity in machine text
    - Lacking recall might hint at missed critical details from the reference
    - A dwindling F1 score might spotlight a disjointed precision-recall performance
    - Consistently low averages could reveal deep-rooted model inadequacies

    **Strengths**:

    - Provides a holistic view of text quality via diverse metrics
    - Gracefully handles paraphrasing owing to n-gram evaluations
    - Promotes the capture of crucial word chains through the longest common subsequence
    - Aggregate visual insights bolster comprehension of overall model behavior

    **Limitations**:

    - Might overlook nuances like semantic integrity, fluency, or syntactic correctness
    - Focuses more on discrete phrases or n-grams over holistic sentences
    - Reliance on human references can be limiting when they're hard to source or infeasible.
    """

    name = "rouge_metrics_aggregate"
    required_inputs = ["model", "model.test_ds"]
    default_params = {
        "rouge_metrics": ["rouge-1", "rouge-2", "rouge-l"],
    }

    def run(self):
        r_metrics = self.params["rouge_metrics"]
        if r_metrics is None:
            raise ValueError("rouge_metrics must be provided in params")

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

        colors = {"Precision": "blue", "Recall": "green", "F1 Score": "red"}
        mapping = {"p": "Precision", "r": "Recall", "f": "F1 Score"}

        for m in metrics_df.columns:
            df_scores = pd.DataFrame(metrics_df[m].tolist())
            avg_scores = df_scores.mean()

            # Visualization part
            fig = go.Figure()

            # Adding the bar plots for average scores with specified colors
            for metric_short, metric_full in mapping.items():
                fig.add_trace(
                    go.Bar(
                        x=[metric_full],
                        y=[avg_scores[metric_short]],
                        name=metric_full,
                        marker_color=colors[metric_full],
                        showlegend=False,
                    )
                )

            fig.update_layout(
                title=f"Average ROUGE Scores for {m}",
                xaxis_title="Metric",
                yaxis_title="Average Score",
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
