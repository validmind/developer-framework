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
        """
        Calculate the Weight of Evidence (WoE) and Information Value (IV) of categorical features.

        Parameters:
        df (pandas.DataFrame): DataFrame to be processed. It should contain the target column.
        target_column (str): Name of the target column in the DataFrame.
        features (list, optional): List of feature names for which WoE and IV is to be calculated.
                                If None, all features in df will be used.
        order_by (list, optional): List of column names to order the resulting DataFrame by.
                                If None, ["Variable", "WoE"] will be used as the default.

        Returns:
        pandas.DataFrame: A DataFrame with the WoE and IV for each category of the feature(s).
        """

        if features is None:
            features = self.params.get("features")

        if order_by is None:
            order_by = self.params.get("order_by")

        # Check if features parameter is provided and valid
        if features is not None:
            if not isinstance(features, list):
                raise ValueError("The 'features' parameter must be a list.")
            invalid_features = set(features) - set(df.columns)
            if invalid_features:
                raise ValueError(
                    f"The following features are not found in the DataFrame: {invalid_features}"
                )

        # If no specific features specified, use all columns in the DataFrame
        if features is None:
            features = df.drop(target_column, axis=1).columns.tolist()

        # Create a dataframe to store WoE and IV values
        master = []

        for feature in features:
            lst = []

            # For each unique category in the feature
            for val in df[feature].unique():
                lst.append(
                    {
                        "Feature": feature,
                        "Category": val,
                        "All": df[df[feature] == val].count()[feature],
                        "Good": df[
                            (df[feature] == val) & (df[target_column] == 0)
                        ].count()[feature],
                        "Bad": df[
                            (df[feature] == val) & (df[target_column] == 1)
                        ].count()[feature],
                    }
                )

            dset = pd.DataFrame(lst)

            # Calculate WoE and IV
            dset["Distr_Good"] = dset["Good"] / dset["Good"].sum()
            dset["Distr_Bad"] = dset["Bad"] / dset["Bad"].sum()
            dset["WoE"] = np.log(dset["Distr_Good"] / dset["Distr_Bad"])
            dset["IV"] = (dset["Distr_Good"] - dset["Distr_Bad"]) * dset["WoE"]

            master.append(dset)

        master_dset = pd.concat(master, ignore_index=True)

        # Check if order_by parameter is provided and valid
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
