# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import evaluate
import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class MeteorScore(Metric):
    """
    Computes and visualizes the METEOR score for each text generation instance, assessing translation quality.

    **Purpose**: METEOR (Metric for Evaluation of Translation with Explicit ORdering) is designed to evaluate the quality
    of machine translations by comparing them against reference translations. It emphasizes both the accuracy and fluency
    of translations, incorporating precision, recall, and word order into its assessment.

    **Test Mechanism**: The METEOR score is computed for each pair of machine-generated translation (prediction) and its
    corresponding human-produced reference. This is done by considering unigram matches between the translations, including
    matches based on surface forms, stemmed forms, and synonyms. The score is a combination of unigram precision and recall,
    adjusted for word order through a fragmentation penalty.

    **Signs of High Risk**:
    - Lower METEOR scores can indicate a lack of alignment between the machine-generated translations and their human-produced references, highlighting potential deficiencies in both the accuracy and fluency of translations.
    - Significant discrepancies in word order or an excessive fragmentation penalty could signal issues with how the translation model processes and reconstructs sentence structures, potentially compromising the natural flow of translated text.
    - Persistent underperformance across a variety of text types or linguistic contexts might suggest a broader inability of the model to adapt to the nuances of different languages or dialects, pointing towards gaps in its training or inherent limitations.

    **Strengths**:
    - Incorporates a balanced consideration of precision and recall, weighted towards recall to reflect the importance of
      content coverage in translations.
    - Directly accounts for word order, offering a nuanced evaluation of translation fluency beyond simple lexical matching.
    - Adapts to various forms of lexical similarity, including synonyms and stemmed forms, allowing for flexible matching.

    **Limitations**:
    - While comprehensive, the complexity of METEOR's calculation can make it computationally intensive, especially for
      large datasets.
    - The use of external resources for synonym and stemming matching may introduce variability based on the resources'
      quality and relevance to the specific translation task.
    """

    name = "meteor_score"
    required_inputs = ["model", "dataset"]

    def run(self):
        # Load the METEOR metric
        meteor = evaluate.load("meteor")

        # Initialize a list to hold METEOR scores
        meteor_scores = []

        for prediction, reference in zip(
            self.inputs.dataset.y_pred(self.inputs.model),
            self.inputs.dataset.y,
        ):
            # Compute the METEOR score for the current prediction-reference pair
            result = meteor.compute(predictions=[prediction], references=[reference])
            meteor_scores.append(result["meteor"])

        # Visualization of METEOR scores
        figures = self.visualize_scores(meteor_scores)

        return self.cache_results(figures=figures)

    def visualize_scores(self, scores):
        # Convert the scores list to a DataFrame for plotting
        scores_df = pd.DataFrame(scores, columns=["METEOR Score"])

        # Create a line plot of the METEOR scores
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=scores_df.index,
                y=scores_df["METEOR Score"],
                mode="lines+markers",
                name="METEOR Score",
            )
        )
        fig.update_layout(
            title="METEOR Scores Across Text Instances",
            xaxis_title="Text Instance Index",
            yaxis_title="METEOR Score",
        )

        # Wrap the Plotly figure for compatibility with your framework
        figures = [Figure(for_object=self, key=self.key, figure=fig)]

        return figures
