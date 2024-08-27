# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import numpy as np
import pandas as pd
import plotly.figure_factory as ff

from validmind.vm_models import Figure, Metric

# Define the 'coolwarm' color scale manually
COOLWARM = [[0, "rgb(95,5,255)"], [0.5, "rgb(255,255,255)"], [1, "rgb(255,5,0)"]]


class LaggedCorrelationHeatmap(Metric):
    """
    Assesses and visualizes correlation between target variable and lagged independent variables in a time-series
    dataset.

    ### Purpose

    The LaggedCorrelationHeatmap metric is utilized to appraise and illustrate the correlation between the target
    variable and delayed copies (lags) of independent variables in a time-series dataset. It assists in revealing
    relationships in time-series data where the influence of an independent variable on the dependent variable is not
    immediate but occurs after a period (lags).

    ### Test Mechanism

    To execute this test, Python's Pandas library pairs with Plotly to perform computations and present the
    visualization in the form of a heatmap. The test begins by extracting the target variable and corresponding
    independent variables from the dataset. Then, generation of lags of independent variables takes place, followed by
    the calculation of correlation between these lagged variables and the target variable. The outcome is a correlation
    matrix that gets recorded and illustrated as a heatmap, where different color intensities represent the strength of
    the correlation, making patterns easier to identify.

    ### Signs of High Risk

    - Insignificant correlations across the heatmap, indicating a lack of noteworthy relationships between variables.
    - Correlations that break intuition or previous understanding, suggesting potential issues with the dataset or the
    model.

    ### Strengths

    - This metric serves as an exceptional tool for exploring and visualizing time-dependent relationships between
    features and the target variable in a time-series dataset.
    - It aids in identifying delayed effects that might go unnoticed with other correlation measures.
    - The heatmap offers an intuitive visual representation of time-dependent correlations and influences.

    ### Limitations

    - The metric presumes linear relationships between variables, potentially ignoring non-linear relationships.
    - The correlation considered is linear; therefore, intricate non-linear interactions might be overlooked.
    - The metric is only applicable for time-series data, limiting its utility outside of this context.
    - The number of lags chosen can significantly influence the results; too many lags can render the heatmap difficult
    to interpret, while too few might overlook delayed effects.
    - This metric does not take into account any causal relationships, but merely demonstrates correlation.
    """

    name = "lagged_correlation_heatmap"
    required_inputs = ["dataset"]
    tasks = ["regression"]
    tags = ["time_series_data", "visualization"]

    def _compute_correlations(self, df, target_col, independent_vars, num_lags):
        correlations = np.zeros((len(independent_vars), num_lags + 1))

        for i, ind_var_col in enumerate(independent_vars):
            for lag in range(num_lags + 1):
                temp_df = pd.DataFrame(
                    {
                        target_col: df[target_col],
                        f"{ind_var_col}_lag{lag}": df[ind_var_col].shift(lag),
                    }
                )

                temp_df = temp_df.dropna()

                corr = temp_df[target_col].corr(temp_df[f"{ind_var_col}_lag{lag}"])

                correlations[i, lag] = corr

        return correlations

    def _plot_heatmap(self, correlations, independent_vars, target_col, num_lags):
        correlation_df = pd.DataFrame(
            correlations,
            columns=[f"{i}" for i in range(num_lags + 1)],
            index=independent_vars,
        )

        # Create heatmap using Plotly
        fig = ff.create_annotated_heatmap(
            z=correlation_df.values,
            x=list(correlation_df.columns),
            y=list(correlation_df.index),
            colorscale=COOLWARM,
            annotation_text=correlation_df.round(2).values,
            showscale=True,
        )

        fig.update_layout(
            title={
                "text": f"Correlations between {target_col} and Lags of Features",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font=dict(size=14),
            xaxis_title="Lags",
        )

        return fig

    def run(self):
        if isinstance(self.inputs.dataset.target_column, list):
            target_col = self.inputs.dataset.target_column[
                0
            ]  # take the first item from the list
        else:
            target_col = self.inputs.dataset.target_column

        independent_vars = list(self.inputs.dataset.feature_columns)
        num_lags = self.params.get("num_lags", 10)

        if isinstance(target_col, list) and len(target_col) == 1:
            target_col = target_col[0]

        if not isinstance(target_col, str):
            raise ValueError(
                "The 'target_col' must be a single string or a list containing a single string"
            )

        df = self.inputs.dataset.df

        correlations = self._compute_correlations(
            df, target_col, independent_vars, num_lags
        )
        fig = self._plot_heatmap(correlations, independent_vars, target_col, num_lags)

        figures = []
        figures.append(
            Figure(
                for_object=self,
                key=self.key,
                figure=fig,
            )
        )

        return self.cache_results(
            figures=figures,
        )
