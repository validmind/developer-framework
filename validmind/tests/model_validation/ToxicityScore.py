# Copyright © 2023 ValidMind Inc. All rights reserved.
import itertools
from dataclasses import dataclass

import evaluate
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp

from validmind.vm_models import Figure, Metric


@dataclass
class ToxicityScore(Metric):
    """
    **Purpose:**
    The ToxicityScore metric is designed to present a sequential representation of toxicity scores for various texts.
    Leveraging line plots, it gives an overview of how toxicity scores evolve across the sequence of texts, highlighting
    trends and patterns.

    **Test Mechanism:**
    The mechanism involves fetching texts from specific columns, computing their toxicity scores using a preloaded
    `toxicity` evaluation tool, and then plotting these scores. A multi-panel visualization is created where each
    panel is dedicated to a specific text data column. Line plots serve as the primary visual tool, showing the progression of toxicity scores across text sequences. Each
    line plot corresponds to a specific text data column, illustrating the variation in toxicity scores as one moves
    from one text segment to the next.

    **Signs of High Risk:**
    Drastic spikes in the line plots, especially those that reach high toxicity values, indicate potentially toxic
    content within the associated text segment. If predicted summaries diverge significantly from input or target
    texts, it could be indicative of issues in the model's generated content.

    **Strengths:**
    The ToxicityScore offers a dynamic view of toxicity trends, enabling users to detect patterns or irregularities
    across the dataset. This is particularly valuable when comparing predicted content with actual data, helping
    highlight any inconsistencies or abnormalities in model output.

    **Limitations:**
    This metric’s accuracy is contingent upon the underlying `toxicity` tool. The line plots provide a broad overview
    of toxicity trends but do not specify which portions or tokens of the text are responsible for high toxicity scores.
    Consequently, for granular insights, supplementary, in-depth analysis might be needed.
    """

    name = "toxicity_line_plot"
    required_inputs = ["model"]
    metadata = {
        "task_types": [
            "text_classification",
            "text_summarization",
        ],
        "tags": ["toxicity_line_plot"],
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

    def toxicity_line_plots(self, df):
        """
        Compute toxicity scores for texts and then plot line plots for all columns of df.

        Parameters:
        - df (pd.DataFrame): The dataframe containing texts.
        """

        # Extract necessary parameters
        toxicity = evaluate.load("toxicity")

        # Get all columns of df
        text_columns = df.columns.tolist()

        # Determine the number of rows required based on the number of text columns
        num_rows = (len(text_columns) + 1) // 2

        # Create a subplot layout
        fig = sp.make_subplots(rows=num_rows, cols=2, subplot_titles=text_columns)

        subplot_height = 350
        total_height = num_rows * subplot_height + 200

        for idx, col in enumerate(text_columns, start=1):
            row = (idx - 1) // 2 + 1
            col_idx = (idx - 1) % 2 + 1

            # Get list of texts from dataframe
            texts = df[col].tolist()

            # Compute toxicity for texts
            toxicity_scores = toxicity.compute(predictions=texts)["toxicity"]

            # Add traces to the corresponding subplot
            fig.add_trace(
                go.Scatter(
                    y=toxicity_scores,
                    mode="lines+markers",
                    marker=dict(size=5),
                    line=dict(width=1.5),
                    showlegend=False,
                ),
                row=row,
                col=col_idx,
            )

            # Update xaxes and yaxes titles only for the first subplot
            if idx == 1:
                fig.update_xaxes(title_text="Text Index", row=row, col=col_idx)
                fig.update_yaxes(title_text="Toxicity Score", row=row, col=col_idx)

        # Update layout
        fig.update_layout(
            title_text="Line Plots of Toxicity Scores", height=total_height
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

        fig = self.toxicity_line_plots(df)

        return self.cache_results(
            figures=[Figure(for_object=self, key=self.key, figure=fig)]
        )
