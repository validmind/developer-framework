"""
Metrics functions for any dataset
"""
import numpy as np
import pandas as pd

from scipy.stats import t


def psi(score_initial, score_new, num_bins=10, mode="fixed", as_dict=False):
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


def csi(x_train, x_val):
    """
    Calculates PSI for each of the dataset features
    """
    csi_values = {}
    for col in x_train.columns:
        psi_df = psi(x_train[col].values, x_val[col].values)
        csi_value = np.mean(psi_df["psi"])
        csi_values[col] = csi_value

    return csi_values


def correlation_significance(r, n):
    """
    Calculates the significance of a Pearson correlation coefficient

    :param r: Pearson correlation coefficient
    :param n: Number of samples
    """
    if r == 1:
        return -1

    t_stat = r * np.sqrt((n - 2) / (1 - r**2))
    p_val = t.sf(np.abs(t_stat), n - 2) * 2

    return p_val
