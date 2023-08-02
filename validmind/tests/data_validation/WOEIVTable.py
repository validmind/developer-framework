# Copyright © 2023 ValidMind Inc. All rights reserved.

import numpy as np
import pandas as pd
from dataclasses import dataclass
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class WOEIVTable(Metric):
    """
    Calculate the Weight of Evidence (WoE) and Information Value (IV) of categorical features.
    The input dataset and target column are required.
    """

    name = "woe_iv_table"
    required_context = ["dataset"]
    default_params = {"features": None, "order_by": None}

    def _get_feature_categories(self, df, feature, target_column):
        lst = []

        for val in df[feature].unique():
            lst.append(
                {
                    "Feature": feature,
                    "Category": val,
                    "All": df[df[feature] == val].count()[feature],
                    "Good": df[(df[feature] == val) & (df[target_column] == 0)].count()[
                        feature
                    ],
                    "Bad": df[(df[feature] == val) & (df[target_column] == 1)].count()[
                        feature
                    ],
                }
            )

        return pd.DataFrame(lst)

    def _calculate_woe_iv_for_feature(self, dset):
        dset["Distr_Good"] = dset["Good"] / dset["Good"].sum()
        dset["Distr_Bad"] = dset["Bad"] / dset["Bad"].sum()
        dset["WoE"] = np.log(dset["Distr_Good"] / dset["Distr_Bad"])
        dset["IV"] = (dset["Distr_Good"] - dset["Distr_Bad"]) * dset["WoE"]

        return dset

    def run(self):
        target_column = self.dataset.target_column
        features = self.params["features"]
        order_by = self.params["order_by"]

        df = self.dataset.df

        summary_woe_iv = self.calculate_woe_iv(df, target_column, features, order_by)

        return self.cache_results(
            {
                "woe_iv": summary_woe_iv,
            }
        )

    def calculate_woe_iv(self, df, target_column, features=None, order_by=None):
        if features is None:
            features = self.params.get("features")

        if order_by is None:
            order_by = self.params.get("order_by")

        if features is not None:
            if not isinstance(features, list):
                raise ValueError("The 'features' parameter must be a list.")
            invalid_features = set(features) - set(df.columns)
            if invalid_features:
                raise ValueError(
                    f"The following features are not found in the DataFrame: {invalid_features}"
                )

        if features is None:
            features = df.drop(target_column, axis=1).columns.tolist()

        master = []

        for feature in features:
            dset = self._get_feature_categories(df, feature, target_column)
            dset = self._calculate_woe_iv_for_feature(dset)
            master.append(dset)

        master_dset = pd.concat(master, ignore_index=True)

        if order_by is None:
            order_by = ["Feature", "WoE"]
        else:
            invalid_columns = set(order_by) - set(dset.columns)
            if invalid_columns:
                raise ValueError(
                    f"The following columns are not found in the table: {invalid_columns}"
                )

        return master_dset.sort_values(by=order_by, ascending=False)

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
