# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

from dataclasses import dataclass

import pandas as pd
import scorecardpy as sc

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class WOEBinTable(Metric):
    """
    Assesses the Weight of Evidence (WoE) and Information Value (IV) of each feature to evaluate its predictive power
    in a binary classification model.

    ### Purpose

    The Weight of Evidence (WoE) and Information Value (IV) test is designed to evaluate the predictive power of each
    feature in a machine learning model. This test generates binned groups of values from each feature, computes the
    WoE and IV for each bin, and provides insights into the relationship between each feature and the target variable,
    illustrating their contribution to the model's predictive capabilities.

    ### Test Mechanism

    The test uses the `scorecardpy.woebin` method to perform automatic binning of the dataset based on WoE. The method
    adjusts the cut-off points for binning numeric variables based on the parameter `breaks_adj`. The bins are then
    used to calculate the WoE and IV values, effectively creating a dataframe that includes the bin boundaries, WoE,
    and IV values for each feature. A target variable is required in the dataset to perform this analysis.

    ### Signs of High Risk

    - High IV values, indicating variables with excessive predictive power which might lead to overfitting.
    - Errors during the binning process, potentially due to inappropriate data types or poorly defined bins.

    ### Strengths

    - Highly effective for feature selection in binary classification problems, as it quantifies the predictive
    information within each feature concerning the binary outcome.
    - The WoE transformation creates a monotonic relationship between the target and independent variables.

    ### Limitations

    - Primarily designed for binary classification tasks, making it less applicable or reliable for multi-class
    classification or regression tasks.
    - Potential difficulties if the dataset has many features, non-binnable features, or non-numeric features.
    - The metric does not help in distinguishing whether the observed predictive factor is due to data randomness or a
    true phenomenon.
    """

    name = "woe_bin_table"
    required_inputs = ["dataset"]
    default_params = {"breaks_adj": None}
    tasks = ["classification"]
    tags = ["tabular_data", "categorical_data"]

    def run(self):
        target_column = self.inputs.dataset.target_column
        breaks_adj = self.params["breaks_adj"]

        df = self.inputs.dataset.df
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
