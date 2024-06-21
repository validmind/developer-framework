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
    Calculates and assesses the Weight of Evidence (WoE) and Information Value (IV) of each feature in a ML model.

    **Purpose**: The Weight of Evidence (WoE) and Information Value (IV) test is intended to evaluate the predictive
    power of each feature in the machine learning model. The test generates binned groups of values from each feature
    in a dataset, computes the WoE value and the IV value for each bin. These values provide insights on the
    relationship between each feature and the target variable and their contribution towards the predictive output of
    the model.

    **Test Mechanism**: The metric leverages the `scorecardpy.woebin` method to perform WoE-based automatic binning on
    the dataset. Depending on the parameter `breaks_adj`, the method adjusts the cut-off points for binning numeric
    variables. The bins are then used to calculate the WoE and IV. The metric requires a dataset with the target
    variable defined. The metric outputs a dataframe that comprises the bin boundaries, WoE, and IV values for each
    feature.

    **Signs of High Risk**:
    - High IV values, which denote variables with too much predictive power which might lead to overfitting
    - Errors during the binning process, which might be due to inappropriate data types or poorly defined bins

    **Strengths**:
    - The WoE and IV test is highly effective for feature selection in binary classification problems, as it quantifies
    how much predictive information is packed within each feature regarding the binary outcome
    - The WoE transformation creates a monotonic relationship between the target and independent variables

    **Limitations**:
    - Mainly designed for binary classification tasks, therefore it might not be applicable or reliable for multi-class
    classification or regression tasks
    - If the dataset has many features or the features are not binnable or they are non-numeric, this process might
    encounter difficulties
    - This metric doesn't help in identifying if the predictive factor being observed is a coincidence or a real
    phenomenon due to data randomness
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
