# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import plotly.express as px
import plotly.graph_objects as go

from validmind.vm_models import Figure, Metric


@dataclass
class DefaultRatesbyRiskBandPlot(Metric):
    """
    Generates a bar plot showcasing the distribution of default rates across different risk bands in a dataset.

    **Purpose**:
    The Default Rates by Risk Band Plot metric aims to quantify and visually represent default rates across varying
    risk bands within a specific dataset. This information is essential in evaluating the functionality of credit risk
    models, by providing a comprehensive view of default rates across a range of risk categories.

    **Test Mechanism**:
    The applied test approach involves a calculated bar plot. This plot is derived by initially determining the count
    of accounts in every risk band and then converting these count values into percentages by dividing by the total
    quantity of accounts. The percentages are then depicted as a bar plot, clearly showcasing the proportion of total
    accounts associated with each risk band. Hence, the plot delivers a summarized depiction of default risk across
    various bands. The 'Dark24' color sequence is used in the plot to ensure each risk band is easily distinguishable.

    **Signs of High Risk**:
    - High risk may be indicated by a significantly large percentage of accounts associated with high-risk bands.
    - High exposure to potential default risk in the dataset indicates potential weaknesses in the model's capability
    to effectively manage or predict credit risk.

    **Strengths**:
    - The metric's primary strengths lie in its simplicity and visual impact.
    - The graphical display of default rates allows for a clear understanding of the spread of default risk across risk
    bands.
    - Using a bar chart simplifies the comparison between various risk bands and can highlight potential spots of high
    risk.
    - This approach assists in identifying any numerical imbalances or anomalies, thus facilitating the task of
    evaluating and contrasting performance across various credit risk models.

    **Limitations**:
    - The key constraint of this metric is that it cannot provide any insights as to why certain risk bands might have
    higher default rates than others.
    - If there is a large imbalance in the number of accounts across risk bands, the visual representation might not
    accurately depict the true distribution of risk.
    - Other factors contributing to credit risk beyond the risk bands are not considered.
    - The metric's reliance on a visual format might potentially lead to misinterpretation of results, as graphical
    depictions can sometimes be misleading.
    """

    name = "default_rates_by_risk_band_plot"
    required_context = ["dataset"]
    default_params = {"title": "Percentage of Total Accounts by Risk Band"}
    metadata = {
        "task_types": ["classification"],
        "tags": ["tabular_data", "visualization", "credit_risk"],
    }

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
