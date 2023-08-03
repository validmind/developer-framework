# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from validmind.logging import get_logger
from validmind.vm_models import (
    Figure,
    Metric,
    Model,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
)

logger = get_logger(__name__)


@dataclass
class PopulationStabilityIndex(Metric):
    """
    Population Stability Index between two datasets
    """

    name = "psi"
    required_context = ["model"]

    def description(self):
        return """
        PSI is a widely-used metric to assess the stability of a predictive model's score distribution when comparing
        two separate samples (usually a development and a validation dataset or two separate time periods). It helps
        determine if a model's performance has changed significantly over time or if there is a major shift in the
        population characteristics.

        In this section, we compare the PSI between the training and test datasets.
        """

    def summary(self, metric_value):
        # Add a table with the PSI values for each feature
        # The data looks like this: [{"initial": 2652, "percent_initial": 0.5525, "new": 830, "percent_new": 0.5188, "psi": 0.0021},...
        psi_table = [
            {
                "Bin": i,
                "Count Initial": values["initial"],
                "Percent Initial (%)": values["percent_initial"] * 100,
                "Count New": values["new"],
                "Percent New (%)": values["percent_new"] * 100,
                "PSI": values["psi"],
            }
            for i, values in enumerate(metric_value)
        ]

        return ResultSummary(
            results=[
                ResultTable(
                    data=psi_table,
                    metadata=ResultTableMetadata(
                        title="Population Stability Index for Training and Test Datasets"
                    ),
                ),
            ]
        )

    def _get_psi(
        self, score_initial, score_new, num_bins=10, mode="fixed", as_dict=False
    ):
        """
        Taken from:
        https://towardsdatascience.com/checking-model-stability-and-population-shift-with-psi-and-csi-6d12af008783
        """
        eps = 1e-4

        # Sort the data
        score_initial.sort()
        score_new.sort()

        # Prepare the bins
        min_val = min(min(score_initial), min(score_new))
        max_val = max(max(score_initial), max(score_new))
        if mode == "fixed":
            bins = [
                min_val + (max_val - min_val) * (i) / num_bins
                for i in range(num_bins + 1)
            ]
        elif mode == "quantile":
            bins = pd.qcut(score_initial, q=num_bins, retbins=True)[
                1
            ]  # Create the quantiles based on the initial population
        else:
            raise ValueError(
                f"Mode '{mode}' not recognized. Allowed options are 'fixed' and 'quantile'"
            )
        bins[0] = min_val - eps  # Correct the lower boundary
        bins[-1] = max_val + eps  # Correct the higher boundary

        # Bucketize the initial population and count the sample inside each bucket
        bins_initial = pd.cut(score_initial, bins=bins, labels=range(1, num_bins + 1))
        df_initial = pd.DataFrame({"initial": score_initial, "bin": bins_initial})
        grp_initial = df_initial.groupby("bin").count()
        grp_initial["percent_initial"] = grp_initial["initial"] / sum(
            grp_initial["initial"]
        )

        # Bucketize the new population and count the sample inside each bucket
        bins_new = pd.cut(score_new, bins=bins, labels=range(1, num_bins + 1))
        df_new = pd.DataFrame({"new": score_new, "bin": bins_new})
        grp_new = df_new.groupby("bin").count()
        grp_new["percent_new"] = grp_new["new"] / sum(grp_new["new"])

        # Compare the bins to calculate PSI
        psi_df = grp_initial.join(grp_new, on="bin", how="inner")

        # Add a small value for when the percent is zero
        psi_df["percent_initial"] = psi_df["percent_initial"].apply(
            lambda x: eps if x == 0 else x
        )
        psi_df["percent_new"] = psi_df["percent_new"].apply(
            lambda x: eps if x == 0 else x
        )

        # Calculate the psi
        psi_df["psi"] = (psi_df["percent_initial"] - psi_df["percent_new"]) * np.log(
            psi_df["percent_initial"] / psi_df["percent_new"]
        )

        return psi_df.to_dict(orient="records")

    def run(self):
        model_library = Model.model_library(self.model.model)
        if (
            model_library == "statsmodels"
            or model_library == "pytorch"
            or model_library == "catboost"
        ):
            logger.info(f"Skiping PSI for {model_library} models")
            return

        psi_results = self._get_psi(
            self.model.predict_proba(self.model.train_ds.x).copy(),
            self.model.predict_proba(self.model.test_ds.x).copy(),
        )

        trace1 = go.Bar(
            x=list(range(len(psi_results))),
            y=[d["percent_initial"] for d in psi_results],
            name="Initial",
            marker=dict(color="#DE257E"),
        )
        trace2 = go.Bar(
            x=list(range(len(psi_results))),
            y=[d["percent_new"] for d in psi_results],
            name="New",
            marker=dict(color="#E8B1F8"),
        )

        trace3 = go.Scatter(
            x=list(range(len(psi_results))),
            y=[d["psi"] for d in psi_results],
            name="PSI",
            yaxis="y2",
            line=dict(color="#257EDE"),
        )

        layout = go.Layout(
            title="Population Stability Index (PSI) Plot",
            xaxis=dict(title="Bin"),
            yaxis=dict(title="Population Ratio"),
            yaxis2=dict(
                title="PSI",
                overlaying="y",
                side="right",
                range=[
                    0,
                    max(d["psi"] for d in psi_results) + 0.005,
                ],  # Adjust as needed
            ),
            barmode="group",
        )

        fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
        figure = Figure(
            for_object=self,
            key=self.key,
            figure=fig,
        )

        return self.cache_results(metric_value=psi_results, figures=[figure])
