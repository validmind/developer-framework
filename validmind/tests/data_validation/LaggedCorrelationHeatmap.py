# Copyright © 2023 ValidMind Inc. All rights reserved.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from validmind.vm_models import Figure, Metric


class LaggedCorrelationHeatmap(Metric):
    """
    Generates a heatmap of correlations between the target variable and the lags of independent variables in the dataset.
    """

    name = "lagged_correlation_heatmap"
    required_context = ["dataset"]

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

        fig, ax = plt.subplots()
        sns.heatmap(
            correlation_df,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            annot_kws={"size": 16},
        )
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=16)  # Here you can set the font size
        fig.suptitle(
            f"Correlations between {target_col} and Lags of Features",
            fontsize=20,
            weight="bold",
            y=0.95,
        )
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.xlabel("Lags", fontsize=18)

        return fig

    def run(self):
        target_col = [self.dataset.target_column]
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
        plt.close("all")

        return self.cache_results(
            figures=figures,
        )
