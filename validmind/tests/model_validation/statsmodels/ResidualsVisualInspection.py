# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.seasonal import seasonal_decompose

from validmind.vm_models import Figure, Metric


@dataclass
class ResidualsVisualInspection(Metric):
    """
    Provides a comprehensive visual analysis of residuals for regression models utilizing various plot types.

    **Purpose**: The main purpose of this metric is to visualize and analyze the residuals (the differences between the
    observed and predicted values) of a regression problem. It allows for a graphical exploration of the model's
    errors, helping to identify statistical patterns or anomalies that may indicate a systematic bias in the model's
    predictions. By inspecting the residuals, we can check how well the model fits the data and meets the assumptions
    of the model.

    **Test Mechanism**: The metric generates four common types of residual plots which are: a histogram with kernel
    density estimation, a quantile-quantile (Q-Q) plot, a residuals series dot plot, and an autocorrelation function
    (ACF) plot.

    - The residuals histogram with kernel density estimation visualizes the distribution of residuals and allows to
    check if they are normally distributed.
    - Q-Q plot compares the observed quantiles of the data to the quantiles of a standard normal distribution, helping
    to assess the normality of residuals.
    - A residuals dot plot indicates the variation in residuals over time, which helps in identifying any time-related
    pattern in residuals.
    - ACF plot visualizes the correlation of an observation with its previous observations, helping to pinpoint any
    seasonality effect within residuals.

    **Signs of High Risk**:

    - Skewness or asymmetry in the histogram or a significant deviation from the straight line in the Q-Q plot, which
    indicates that the residuals aren't normally distributed.
    - Large spikes in the ACF plot, indicating that the residuals are correlated, in violation of the assumption that
    they are independent.
    - Non-random patterns in the dot plot of residuals, indicating potential model misspecification.

    **Strengths**:

    - Visual analysis of residuals is a powerful yet simple way to understand a model’s behavior across the data set
    and to identify problems with the model's assumptions or its fit to the data.
    - The test is applicable to any regression model, irrespective of complexity.
    - By exploring residuals, we might uncover relationships that were not captured by the model, revealing
    opportunities for model improvement.

    **Limitations**:

    - Visual tests are largely subjective and can be open to interpretation. Clear-cut decisions about the model based
    solely on these plots may not be possible.
    - The metrics from the test do not directly infer the action based on the results; domain-specific knowledge and
    expert judgement is often required to interpret the results.
    - These plots can indicate a problem with the model but they do not necessarily reveal the nature or cause of the
    problem.
    - The test assumes that the error terms are identically distributed, which might not always be the case in
    real-world scenarios.
    """

    name = "residuals_visual_inspection"
    metadata = {
        "task_types": ["regression"],
        "tags": ["statsmodels", "visualization"],
    }

    def get_residuals(self, column, series):
        """
        Get the seasonal decomposition residuals from the test
        context or re-compute them if not available. This allows
        running the test individually or as part of a test suite.
        """
        sd_all_columns = self.test_context.get_context_data("seasonal_decompose")
        if sd_all_columns is None or column not in sd_all_columns:
            return seasonal_decompose(series, model="additive")

        return sd_all_columns[column]

    @staticmethod
    def residual_analysis(residuals, variable_name, axes):
        residuals = residuals.dropna().reset_index(
            drop=True
        )  # drop NaN values and reset index

        # QQ plot
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title(f"Residuals Q-Q Plot ({variable_name})")

        # Histogram with KDE
        sns.histplot(residuals, kde=True, ax=axes[0, 0])
        axes[0, 0].set_xlabel("Residuals")
        axes[0, 0].set_title(f"Residuals Histogram ({variable_name})")

        # Residual series dot plot
        sns.lineplot(data=residuals, linewidth=0.5, color="red", ax=axes[1, 0])
        axes[1, 0].set_title(f"Residual Series Dot Plot ({variable_name})")

        # ACF plot
        n_lags = min(100, len(residuals) - 1)  # Adjust the number of lags
        plot_acf(residuals, ax=axes[1, 1], lags=n_lags, zero=False)  # Added zero=False
        axes[1, 1].set_title(f"ACF Plot of Residuals ({variable_name})")

    def run(self):
        x_train = self.train_ds.df
        x_train = self.train_ds.df
        figures = []

        # TODO: specify which columns to plot via params
        for col in x_train.columns:
            sd = self.get_residuals(col, x_train[col])

            # Remove NaN values from the residuals and reset the index
            residuals = pd.Series(sd.resid).dropna().reset_index(drop=True)

            # Create subplots
            fig, axes = plt.subplots(nrows=2, ncols=2)
            fig.suptitle(f"Residuals Inspection for {col}", fontsize=24)

            self.residual_analysis(residuals, col, axes)

            # Adjust the layout
            plt.tight_layout()

            # Do this if you want to prevent the figure from being displayed
            plt.close("all")

            figures.append(
                Figure(
                    for_object=self,
                    key=self.key,
                    figure=fig,
                )
            )
        return self.cache_results(figures=figures)
