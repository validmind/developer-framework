# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class IQROutliersBarPlot(Metric):
    """
    **Purpose**: The InterQuartile Range Outliers Bar Plot (IQROutliersBarPlot) metric aims to visually analyse and
    evaluate the extent of outliers in numeric variables based on percentiles. This metric is vital for understanding
    data distribution, identifying abnormalities within a dataset and assessing the risk associated with processing
    potentially skewed data that might impact the predictive performance of the machine learning model.

    **Test Mechanism**: The test involves the following steps:

    1. For each numeric feature, or column, in the dataset, it computes Q1 (25th percentile) and Q3 (75th percentile),
    and then the Interquartile Range (IQR) which is the difference between Q3 and Q1.
    2. It then calculates the thresholds for lower and upper bounds as Q1 minus `threshold` times IQR and Q3 plus
    `threshold` times IQR, respectively. The default `threshold` is 1.5.
    3. Any value in the feature that is less than the lower bound and greater than the upper bound is considered an
    outlier.
    4. The number of outliers are then calculated for different percentile categories like [0-25], [25-50], [50-75],
    [75-100].
    5. These counts are then used to prepare a bar plot for the feature showing the distribution of outliers across
    different percentile ranges.

    **Signs of High Risk**: High risk or failure in the model's performance could be indicated by:

    1. Presence of large number of outliers in the data that will skew the distribution.
    2. When the outliers are in higher percentiles (75-100). This indicates extreme values, which can have a more
    prominent impact on the model's performance.
    3. Certain features having a majority of their values as outliers, meaning these features may not contribute
    positively to model's prediction power.

    **Strengths**:

    1. Identifies outliers in the data visually, which is easy to understand and can help in interpreting the potential
    impact on the model.
    2. Accommodates both total numeric features or a selected subset hence proving its flexibility.
    3. Agnostic to the task type: can be used for both classification and regression tasks.
    4. This metric can process large datasets as it does not rely on computationally expensive operations.

    **Limitations**:

    1. This metric only works with numerical variables and would not be applicable to categorical variables.
    2. It uses a pre-defined threshold (defaulting to 1.5) to determine what constitutes an outlier. This threshold
    might not be ideal for all cases.
    3. This metric does not provide insights about the consequence of these outliers on the predictive performance of
    the models, but only presents their presence and distribution.
    4. It assumes that the data is unimodal and symmetric, which may not be always the case. For non-normal
    distributions, the results might be misleading.
    """

    name = "iqr_outliers_bar_plot"
    required_context = ["dataset"]
    default_params = {"threshold": 1.5, "num_features": None, "fig_width": 800}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "visualization", "numerical_data"],
    }

    def run(self):
        df = self.dataset.df
        num_features = self.params["num_features"]
        threshold = self.params["threshold"]
        fig_width = self.params["fig_width"]

        # If num_features is None, use all numeric columns.
        # Otherwise, only use the columns provided in num_features.
        if num_features is None:
            df = df.select_dtypes(include=[np.number])
        else:
            df = df[num_features]

        return self.detect_and_visualize_outliers(df, threshold, fig_width)

    @staticmethod
    def compute_outliers(series, threshold=1.5):
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return series[(series < lower_bound) | (series > upper_bound)]

    def detect_and_visualize_outliers(self, df, threshold, fig_width):
        num_cols = df.columns.tolist()
        figures = []

        for col in num_cols:
            # Compute outliers
            outliers = self.compute_outliers(df[col], threshold)

            Q1_count = outliers[
                (outliers >= 0) & (outliers < outliers.quantile(0.25))
            ].count()
            Q2_count = outliers[
                (outliers >= outliers.quantile(0.25)) & (outliers < outliers.median())
            ].count()
            Q3_count = outliers[
                (outliers >= outliers.median()) & (outliers < outliers.quantile(0.75))
            ].count()
            Q4_count = outliers[
                (outliers >= outliers.quantile(0.75)) & (outliers <= outliers.max())
            ].count()

            # Prepare data for bar plot
            bar_data = [Q1_count, Q2_count, Q3_count, Q4_count]
            percentile_labels = [
                "0-25",
                "25-50",
                "50-75",
                "75-100",
            ]

            # Create a bar plot
            fig = go.Figure(
                data=[go.Bar(x=percentile_labels, y=bar_data, marker_color="skyblue")]
            )

            # Set layout properties
            fig.update_layout(
                title_text=col,
                width=fig_width,
                height=400,
                plot_bgcolor="white",
                xaxis_title="Percentile",
                yaxis_title="Outlier Count",
            )

            # Create a Figure object and append to figures list
            figure = Figure(for_object=self, key=f"{self.key}:{col}", figure=fig)
            figures.append(figure)

        return self.cache_results(figures=figures)
