# Copyright © 2023 ValidMind Inc. All rights reserved.

import itertools
from dataclasses import dataclass

import evaluate
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class RegardScore(Metric):
    """
    **Purpose:**
    The `RegardScore` metric assesses the degree of regard—positive, negative, neutral, or other—present in the given text,
    whether it's a classification or summarization result. Especially crucial for applications like sentiment analysis,
    product reviews, or opinion mining, it provides a granular understanding of how the model perceives or generates content
    in terms of favorability or sentiment.

    **Test Mechanism:**
    The metric ingests data primarily from the model's test dataset, extracting the input text, target text (true regard),
    and the model's predicted regard. These elements undergo a series of consistency checks before being processed. Using
    the `evaluate.load("regard")` tool, regard scores are computed for each segment of text. The results are then visualized
    in a multi-subplot line graph, where each subplot corresponds to a particular category of regard (e.g., positive, negative,
    neutral, other) against the input, target, and predicted texts.

    **Signs of High Risk:**
    Disparities between the target regard scores and the predicted regard scores may signify potential flaws or biases in
    the model. For instance, if neutral inputs are consistently perceived as strongly positive or negative, this could
    indicate the model's inability to correctly identify or generate balanced sentiments.

    **Strengths:**
    The metric's visual presentation, using line plots, provides an intuitive way to comprehend the model's regard assessment
    across different text samples and regard categories. The color-coded lines associated with each regard category further
    enhance the clarity of the comparison, making it simpler for stakeholders or researchers to infer the model's performance.

    **Limitations:**
    The `RegardScoreHistogram` metric emphasizes regard scores but may not always grasp intricate nuances or the true context
    of texts. Its reliance on underlying tools, which might be trained on potentially biased datasets, can result in skewed
    interpretations. Additionally, while the metric segments regard into discrete categories such as "positive" and "negative,"
    real-world sentiments often exist on a more complex spectrum. The metric's efficacy is intertwined with the accuracy of
    the model's predictions; any inherent model inaccuracies can impact the metric's reflection of true sentiments.
    """

    name = "regard_score"
    required_inputs = ["model"]
    metadata = {
        "task_types": ["text_classification", "text_summarization"],
        "tags": ["regard_score"],
    }

    def _get_datasets(self):
        if not hasattr(self, "model"):
            raise AttributeError("The 'model' attribute is missing.")

        y_true = list(itertools.chain.from_iterable(self.model.y_test_true))
        y_pred = self.model.y_test_predict
        input_text = self.model.test_ds.df[self.model.test_ds.text_column]

        if not len(y_true) == len(y_pred) == len(input_text):
            raise ValueError(
                "Inconsistent lengths among input text, true summaries, and predicted summaries."
            )

        return input_text, y_true, y_pred

    def regard_line_plot(self):
        regard_tool = evaluate.load("regard")
        input_text, y_true, y_pred = self._get_datasets()

        dataframes = {
            "Input Text": input_text,
            "Target Text": y_true,
            "Predicted Summaries": y_pred,
        }

        total_text_columns = len(dataframes)
        total_rows = total_text_columns * 2

        categories_order = ["positive", "negative", "neutral", "other"]
        category_colors = {
            "negative": "#d9534f",
            "neutral": "#5bc0de",
            "other": "#f0ad4e",
            "positive": "#5cb85c",
        }

        fig = make_subplots(
            rows=total_rows,
            cols=2,
            subplot_titles=[
                f"{col_name} {cat}"
                for col_name in dataframes
                for cat in categories_order
            ],
            shared_yaxes=True,
            vertical_spacing=0.1,
        )

        row_offset = 0
        for column_name, column_data in dataframes.items():
            results = regard_tool.compute(data=column_data)["regard"]
            regard_dicts = [
                dict((x["label"], x["score"]) for x in sublist) for sublist in results
            ]

            for idx, category in enumerate(categories_order, start=1):
                row, col = ((idx - 1) // 2 + 1 + row_offset, (idx - 1) % 2 + 1)
                scores = [res_dict[category] for res_dict in regard_dicts]
                fig.add_trace(
                    go.Scatter(
                        name=f"{category} ({column_name})",
                        x=list(range(len(column_data))),
                        y=scores,
                        mode="lines+markers",
                        marker=dict(size=5),
                        hoverinfo="y+name",
                        line=dict(color=category_colors[category], width=1.5),
                        showlegend=False,
                    ),
                    row=row,
                    col=col,
                )
            row_offset += 2

        subplot_height = 350
        total_height = total_rows * subplot_height + 200

        fig.update_layout(title_text="Regard Scores", height=total_height)
        fig.update_yaxes(range=[0, 1])
        fig.update_xaxes(showticklabels=False, row=1, col=1)
        fig.update_xaxes(title_text="Index", showticklabels=True, row=1, col=1)
        fig.update_yaxes(title_text="Score", showticklabels=True, row=1, col=1)

        return fig

    def run(self):
        fig = self.regard_line_plot()
        return self.cache_results(
            figures=[Figure(for_object=self, key=self.key, figure=fig)]
        )
