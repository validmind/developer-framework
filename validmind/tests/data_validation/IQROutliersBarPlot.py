# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class IQROutliersBarPlot(Metric):
    """
    Visualizes outlier distribution across percentiles in numerical data using the Interquartile Range (IQR) method.

    ### Purpose

    The InterQuartile Range Outliers Bar Plot (IQROutliersBarPlot) metric aims to visually analyze and evaluate the
    extent of outliers in numeric variables based on percentiles. Its primary purpose is to clarify the dataset's
    distribution, flag possible abnormalities in it, and gauge potential risks associated with processing potentially
    skewed data, which can affect the machine learning model's predictive prowess.

    ### Test Mechanism

    The examination invokes a series of steps:

    1. For every numeric feature in the dataset, the 25th percentile (Q1) and 75th percentile (Q3) are calculated
    before deriving the Interquartile Range (IQR), the difference between Q1 and Q3.
    2. Subsequently, the metric calculates the lower and upper thresholds by subtracting Q1 from the `threshold` times
    IQR and adding Q3 to `threshold` times IQR, respectively. The default `threshold` is set at 1.5.
    3. Any value in the feature that falls below the lower threshold or exceeds the upper threshold is labeled as an
    outlier.
    4. The number of outliers are tallied for different percentiles, such as [0-25], [25-50], [50-75], and [75-100].
    5. These counts are employed to construct a bar plot for the feature, showcasing the distribution of outliers
    across different percentiles.

    ### Signs of High Risk

    - A prevalence of outliers in the data, potentially skewing its distribution.
    - Outliers dominating higher percentiles (75-100) which implies the presence of extreme values, capable of severely
    influencing the model's performance.
    - Certain features harboring most of their values as outliers, which signifies that these features might not
    contribute positively to the model's forecasting ability.

    ### Strengths

    - Effectively identifies outliers in the data through visual means, facilitating easier comprehension and offering
    insights into the outliers' possible impact on the model.
    - Provides flexibility by accommodating all numeric features or a chosen subset.
    - Task-agnostic in nature; it is viable for both classification and regression tasks.
    - Can handle large datasets as its operation does not hinge on computationally heavy operations.

    ### Limitations

    - Its application is limited to numerical variables and does not extend to categorical ones.
    - Relies on a predefined threshold (default being 1.5) for outlier identification, which may not be suitable for
    all cases.
    - Only reveals the presence and distribution of outliers and does not provide insights into how these outliers
    might affect the model's predictive performance.
    - The assumption that data is unimodal and symmetric may not always hold true. In cases with non-normal
    distributions, the results can be misleading.
    """

    name = "iqr_outliers_bar_plot"
    required_inputs = ["dataset"]
    default_params = {"threshold": 1.5, "fig_width": 800}
    tasks = ["classification", "regression"]
    tags = ["tabular_data", "visualization", "numerical_data"]

    def run(self):
        df = self.inputs.dataset.df

        # Select numerical features
        features = self.inputs.dataset.feature_columns_numeric

        # Select non-binary features
        features = [
            feature
            for feature in features
            if len(self.inputs.dataset.df[feature].unique()) > 2
        ]

        threshold = self.params["threshold"]
        fig_width = self.params["fig_width"]

        df = df[features]

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

            if outliers.empty:
                continue  # Skip plotting if there are no outliers

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
