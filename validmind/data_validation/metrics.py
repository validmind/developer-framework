"""
Metrics functions for any dataset
"""
import numpy as np

from scipy.stats import t


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
