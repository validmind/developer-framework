# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from dataclasses import dataclass
from validmind.vm_models import Figure, Metric
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


@dataclass
class WOEIVPlots(Metric):
    """
    Generates a visual analysis of the WoE and IV values distribution for categorical variables.
    The input dataset is required.
    """

    name = "woe_and_iv_plots"
    required_context = ["dataset"]
    default_params = {"fig_height": 600, "fig_width": 500, "features": None}

    def run(self):
        df = self.dataset.df
        target_column = self.dataset.target_column
        features = self.params["features"]
        fig_height = self.params["fig_height"]
        fig_width = self.params["fig_width"]

        woe_iv_df = self.calculate_woe_iv(df, target_column, features)
        return self.plot_woe_iv_distribution(woe_iv_df, fig_height, fig_width)

    @staticmethod
    def calculate_woe_iv(df, target_column, features=None):
        # If no specific features specified, use all columns in the DataFrame
        if features is None:
            features = df.drop(target_column, axis=1).columns.tolist()

        # Create a dataframe to store WoE and IV values
        master = []

        for feature in features:
            lst = []

            # For each unique category in the feature
            for val in df[feature].unique():
                lst.append(
                    {
                        "Variable": feature,
                        "Value": val,
                        "All": df[df[feature] == val].count()[feature],
                        "Good": df[
                            (df[feature] == val) & (df[target_column] == 0)
                        ].count()[feature],
                        "Bad": df[
                            (df[feature] == val) & (df[target_column] == 1)
                        ].count()[feature],
                    }
                )

            dset = pd.DataFrame(lst)

            # Calculate WoE and IV
            dset["Distr_Good"] = dset["Good"] / dset["Good"].sum()
            dset["Distr_Bad"] = dset["Bad"] / dset["Bad"].sum()
            dset["WoE"] = np.log(
                (dset["Distr_Good"] + 0.0001) / (dset["Distr_Bad"] + 0.0001)
            )  # Avoid divide by zero
            dset["IV"] = (dset["Distr_Good"] - dset["Distr_Bad"]) * dset["WoE"]

            master.append(dset)

        master_dset = pd.concat(master, ignore_index=True)

        return master_dset.sort_values(by=["Variable", "WoE"])

    def plot_woe_iv_distribution(self, woe_iv_df, fig_height, fig_width):
        variables = woe_iv_df["Variable"].unique()

        figures = []
        for variable in variables:
            variable_df = woe_iv_df[woe_iv_df["Variable"] == variable]

            fig = make_subplots(rows=1, cols=2)  # Adjusted for 1 row and 2 columns

            # IV bar plot
            fig.add_trace(
                go.Bar(
                    x=variable_df["Value"],
                    y=variable_df["IV"],
                    marker_color=px.colors.qualitative.Plotly[
                        : len(variable_df["Value"])
                    ],
                    hovertemplate="<b>%{x}</b><br>" + "IV: %{y}<extra></extra>",
                ),
                row=1,
                col=1,  # Adjusted for column 1
            )
            fig.update_xaxes(
                ticktext=variable_df["Value"].tolist(),
                tickvals=np.arange(len(variable_df["Value"])),
                row=1,
                col=1,  # Adjusted for column 1
            )

            # WoE trend plot
            fig.add_trace(
                go.Scatter(
                    x=variable_df["Value"],
                    y=variable_df["WoE"],
                    mode="lines+markers",
                    marker=dict(symbol="circle", size=6),
                    hovertemplate="<b>%{x}</b><br>" + "WoE: %{y}<extra></extra>",
                ),
                row=1,
                col=2,  # Adjusted for column 2
            )
            fig.update_xaxes(
                ticktext=variable_df["Value"].tolist(),
                tickvals=np.arange(len(variable_df["Value"])),
                row=1,
                col=2,  # Adjusted for column 2
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
