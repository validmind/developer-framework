# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
import plotly.figure_factory as ff

from validmind.vm_models import Figure, Metric

# Define the 'coolwarm' color scale manually
COOLWARM = [[0, "rgb(95,5,255)"], [0.5, "rgb(255,255,255)"], [1, "rgb(255,5,0)"]]


class LaggedCorrelationHeatmap(Metric):
    """
    Generates a heatmap of correlations between the target variable and the lags of independent variables in the dataset.
    """

    name = "lagged_correlation_heatmap"
    required_inputs = ["dataset"]

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
        if isinstance(self.dataset.target_column, list):
            target_col = self.dataset.target_column[
                0
            ]  # take the first item from the list
        else:
            target_col = self.dataset.target_column

        independent_vars = list(self.dataset.get_features_columns())
        num_lags = self.params.get("num_lags", 10)

        if isinstance(target_col, list) and len(target_col) == 1:
            target_col = target_col[0]

        if not isinstance(target_col, str):
            raise ValueError(
                "The 'target_col' must be a single string or a list containing a single string"
            )

        df = self.dataset.df

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
