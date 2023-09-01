# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import plotly.express as px
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class DefaultRatesbyRiskBandPlot(Metric):
    """
    Default Rates per Risk Band Bar Plot
    """

    name = "default_rates_by_risk_band_plot"
    required_context = ["dataset"]
    default_parameters = {"title": "Percentage of Total Accounts by Risk Band"}

    def description(self):
        return """
        This metric calculates the default rates for each risk band in the data,
        and creates a bar plot to visualize these rates.
        The bar plot offers a straightforward view of default rates across different risk bands,
        which can help with evaluating and comparing the performance of credit risk models.
        """

    @staticmethod
    def plot_band_percentages(df, risk_band_column, title):
        # Calculate the count of accounts in each risk band
        risk_band_counts = df[risk_band_column].value_counts().sort_index()

        # Convert to percentage
        total_accounts = len(df)
        risk_band_percentages = (risk_band_counts / total_accounts) * 100

        # Use 'Dark24' color sequence for more distinguishable colors
        colors = px.colors.qualitative.Dark24[: len(risk_band_percentages)]

        # Create the bar plot
        fig = go.Figure(
            data=[
                go.Bar(
                    x=risk_band_percentages.index,
                    y=risk_band_percentages.values,
                    marker_color=colors,
                )
            ]
        )

        # Customize the plot
        fig.update_layout(
            title_text=title,
            xaxis_title="Risk Band",
            yaxis_title="Percentage of Total Accounts",
        )

        return fig, risk_band_percentages

    def run(self):
        df = self.dataset
        risk_band_column = self.params["risk_band_column"]
        title = self.params["title"]

        fig, risk_band_percentages = self.plot_band_percentages(
            df, risk_band_column, title
        )

        return self.cache_results(
            metric_value={
                "band_percentages": risk_band_percentages.to_dict(),
            },
            figures=[
                Figure(
                    for_object=self,
                    key="band_percentages",
                    figure=fig,
                )
            ],
        )
