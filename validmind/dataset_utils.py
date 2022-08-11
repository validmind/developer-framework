"""
Utilities for inspecting and extracting statistics from client datasets
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet

# Silence this warning: *c* argument looks like a single numeric RGB or
# RGBA sequence, which should be avoided
matplotlib_axes_logger.setLevel("ERROR")

from .dataset import Dataset

sns.set(rc={"figure.figsize": (20, 10)})

DEFAULT_HISTOGRAM_BINS = 10


def _get_histogram(df, field, type_):
    """
    Returns a histogram for a numerical or categorical field
    """
    # Set the minimum number of bins to nunique if it's less than the default
    if type_ == "Numeric":
        unique = df[field].nunique()
        num_bins = min(unique, DEFAULT_HISTOGRAM_BINS)
        values = df[field].to_numpy()
        values_cleaned = values[~np.isnan(values)]
        hist = np.histogram(values_cleaned, bins=num_bins)
        return {
            "bin_edges": hist[1].tolist(),
            "counts": hist[0].tolist(),
        }
    elif type_ == "Categorical" or type_ == "Boolean":
        return df[field].value_counts().to_dict()
    else:
        raise ValueError(
            f"Unsupported field type found when computing its histogram: {type_}"
        )


def _add_field_statistics(df, field, analyze_opts=None):
    """
    We're moving the statistics to the `fields` attribute of the dataset
    in order to be more consistent, but still keeping the old statistics
    with `histogram`s until they are migrated as well
    """
    field_type = field["type"]
    field_type_options = field.get("type_options", dict())

    # Force a categorical field when it's declared as a primary key
    if field_type_options.get("primary_key", False):
        field_type = "Categorical"
        field["type"] = "Categorical"

    # - When we call describe on one field at a time, Pandas will
    #   know better if it needs to report on numerical or categorical statistics
    # - Boolean (binary) fields should be reported as categorical
    #       (force to categorical when nunique == 2)
    if field_type == ["Boolean"] or df[field["id"]].nunique() == 2:
        top_value = df[field["id"]].value_counts().nlargest(1)

        field["statistics"] = {
            "count": df[field["id"]].count(),
            "unique": df[field["id"]].nunique(),
            "top": top_value.index[0],
            "freq": top_value.values[0],
        }
    elif field_type == "Numeric":
        field["statistics"] = df[field["id"]].describe().to_dict()
    elif field_type == "Categorical":
        field["statistics"] = df[field["id"]].astype("category").describe().to_dict()

    field["statistics"]["n_missing"] = df[field["id"]].isna().sum()
    field["statistics"]["missing"] = field["statistics"]["n_missing"] / len(
        df[field["id"]]
    )
    field["statistics"]["n_distinct"] = df[field["id"]].nunique()
    field["statistics"]["distinct"] = field["statistics"]["n_distinct"] / len(
        df[field["id"]]
    )


def _format_axes(subplot):
    label_format = "{:,.0f}"
    ticks_loc = subplot.get_yticks().tolist()
    subplot.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    subplot.set_yticklabels([label_format.format(v) for v in ticks_loc])

    ticks_loc = subplot.get_xticks().tolist()
    subplot.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    subplot.set_xticklabels([label_format.format(v) for v in ticks_loc])


def _get_scatter_plot(df, x, y):
    """
    Returns a scatter plot for a pair of features
    """
    subplot = df.plot.scatter(x=x, y=y, figsize=(20, 10))
    _format_axes(subplot)

    # avoid drawing on notebooks
    plt.close()
    return subplot


def _get_box_plot(df, x, y):
    """
    Returns a box plot for a pair of features
    """
    subplot = sns.boxplot(x=x, y=y, data=df)
    _format_axes(subplot)
    # avoid drawing on notebooks
    plt.close()
    return subplot


def _get_crosstab_plot(df, vm_dataset, x, y):
    """
    Returns a crosstab plot for a pair of features. If one of the features
    is the target column, we should not use it as an index
    """
    target_column = vm_dataset.targets.target_column
    if target_column == x:
        x = y
        y = target_column
    elif target_column == y:
        y = target_column
        x = y

    crosstab = pd.crosstab(index=df[x], columns=df[y])
    subplot = crosstab.plot.bar(rot=0)
    _format_axes(subplot)
    # avoid drawing on notebooks
    plt.close()
    return subplot


def _get_plot_for_feature_pair(df, vm_dataset, x, y):
    """
    Checks the data types for each feature pair and creates the
    appropriate plot to represent their relationship
    """
    x_type = vm_dataset.get_feature_type(x)
    y_type = vm_dataset.get_feature_type(y)

    # Easy case when we just need a scatter plot
    if x_type == "Numeric" and y_type == "Numeric":
        return _get_scatter_plot(df, x, y)

    # When one feature is numerical, it needs to be plotted as a box plot
    # where X is the category and Y is the distribution of numerical values
    if x_type == "Numeric":
        return _get_box_plot(df, y, x)
    elif y_type == "Numeric":
        return _get_box_plot(df, x, y)

    # Now each feature is either categorical or Boolean
    return _get_crosstab_plot(df, vm_dataset, x, y)


def _generate_correlation_plots(df, vm_dataset, correlation_matrix, n_top=15):
    correlation_matrix = correlation_matrix.abs()
    corr_matrix_abs_us = correlation_matrix.unstack()
    sorted_correlated_features = corr_matrix_abs_us.sort_values(
        kind="quicksort", ascending=False
    ).reset_index()

    # Remove comparisons of the same feature
    sorted_correlated_features = sorted_correlated_features[
        (sorted_correlated_features.level_0 != sorted_correlated_features.level_1)
    ]

    # Remove duplicates
    sorted_correlated_features = sorted_correlated_features.iloc[:-2:2]

    sorted_correlated_features = sorted_correlated_features[:n_top]

    plots = []
    for fields in sorted_correlated_features.values:
        x, y, value = fields
        fields = ":".join(sorted([x, y]))
        key = f"corr:{fields}"
        subplot = _get_plot_for_feature_pair(df, vm_dataset, x, y)
        plots.append(
            {
                "type": "correlation-pearson",
                "figure": subplot.figure,
                "key": key,
                "metadata": {"x": x, "y": y, "value": value},
            }
        )
    return plots


def _analyze_pd_dataset(df, vm_dataset, analyze_opts=None):
    """
    Runs basic analysis tasks on a Pandas dataset:

    - Descriptive statistics
    - Pearson correlation matrix
    - Histograms for distribution of values
    """
    fields = vm_dataset.fields
    # TODO - accept analyze_opts to configure how to extract different metrics
    statistics = df.describe().to_dict(orient="dict")

    for field in fields:
        field_type = field["type"]
        # Temporary hack until histograms are separated from statistics
        if field["id"] not in statistics:
            statistics[field["id"]] = {}

        statistics[field["id"]]["histogram"] = _get_histogram(
            df, field["id"], field_type
        )

        _add_field_statistics(df, field, analyze_opts)

    correlation_matrix = df.corr()
    # Transform to the current format expected by the UI
    correlations = [
        [
            {
                "field": key,
                "value": value,
            }
            for key, value in correlation_row.items()
        ]
        for correlation_row in correlation_matrix.to_dict(orient="records")
    ]

    correlation_plots = _generate_correlation_plots(
        df, vm_dataset, correlation_matrix, n_top=15
    )

    return {
        "correlations": {
            "pearson": correlations,
        },
        "correlations_plots": {
            "pearson": correlation_plots,
        },
        "statistics": statistics,
    }


def _validate_pd_dataset_targets(df, targets):
    unique_targets = df[targets.target_column].unique()
    if len(unique_targets) != len(targets.class_labels):
        raise ValueError(
            f"The number of unique values ({unique_targets}) in the target column does not match the number of unique class labels."
        )

    for target in unique_targets:
        if str(target) not in targets.class_labels:
            raise ValueError(
                f'The target column contains a value ("{target}") that is not in the list of class labels.'
            )

    return True


def _validate_dataset_features(df, features):
    """
    Validates that the features list that was manually passed is valid and returns
    a feature map so the full dataset features list can be built by merging from
    df.columns. A faeture should at least have an "id" field.
    Validation for other fields TBD
    """
    feature_map = {}

    for feature in features:
        if "id" not in feature:
            raise ValueError(f"Feature {feature.__dict__} does not have an 'id' field")
        if feature["id"] not in df:
            raise ValueError(f"Feature {feature['id']} does not exist in the dataset")

        feature_map[feature["id"]] = feature

    return feature_map


# 1. Accept descriptions from SDK
# 2. Accept type overrides from SDK
# 3. Run df.describe() for numerical and categorical fields
#       df[df.columns].astype('category')
def init_from_pd_dataset(df, targets=None, features=None):
    typeset = ProfilingTypeSet(Settings())
    dataset_types = typeset.infer_type(df)

    feature_map = _validate_dataset_features(df, features or [])
    dataset_features = []

    # Iterate through df.columns to preserve order
    for column in df.columns.tolist():
        inferred_feature = {"id": column, "type": str(dataset_types[column])}
        # Check if feature exists in features list and merge with inferred_feature
        if column in feature_map:
            inferred_feature.update(feature_map[column])
        dataset_features.append(inferred_feature)

    shape = {
        "rows": df.shape[0],
        "columns": df.shape[1],
    }
    df_head = df.head().to_dict(orient="records")
    df_tail = df.tail().to_dict(orient="records")

    if targets:
        _validate_pd_dataset_targets(df, targets)

    return Dataset(
        fields=dataset_features,  # TODO - deprecate naming in favor of features
        sample=[
            {
                "id": "head",
                "data": df_head,
            },
            {
                "id": "tail",
                "data": df_tail,
            },
        ],
        shape=shape,
        targets=targets,
    )


def analyze_vm_dataset(dataset, vm_dataset, analyze_opts=None):
    """
    Analyzes a dataset instance and extracts different metrics from it

    :param dataset: A full input dataset. Only supports Pandas datasets at the moment.
    :param vm_dataset: VM Dataset metadata
    :param analyze_opts: Additional analyze options (not used yet)
    """
    dataset_class = dataset.__class__.__name__

    if dataset_class == "DataFrame":
        analyze_results = _analyze_pd_dataset(dataset, vm_dataset, analyze_opts)
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    return analyze_results


def init_vm_dataset(dataset, dataset_type, targets=None, features=None):
    """
    Initializes a validmind.Dataset by extracting metadata from a dataset instance
    """
    dataset_class = dataset.__class__.__name__

    if dataset_class == "DataFrame":
        vm_dataset = init_from_pd_dataset(dataset, targets, features)
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    vm_dataset.dataset_type = dataset_type

    return vm_dataset
