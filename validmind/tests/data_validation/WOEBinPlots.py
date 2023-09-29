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
    **Purpose**: The purpose of this test is to perform a visual analysis of the Weight of Evidence (WoE) and
    Information Value (IV) for categorical variables in a provided dataset. This aids in understanding the predictive
    power of each variable in a classification-based machine learning model by displaying the data distribution over
    the different categories of each feature. WoE and IV are common metric in credit scoring models and provide
    reliable statistical measures for variables' predictive power.

    **Test Mechanism**: The test mechanism proceeds in predefined steps. It first selects non-numeric columns and
    converts them to string type for proper binning. Afterward, it performs an automatic WoE binning on the selected
    features in the dataset, which effectively groups the possible values of a variable into bins or categories. Once
    this is done, the function generates two visual charts for each variable - a Bar chart for IV and a Scatter chart
    for WoE values. These visualizations are rendered based on the distribution of the respective metric across the
    different categories of each feature.

    **Signs of High Risk**: Indicators of high potential risk include an error occurring during the binning process or
    issues converting non-numeric columns to string data type. Furthermore, an uneven distribution of WoE and IV,
    especially if certain bins dominate others significantly, might indicate that the model is excessively relying on
    certain variables or categories for predictions, which could have an adverse impact on the model's generalizability
    and robustness.

    **Strengths**: One of the strengths of using this metric is that it provides a detailed visual presentation of how
    feature categories relate to the target variable, giving an intuitive understanding of the feature's contribution
    to the model. It also allows easy identification of highly impacting features, which can aid in feature selection
    and in understanding the decision logic of the model. Furthermore, WoE transformations are monotonic, meaning they
    preserve the rank ordering of the original data points, which simplifies subsequent analyses.

    **Limitations**: One of the limitations of this method is that it is largely dependent on the binning process. An
    inappropriate choice of the number of bins or the binning thresholds can lead to an inadequate representation of
    the variable's distribution. Also, this method is most suitable for categorical data; encoding continuous variables
    to categorical might sometimes lead to loss of information. Another limitation is that extreme or outlier values
    can have a significant impact on WoE and IV calculation. Finally, it requires sufficient events per bin in order to
    give reliable information value and weight of evidence.
    """

    name = "woe_bin_plots"
    required_context = ["dataset"]
    default_params = {"breaks_adj": None, "fig_height": 600, "fig_width": 500}
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "categorical_data"],
    }

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
