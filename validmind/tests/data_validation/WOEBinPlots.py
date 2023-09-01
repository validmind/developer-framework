# Copyright © 2023 ValidMind Inc. All rights reserved.
from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scorecardpy as sc
from plotly.subplots import make_subplots

from validmind.vm_models import Figure, Metric


@dataclass
class WOEBinPlots(Metric):
    """
    Generates a visual analysis of the WoE and IV values distribution for categorical variables.
    The input dataset is required.
    """

    name = "woe_bin_plots"
    required_context = ["dataset"]
    default_params = {"breaks_adj": None, "fig_height": 600, "fig_width": 500}

    def run(self):
        df = self.dataset.df
        target_column = self.dataset.target_column
        fig_height = self.params["fig_height"]
        fig_width = self.params["fig_width"]
        breaks_adj = self.params["breaks_adj"]

        woe_iv_df = self.binning_data(df, target_column, breaks_adj)
        return self.plot_woe_iv_distribution(woe_iv_df, fig_height, fig_width)

    def binning_data(self, df, y, breaks_adj=None):
        """
        This function performs automatic binning using WoE.
        df: A pandas dataframe
        y: The target variable in quotes, e.g. 'target'
        """

        non_numeric_cols = df.select_dtypes(exclude=["int64", "float64"]).columns
        df[non_numeric_cols] = df[non_numeric_cols].astype(str)

        try:
            bins = sc.woebin(df, y, breaks_list=breaks_adj)
        except Exception as e:
            print("Error during binning: ")
            print(e)
        else:
            bins_df = pd.concat(bins.values(), keys=bins.keys())
            bins_df.reset_index(inplace=True)
            bins_df.drop(columns=["variable"], inplace=True)
            bins_df.rename(
                columns={"level_0": "variable", "level_1": "bin_number"}, inplace=True
            )

            return bins_df

    def plot_woe_iv_distribution(self, woe_iv_df, fig_height, fig_width):
        variables = woe_iv_df["variable"].unique()

        figures = []
        for variable in variables:
            variable_df = woe_iv_df[woe_iv_df["variable"] == variable]

            fig = make_subplots(rows=1, cols=2)

            fig.add_trace(
                go.Bar(
                    x=variable_df["bin"],
                    y=variable_df["bin_iv"],
                    marker_color=px.colors.qualitative.Plotly[
                        : len(variable_df["bin"])
                    ],
                    hovertemplate="<b>%{x}</b><br>" + "IV: %{y}<extra></extra>",
                ),
                row=1,
                col=1,
            )
            fig.update_xaxes(
                ticktext=variable_df["bin"].tolist(),
                tickvals=np.arange(len(variable_df["bin"])),
                row=1,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=variable_df["bin"],
                    y=variable_df["woe"],
                    mode="lines+markers",
                    marker=dict(symbol="circle", size=6),
                    hovertemplate="<b>%{x}</b><br>" + "WoE: %{y}<extra></extra>",
                ),
                row=1,
                col=2,
            )
            fig.update_xaxes(
                ticktext=variable_df["bin"].tolist(),
                tickvals=np.arange(len(variable_df["bin"])),
                row=1,
                col=2,
            )

            fig.update_layout(
                title=f"IV and WoE for {variable}",
                height=fig_height,
                width=fig_width,
                showlegend=False,
            )

            figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.key}:{variable}",
                    figure=fig,
                )
            )

        return self.cache_results(figures=figures)
