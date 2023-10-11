# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import evaluate
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp

from validmind.vm_models import Figure, Metric


@dataclass
class ToxicityHistogram(Metric):
    """
    **Purpose:**
    The ToxicityHistogram metric visualizes and analyzes the toxicity scores of various texts. Through histograms, it
    provides insights into the distribution and nature of toxicity present in the evaluated text segments.

    **Test Mechanism:**
    Texts are fetched from specified columns and their toxicity scores are computed using a preloaded `toxicity`
    evaluation tool. Each text data column is visualized with its own histogram, culminating in a multi-panel
    visualization.

    **Signs of High Risk:**
    High toxicity concentrations in the histogram, especially on the upper scale, signify a higher presence of toxic
    content in the respective text segment. If predicted summaries show significantly differing patterns from input or
    target texts, it could indicate issues with the model's output.

    **Strengths:**
    The metric offers a lucid representation of toxicity distributions, facilitating the swift identification of
    concerning patterns. It's instrumental for gauging potential pitfalls of generated content, particularly in the
    realm of predicted summaries.

    **Limitations:**
    The ToxicityHistogram's efficacy hinges on the accuracy of the `toxicity` tool it employs. While histograms depict
    distribution patterns, they omit details about which specific text portions or tokens result in high toxicity
    scores. Therefore, for a comprehensive understanding, more in-depth analysis might be requisite.
    """

    name = "toxicity_histogram"
    required_inputs = ["model"]
    metadata = {
        "task_types": [
            "text_classification",
            "text_summarization",
        ],
        "tags": ["toxicity_histogram"],
    }

    def _get_datasets(self):
        # Check model attributes
        if not hasattr(self, "model"):
            raise AttributeError("The 'model' attribute is missing.")

        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict
        input_text = self.model.test_ds.df[self.model.test_ds.text_column]

        # Ensure consistency in lengths
        if not len(y_true) == len(y_pred) == len(input_text):
            raise ValueError(
                "Inconsistent lengths among input text, true summaries, and predicted summaries."
            )

        return input_text, y_true, y_pred

    def toxicity_histograms(self, df):
        """
        Compute toxicity scores for texts and then plot histograms for all columns of df.

        Parameters:
        - df (pd.DataFrame): The dataframe containing texts.
        """

        # Extract necessary parameters
        toxicity = evaluate.load("toxicity")

        # Get all columns of df
        text_columns = df.columns.tolist()

        # Determine the number of rows required based on the number of text columns
        num_rows = (len(text_columns) + 1) // 2  # +1 to handle odd number of columns

        # Create a subplot layout
        fig = sp.make_subplots(rows=num_rows, cols=2, subplot_titles=text_columns)

        subplot_height = 350  # Height of each subplot
        total_height = num_rows * subplot_height + 200  # 200 for padding, titles, etc.

        for idx, col in enumerate(text_columns, start=1):
            row = (idx - 1) // 2 + 1
            col_idx = (idx - 1) % 2 + 1  # to place subplots in two columns

            # Get list of texts from dataframe
            texts = df[col].tolist()

            # Compute toxicity for texts
            toxicity_scores = toxicity.compute(predictions=texts)["toxicity"]

            # Add traces to the corresponding subplot without legend
            fig.add_trace(
                go.Histogram(x=toxicity_scores, showlegend=False), row=row, col=col_idx
            )

            # Update xaxes and yaxes titles only for the first subplot
            if idx == 1:
                fig.update_xaxes(title_text="Toxicity Score", row=row, col=col_idx)
                fig.update_yaxes(title_text="Frequency", row=row, col=col_idx)

        # Update layout
        fig.update_layout(
            title_text="Histograms of Toxicity Scores", height=total_height
        )

        return fig

    def run(self):
        input_text, y_true, y_pred = self._get_datasets()

        df = pd.DataFrame(
            {
                "Input Text": input_text,
                "Target Text": y_true,
                "Predicted Summaries": y_pred,
            }
        )

        fig = self.toxicity_histograms(df)

        return self.cache_results(
            figures=[Figure(for_object=self, key=self.key, figure=fig)]
        )
