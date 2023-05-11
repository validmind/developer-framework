"""
Plot utilities
"""
import matplotlib.pylab as pylab
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from sklearn.metrics import r2_score

# Silence this warning: *c* argument looks like a single numeric RGB or
# RGBA sequence, which should be avoided
matplotlib_axes_logger.setLevel("ERROR")

sns.set(rc={"figure.figsize": (20, 10)})

params = {
    "legend.fontsize": "x-large",
    "axes.labelsize": "x-large",
    "axes.titlesize": "x-large",
    "xtick.labelsize": "x-large",
    "ytick.labelsize": "x-large",
}
pylab.rcParams.update(params)


def _format_axes(subplot):
    label_format = "{:,.0f}"
    ticks_loc = subplot.get_yticks().tolist()
    subplot.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    subplot.set_yticklabels([label_format.format(v) for v in ticks_loc])

    ticks_loc = subplot.get_xticks().tolist()
    subplot.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    subplot.set_xticklabels([label_format.format(v) for v in ticks_loc])


def get_box_plot(df, x, y):
    """
    Returns a box plot for a pair of features
    """
    subplot = sns.boxplot(x=x, y=y, data=df)
    _format_axes(subplot)

    # avoid drawing on notebooks
    plt.close()
    return subplot


def get_crosstab_plot(vm_dataset, x, y):
    """
    Returns a crosstab plot for a pair of features. If one of the features
    is the target column, we should not use it as an index
    """
    df = vm_dataset.df

    # If dataset targets were specified we try to use the target column as y
    if vm_dataset.targets:
        target_column = vm_dataset.targets.target_column
        if target_column == x:
            x = y
            y = target_column
        elif target_column == y:
            y = x
            x = target_column

    crosstab = pd.crosstab(index=df[x], columns=df[y])
    subplot = crosstab.plot.bar(rot=0)
    _format_axes(subplot)

    # avoid drawing on notebooks
    plt.close()
    return subplot


def get_scatter_plot(df, x, y):
    """
    Returns a scatter plot for a pair of features
    """
    df_with_no_nan = df.dropna(subset=[x, y])
    subplot = df_with_no_nan.plot.scatter(
        x=x, y=y, figsize=(20, 10), color="#DE257E", alpha=0.2
    )

    # Generate a 1d least squares fit to show a trend line
    z = np.polyfit(df_with_no_nan[x], df_with_no_nan[y], 1)
    p = np.poly1d(z)
    r2 = r2_score(df_with_no_nan[y], p(df_with_no_nan[x]))

    subplot.plot(
        df_with_no_nan[x],
        p(df_with_no_nan[x]),
        color="gray",
        linewidth=2,
        linestyle="dashed",
        label="Trendline - R-Squared Score: " + "{:.4f}".format(r2),
    )
    subplot.legend()
    _format_axes(subplot)

    # avoid drawing on notebooks
    plt.close()
    return subplot


def get_plot_for_feature_pair(vm_dataset, x, y):
    """
    Checks the data types for each feature pair and creates the
    appropriate plot to represent their relationship
    """
    df = vm_dataset.df
    x_type = vm_dataset.get_feature_type(x)
    y_type = vm_dataset.get_feature_type(y)

    # Easy case when we just need a scatter plot
    if x_type == "Numeric" and y_type == "Numeric":
        return get_scatter_plot(df, x, y)

    # When one feature is numerical, it needs to be plotted as a box plot
    # where X is the category and Y is the distribution of numerical values
    if x_type == "Numeric":
        return get_box_plot(df, y, x)
    elif y_type == "Numeric":
        return get_box_plot(df, x, y)

    # Now each feature is either categorical or Boolean
    return get_crosstab_plot(vm_dataset, x, y)
