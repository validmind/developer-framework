"""
Utilities for manipulating VMDataset objects
"""

import numpy as np
from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet

from .figure import Figure
from .plot_utils import get_plot_for_feature_pair

DEFAULT_HISTOGRAM_BINS = 10
DEFAULT_HISTOGRAM_BIN_SIZES = [5, 10, 20, 50]


def get_x_and_y(df, target_column):
    """
    Get the X and Y dataframes from the input dataset.
    """
    x = df.drop(target_column, axis=1)
    y = df[target_column]
    return x, y


def parse_dataset_variables(df, options=None):
    """
    Infers the data types for each column using pandas_profiling's
    typeset from visions library.

    If dummy variables were specified with dataset_options, we will
    not inter the types for these columns since they need to be described
    as a group of columns (e.g. dummy_a, dummy_b, dummy_c, etc.)

    When a type is inferred as Unsupported we check if it's a null column
    and mark it appropriately.
    """
    df_columns = df.columns
    vm_dataset_variables = {}

    # Exclude dummy variables from type inference
    dummy_variables = options.get("dummy_variables", []) if options else []
    # Check for each df column if any of the dummy variables is a prefix of it
    df_columns = [
        column
        for column in df_columns
        if not any(column.startswith(dummy) for dummy in dummy_variables)
    ]

    if len(dummy_variables) > 0:
        print(
            f"Excluding the following dummy variables from type inference: {dummy_variables}"
        )

    typeset = ProfilingTypeSet(Settings())
    variable_types = typeset.infer_type(df[df_columns])

    for column, type in variable_types.items():
        if str(type) == "Unsupported":
            if df[column].isnull().all():
                vm_dataset_variables[column] = {"id": column, "type": "Null"}
            else:
                raise ValueError(
                    f"Unsupported type for column {column}. Please review all values in this dataset column."
                )
        else:
            vm_dataset_variables[column] = {"id": column, "type": str(type)}

    # Set variable_types to Dummy for each dummy variable
    for dummy in dummy_variables:
        vm_dataset_variables[dummy] = {"id": dummy, "type": "Dummy"}

    return list(vm_dataset_variables.values())


def validate_pd_dataset_targets(df, targets):
    if targets.class_labels is None:
        return True

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


def describe_dataset_field(df, field):
    """
    Gets descriptive statistics for a single field in a Pandas DataFrame.
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
        field["statistics"] = (
            df[field["id"]].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95]).to_dict()
        )
    elif field_type == "Categorical" or field_type == "Dummy":
        field["statistics"] = df[field["id"]].astype("category").describe().to_dict()

    # Initialize statistics object for non-numeric or categorical fields
    if "statistics" not in field:
        field["statistics"] = {}

    field["statistics"]["n_missing"] = df[field["id"]].isna().sum()
    field["statistics"]["missing"] = field["statistics"]["n_missing"] / len(
        df[field["id"]]
    )
    field["statistics"]["n_distinct"] = df[field["id"]].nunique()
    field["statistics"]["distinct"] = field["statistics"]["n_distinct"] / len(
        df[field["id"]]
    )

    field["histograms"] = get_field_histograms(df, field["id"], field_type)


def get_field_histograms(df, field, type_):
    """
    Returns a collection of histograms for a numerical or categorical field.
    We store different combinations of bin sizes to allow analyzing the data better

    Will be used in favor of _get_histogram in the future
    """
    # Set the minimum number of bins to nunique if it's less than the default
    if type_ == "Numeric":
        return get_numerical_histograms(df, field)
    elif type_ == "Categorical" or type_ == "Boolean" or type_ == "Dummy":
        value_counts = df[field].value_counts()
        return {
            "default": {
                "bin_size": len(value_counts),
                "histogram": value_counts.to_dict(),
            }
        }
    elif type_ == "Null":
        print(f"Ignoring histogram generation for null column {field}")
    else:
        raise ValueError(
            f"Unsupported field type found when computing its histogram: {type_}"
        )


def get_numerical_histograms(df, field):
    """
    Returns a collection of histograms for a numerical field, each one
    with a different bin size
    """
    values = df[field].to_numpy()
    values_cleaned = values[~np.isnan(values)]

    # bins='sturges'. Cannot use 'auto' until we review and fix its performance
    #  on datasets with too many unique values
    #
    # 'sturges': R’s default method, only accounts for data size. Only optimal
    # for gaussian data and underestimates number of bins for large non-gaussian datasets.
    default_hist = np.histogram(values_cleaned, bins="sturges")

    histograms = {
        "default": {
            "bin_size": len(default_hist[0]),
            "histogram": {
                "bin_edges": default_hist[1].tolist(),
                "counts": default_hist[0].tolist(),
            },
        }
    }

    for bin_size in DEFAULT_HISTOGRAM_BIN_SIZES:
        hist = np.histogram(values_cleaned, bins=bin_size)
        histograms[f"bins_{bin_size}"] = {
            "bin_size": bin_size,
            "histogram": {
                "bin_edges": hist[1].tolist(),
                "counts": hist[0].tolist(),
            },
        }

    return histograms


def generate_correlation_plots(vm_dataset, n_top=15):
    corr_matrix_abs_us = vm_dataset.correlation_matrix.unstack()
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
        subplot = get_plot_for_feature_pair(vm_dataset, x, y)
        plots.append(
            Figure(
                figure=subplot.figure,
                key=key,
                metadata={"x": x, "y": y, "value": value},
                extras={
                    "type": "correlation-pearson"
                },  # Now using dython which generates multiple correlation types
            )
        )
    return plots
