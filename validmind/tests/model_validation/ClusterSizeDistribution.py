# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class ClusterSizeDistribution(Metric):
    """
    Assesses the performance of clustering models by comparing the distribution of cluster sizes in model predictions
    with the actual data.

    ### Purpose

    The Cluster Size Distribution test aims to assess the performance of clustering models by comparing the
    distribution of cluster sizes in the model's predictions with the actual data. This comparison helps determine if
    the clustering model's output aligns well with the true cluster distribution, providing insights into the model's
    accuracy and performance.

    ### Test Mechanism

    The test mechanism involves the following steps:
    - Run the clustering model on the provided dataset to obtain predictions.
    - Convert both the actual and predicted outputs into pandas dataframes.
    - Use pandas built-in functions to derive the cluster size distributions from these dataframes.
    - Construct two histograms: one for the actual cluster size distribution and one for the predicted distribution.
    - Plot the histograms side-by-side for visual comparison.

    ### Signs of High Risk

    - Discrepancies between the actual cluster size distribution and the predicted cluster size distribution.
    - Irregular distribution of data across clusters in the predicted outcomes.
    - High number of outlier clusters suggesting the model struggles to correctly group data.

    ### Strengths

    - Provides a visual and intuitive way to compare the clustering model's performance against actual data.
    - Effectively reveals where the model may be over- or underestimating cluster sizes.
    - Versatile as it works well with any clustering model.

    ### Limitations

    - Assumes that the actual cluster distribution is optimal, which may not always be the case.
    - Relies heavily on visual comparison, which could be subjective and may not offer a precise numerical measure of
    performance.
    - May not fully capture other important aspects of clustering, such as cluster density, distances between clusters,
    and the shape of clusters.
    """

    name = "cluster_size_distribution"
    required_inputs = ["model", "dataset"]
    tasks = ["clustering"]
    tags = [
        "sklearn",
        "model_performance",
    ]

    def run(self):
        y_true_train = self.inputs.dataset.y
        y_pred_train = self.inputs.dataset.y_pred(self.inputs.model)
        y_true_train = y_true_train.astype(y_pred_train.dtype)
        df = pd.DataFrame(
            {"Actual": y_true_train.ravel(), "Prediction": y_pred_train.ravel()}
        )
        df_counts = df.apply(pd.value_counts)

        fig = go.Figure(
            data=[
                go.Bar(name="Actual", x=df_counts.index, y=df_counts["Actual"].values),
                go.Bar(
                    name="Prediction",
                    x=df_counts.index,
                    y=df_counts["Prediction"].values,
                ),
            ]
        )
        # Change the bar mode
        fig.update_xaxes(title_text="Number of clusters", showgrid=False)
        fig.update_yaxes(title_text="Counts", showgrid=False)
        fig.update_layout(
            title_text="Cluster distribution", title_x=0.5, barmode="group"
        )

        figures = [
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        ]

        return self.cache_results(figures=figures)
