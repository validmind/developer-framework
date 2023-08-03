# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from validmind.vm_models import (
    Figure,
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    TestResult,
    ThresholdTest,
)


@dataclass
class TimeSeriesMissingValues(ThresholdTest):
    """
    Test that the number of missing values is less than a threshold
    """

    category = "data_quality"
    name = "time_series_missing_values"
    required_context = ["dataset"]
    default_params = {"min_threshold": 1}

    def summary(self, results, all_passed):
        results_table = [
            {
                "Column": result.column,
                "Number of Missing Values": result.values["n_missing"],
                "Percentage of Missing Values (%)": result.values["p_missing"] * 100,
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(
                        title="Missing Values Results for Dataset"
                    ),
                )
            ]
        )

    def run(self):
        # Check if the index of dataframe is datetime
        is_datetime = pd.api.types.is_datetime64_any_dtype(self.dataset.df.index)
        if not is_datetime:
            raise ValueError("Dataset must be provided with datetime index")

        # Validate threshold paremeter
        if "min_threshold" not in self.params:
            raise ValueError("min_threshold must be provided in params")
        min_threshold = self.params["min_threshold"]

        rows = self.dataset.df.shape[0]
        missing = self.dataset.df.isna().sum()
        test_results = [
            TestResult(
                column=col,
                passed=missing[col] < min_threshold,
                values={"n_missing": missing[col], "p_missing": missing[col] / rows},
            )
            for col in missing.index
        ]

        fig_barplot = self._barplot(self.dataset.df, rotation=45)
        fig_heatmap = self._heatmap(self.dataset.df)
        test_figures = []
        if fig_barplot is not None:
            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:barplot",
                    figure=fig_barplot,
                    metadata={"type": "barplot"},
                )
            )
            test_figures.append(
                Figure(
                    for_object=self,
                    key=f"{self.name}:heatmap",
                    figure=fig_heatmap,
                    metadata={"type": "heatmap"},
                )
            )

        return self.cache_results(
            test_results,
            passed=all([r.passed for r in test_results]),
            # Don't pass figures until we figure out how to group metric-figures for multiple
            # executions inside a single test run
            # figures=test_figures,
        )

    def _barplot(self, df: pd.DataFrame, rotation: int = 45) -> plt.Figure:
        """
        Generate a bar plot of missing values in a pandas DataFrame.
        Args:
        df (pandas.DataFrame): The input DataFrame to plot the missing values of.
        rotation (int): The rotation angle for x-axis labels. Default is 45.
        font_size (int): The font size for x-axis and y-axis labels. Default is 18.
        Returns:
        matplotlib.figure.Figure: A matplotlib figure object containing the bar plot.
        """
        # Create a bar plot using seaborn library
        missing_values = df.isnull().sum()
        if sum(missing_values.values) != 0:
            fig, ax = plt.subplots()
            sns.barplot(
                data=missing_values,
                x=missing_values.index,
                y=missing_values.values,
                ax=ax,
                palette="Reds",
            )
            ax.set_xticklabels(
                labels=missing_values.index, rotation=rotation, fontsize=18
            )
            plt.yticks(rotation=45, fontsize=18)
            ax.set_title(
                "Total Number of Missing Values per Variable",
                weight="bold",
                fontsize=20,
            )
        else:
            fig = None

        return fig

    def _heatmap(self, df):
        """
        Plots a heatmap to visualize missing values in a dataframe with actual years on the x-axis.
        Args:
        df (pandas.DataFrame): The input dataframe to visualize.
        Returns:
        matplotlib.figure.Figure: A matplotlib figure object representing the heatmap plot.
        Raises:
        None
        """
        # Create a boolean mask for missing values
        missing_mask = df.isnull()
        # Set seaborn plot style
        sns.set(style="darkgrid")
        fig, ax = plt.subplots()

        # Plot the heatmap
        sns.heatmap(missing_mask.T, cmap="Reds", cbar=False, xticklabels=False, ax=ax)

        # Add actual years on the x-axis
        years = df.index.year.unique()
        xticks = [
            df.index.get_loc(df.index[df.index.year == year][0]) for year in years
        ]

        plt.xticks(xticks, years, rotation=45, fontsize=18)
        plt.yticks(rotation=45, fontsize=18)
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
        ax.set_xlabel("")
        ax.set_title(
            "Missing Values Heatmap",
            weight="bold",
            fontsize=20,
        )
        # Do this if you want to prevent the figure from being displayed
        plt.close("all")

        return fig
