# Copyright © 2023 ValidMind Inc. All rights reserved.
from dataclasses import dataclass

import pandas as pd
import scorecardpy as sc

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class WOEBinTable(Metric):
    """
    Implements WoE-based automatic binning for features in a dataset and calculates their Information Value (IV).
    Utilizes the 'scorecardpy' library for the binning process.
    """

    name = "woe_bin_table"
    required_context = ["dataset"]
    default_params = {"breaks_adj": None}

    def run(self):
        target_column = self.dataset.target_column
        breaks_adj = self.params["breaks_adj"]

        df = self.dataset.df
        print(
            f"Running with breaks_adj: {breaks_adj}"
        )  # print the breaks_adj being used
        bins_df = self.binning_data(df, target_column, breaks_adj)

        return self.cache_results(
            {
                "woe_iv": bins_df.to_dict(orient="records"),
            }
        )

    def binning_data(self, df, y, breaks_adj=None):
        """
        This function performs automatic binning using WoE.
        df: A pandas dataframe
        y: The target variable in quotes, e.g. 'target'
        """
        non_numeric_cols = df.select_dtypes(exclude=["int64", "float64"]).columns
        df[non_numeric_cols] = df[non_numeric_cols].astype(str)

        try:
            print(
                f"Performing binning with breaks_adj: {breaks_adj}"
            )  # print the breaks_adj being used
            bins = sc.woebin(df, y, breaks_list=breaks_adj)
        except Exception as e:
            print("Error during binning: ")
            print(e)
        else:
            bins_df = pd.concat(bins.values(), keys=bins.keys())
            bins_df.reset_index(inplace=True)
            bins_df.drop(columns=["variable"], inplace=True)
            bins_df.rename(columns={"level_0": "variable"}, inplace=True)

            bins_df["bin_number"] = bins_df.groupby("variable").cumcount()

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
