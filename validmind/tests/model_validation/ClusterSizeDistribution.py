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
    Compares and visualizes the distribution of cluster sizes in model predictions and actual data for assessing
    clustering model performance.

    **Purpose:** The purpose of the `ClusterSizeDistribution` metric is to assess the performance of clustering models.
    It does this by comparing the distribution of cluster sizes in the predictions made by the model and the actual
    data. Observing the cluster distribution helps gain insights into whether the model's output aligns well with the
    actual dataset distribution.

    **Test Mechanism:** The testing mechanism for `ClusterSizeDistribution` involves first running the clustering model
    on the training dataset, storing predictions, and comparing these predictions with the actual output. The actual
    and predicted outputs are then converted into pandas dataframes, which conveniently enables the use of pandas
    built-in functions to derive cluster size distributions. Two histograms are constructed from this data: one for the
    actual distribution and one for the predicted distribution. These histograms are then plotted side-by-side for
    visual comparison.

    **Signs of High Risk:**
    * Discrepancies between the actual cluster size distribution and the predicted cluster size distribution may
    indicate high risk.
    * An irregular distribution of data across clusters in the predicted outcomes points towards an inaccurate
    prediction model.
    * A high number of outlier clusters could indicate that the model has trouble correctly grouping data.

    **Strengths:**
    * `ClusterSizeDistribution` provides a visual and intuitive way to compare the performance of the clustering model
    against the actual data.
    * This metric can effectively reveal where the model might be over- or underestimating cluster sizes.
    * It works well with any clustering models, making it a versatile comparison tool.

    **Limitations:**
    * The metric assumes that the actual cluster distribution is optimal, which may not always be the case.
    * It relies heavily on visual comparison, which might be subjective and may not provide a precise numerical measure
    of model performance.
    * The metric might not fully capture other important aspects of clustering such as cluster density, distances
    between clusters, and the shape of clusters.
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
