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
    **Purpose**: ROUGE, or Recall-Oriented Understudy for Gisting Evaluation, serves as a robust metric framework aimed
    at evaluating the caliber of machine-generated text. Especially pertinent in the arena of natural language
    generation tasks, such as text summarization, machine translation, and text generation, its overarching goal is to
    ascertain how effectively the machine-rendered text mirrors key information and concepts present in reference
    human-crafted text. Owing to its efficacy, the ROUGE metrics have become staples in the NLP community for the
    assessment of text generation systems.

    **Test Mechanism**:

    1. **Comparison Basis**: At its core, ROUGE operates by juxtaposing machine-generated content with a reference
    human-constructed text.

    2. **Incorporated Metrics**:
    - **ROUGE-N (N-gram Overlap)**: Focuses on the alignment of n-grams (sequential sets of n words) between the
    generated and reference texts. Typical n-values include 1 (unigrams), 2 (bigrams), and 3 (trigrams). Each metric
    calculates precision, recall, and F1-score components.

    - **ROUGE-L (Longest Common Subsequence)**: Pinpoints the most extended shared word sequence present in both the
    machine and reference texts, assessing the generated text's ability to encapsulate pivotal phrases.

    3. **Visual Representation**: The determined precision, recall, and F1-score for each metric are plotted visually,
    ensuring streamlined comprehension of the results.

    **Signs of High Risk**: Warning signs under this metric umbrella encompass low scores across the ROUGE suite. A
    diminished precision could insinuate the presence of redundant information in machine-produced text, while a low
    recall might denote the omission of salient data from the reference text. A decreased F1 score pinpoints a
    suboptimal harmony between precision and recall. Persistent low scores, especially across diverse test sets, may
    herald intrinsic flaws in the model's prowess.

    **Strengths**: ROUGE's primary asset is its multifaceted view on text quality, enabled by an array of evaluation
    metrics. It graciously accommodates synonyms and rephrasing due to its n-gram-based approach, and it champions the
    retention of salient word sequences via the longest common subsequence tactic. The visual representation of
    precision, recall, and F1-scores facilitates an intuitive grasp of model efficacy.

    **Limitations**: In spite of its advantages, certain constraints tether ROUGE. It might not adequately address the
    semantic coherence, fluency, or grammatical integrity of the generated narrative, leaning more towards evaluating
    isolated phrases or n-grams. The metric can be less discerning when critiquing elaborate sentences due to its
    fragmentary nature. Moreover, as it banks on comparisons with human-made references, procuring such benchmarks can
    be challenging or even impractical at times.
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
