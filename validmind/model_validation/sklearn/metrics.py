"""
Metrics functions models trained with sklearn or that provide
a sklearn-like API
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.inspection import permutation_importance

from ...vm_models import Metric, Model


def _get_psi(score_initial, score_new, num_bins=10, mode="fixed", as_dict=False):
    """
    Taken from:
    https://towardsdatascience.com/checking-model-stability-and-population-shift-with-psi-and-csi-6d12af008783
    """
    eps = 1e-4

    # Sort the data
    score_initial.sort()
    score_new.sort()

    # Prepare the bins
    min_val = min(min(score_initial), min(score_new))
    max_val = max(max(score_initial), max(score_new))
    if mode == "fixed":
        bins = [
            min_val + (max_val - min_val) * (i) / num_bins for i in range(num_bins + 1)
        ]
    elif mode == "quantile":
        bins = pd.qcut(score_initial, q=num_bins, retbins=True)[
            1
        ]  # Create the quantiles based on the initial population
    else:
        raise ValueError(
            f"Mode '{mode}' not recognized. Your options are 'fixed' and 'quantile'"
        )
    bins[0] = min_val - eps  # Correct the lower boundary
    bins[-1] = max_val + eps  # Correct the higher boundary

    # Bucketize the initial population and count the sample inside each bucket
    bins_initial = pd.cut(score_initial, bins=bins, labels=range(1, num_bins + 1))
    df_initial = pd.DataFrame({"initial": score_initial, "bin": bins_initial})
    grp_initial = df_initial.groupby("bin").count()
    grp_initial["percent_initial"] = grp_initial["initial"] / sum(
        grp_initial["initial"]
    )

    # Bucketize the new population and count the sample inside each bucket
    bins_new = pd.cut(score_new, bins=bins, labels=range(1, num_bins + 1))
    df_new = pd.DataFrame({"new": score_new, "bin": bins_new})
    grp_new = df_new.groupby("bin").count()
    grp_new["percent_new"] = grp_new["new"] / sum(grp_new["new"])

    # Compare the bins to calculate PSI
    psi_df = grp_initial.join(grp_new, on="bin", how="inner")

    # Add a small value for when the percent is zero
    psi_df["percent_initial"] = psi_df["percent_initial"].apply(
        lambda x: eps if x == 0 else x
    )
    psi_df["percent_new"] = psi_df["percent_new"].apply(lambda x: eps if x == 0 else x)

    # Calculate the psi
    psi_df["psi"] = (psi_df["percent_initial"] - psi_df["percent_new"]) * np.log(
        psi_df["percent_initial"] / psi_df["percent_new"]
    )

    if as_dict:
        return psi_df.to_dict(orient="records")

    # Return the psi values dataframe
    return psi_df


@dataclass
class PermutationFeatureImportance(Metric):
    """
    Permutation Feature Importance
    """

    type = "training"
    scope = "training_dataset"
    key = "pfi"

    def run(self, vm_model: Model, x, y):
        model = vm_model.model

        pfi_values = permutation_importance(
            model.model, x, y, random_state=0, n_jobs=-2
        )
        pfi = {}
        for i, column in enumerate(x.columns):
            pfi[column] = [pfi_values["importances_mean"][i]], [
                pfi_values["importances_std"][i]
            ]

        self.cache_results(pfi)


@dataclass
class CharacteristicStabilityIndex(Metric):
    """
    Characteristic Stability Index between two datasets
    """

    type = "training"
    scope = "training:validation"  # should be set when running test plan
    key = "csi"
    value_formatter = "key_values"

    def run(self, train_ds, test_ds):
        """
        Calculates PSI for each of the dataset features
        """
        x_train = train_ds.raw_dataset.drop(columns=train_ds.target_column)
        x_test = test_ds.raw_dataset.drop(columns=test_ds.target_column)

        csi_values = {}
        for col in x_train.columns:
            psi_df = _get_psi(x_train[col].values, x_test[col].values)
            csi_value = np.mean(psi_df["psi"])
            csi_values[col] = csi_value

        self.cache_results(csi_values)
        return csi_values


@dataclass
class PopulationStabilityIndex(Metric):
    """
    Population Stability Index between two datasets
    """

    type = "training"
    scope = "training:validation"  # should be set when running test plan
    key = "psi"
    value_formatter = "records"

    def run(self, y_train_predict, y_test_predict):
        psi_df = _get_psi(y_train_predict, y_test_predict)

        self.cache_results(psi_df)
        return psi_df
