# Copyright © 2023 ValidMind Inc. All rights reserved.

import pandas as pd
from dataclasses import dataclass
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata
import scorecardpy as sc


@dataclass
class WOEIVTable(Metric):
    """
    Calculate the Weight of Evidence (WoE) and Information Value (IV) of features.
    The input dataset and target column are required.
    """

    name = "woe_iv_table"
    required_context = ["dataset"]
    default_params = {}

    def run(self):
        target_column = self.dataset.target_column
        df = self.dataset.df
        summary_woe_iv = self.binning_data(df, target_column)
        return self.cache_results(
            {
                "woe_iv": summary_woe_iv.to_dict(orient="records"),
            }
        )

    def binning_data(self, df, y):
        """
        This function performs automatic binning using WoE.
        df: A pandas dataframe
        y: The target variable in quotes, e.g. 'target'
        """

        # Identify non-numeric columns
        non_numeric_cols = df.select_dtypes(exclude=["int64", "float64"]).columns

        # Convert non-numeric columns to string type
        df[non_numeric_cols] = df[non_numeric_cols].astype(str)

        # Perform binning
        try:
            bins = sc.woebin(df, y)
        except Exception as e:
            print("Error during binning: ")
            print(e)
        else:
            # Concatenate the individual dataframes into a single dataframe
            bins_df = pd.concat(bins.values(), keys=bins.keys())

            # Reset index and convert multi-index into columns
            bins_df.reset_index(inplace=True)

            # Drop the 'variable' column as it is identical to 'level_0'
            bins_df.drop(columns=["variable"], inplace=True)

            # Rename 'level_0' to 'variable' and 'level_1' to 'bin_number'
            bins_df.rename(
                columns={"level_0": "variable", "level_1": "bin_number"}, inplace=True
            )

            return bins_df

    def summary(self, metric_value):
        summary_woe_iv_table = metric_value["woe_iv"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=summary_woe_iv_table,
                    metadata=ResultTableMetadata(
                        title="Weight of Evidence (WoE) and Information Value (IV)"
                    ),
                )
            ]
        )
