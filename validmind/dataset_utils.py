"""
Utilities for inspecting and extracting statistics from client datasets
"""
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

from dython.nominal import associations
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet
from sklearn.metrics import r2_score

from .dataset import Dataset

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
    elif type_ == "Categorical" or type_ == "Boolean" or type_ == "Dummy":
        return df[field].value_counts().to_dict()
    elif type_ == "Null":
        print(f"Ignoring histogram generation for null column {field}")
    else:
        raise ValueError(
            f"Unsupported field type found when computing its histogram: {type_}"
        )


def _add_field_statistics(df, field, dataset_options=None):
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
        label="Trendline",
    )
    subplot.legend()
    subplot.set_title("R2 Score: " + "{:.4f}".format(r2), fontsize=20)
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
                "type": "correlation-pearson",  # Now using dython which generates multiple correlation types
                "figure": subplot.figure,
                "key": key,
                "metadata": {"x": x, "y": y, "value": value},
            }
        )
    return plots


def get_transformed_dataset(df, vm_dataset):
    """
    Returns a transformed dataset that uses the features from vm_dataset.
    Some of the features in vm_dataset are of type Dummy so we need to
    reverse the one hot encoding and drop the individual dummy columns
    """
    # Get the list of features that are of type Dummy
    dataset_options = vm_dataset.dataset_options
    dummy_variables = (
        dataset_options.get("dummy_variables", []) if dataset_options else []
    )
    # Exclude columns that have prefixes that are in the dummy feature list
    dummy_column_names = [
        column_name
        for column_name in df.columns
        if any(
            column_name.startswith(dummy_variable) for dummy_variable in dummy_variables
        )
    ]
    transformed_df = df.drop(dummy_column_names, axis=1)

    # Add reversed dummy features to the transformed dataset
    for dummy_variable in dummy_variables:
        columns_with_dummy_prefix = [
            col for col in df.columns if col.startswith(dummy_variable)
        ]
        transformed_df[dummy_variable] = (
            df[columns_with_dummy_prefix]
            .idxmax(axis=1)
            .replace(f"{dummy_variable}[-_:]", "", regex=True)
        )

    return transformed_df


def _analyze_pd_dataset(df, vm_dataset):
    """
    Runs basic analysis tasks on a Pandas dataset:

    - Descriptive statistics
    - Pearson correlation matrix
    - Histograms for distribution of values
    """
    fields = vm_dataset.fields
    transformed_df = get_transformed_dataset(df, vm_dataset)

    # TODO - accept dataset_options to configure how to extract different metrics
    statistics = transformed_df.describe().to_dict(orient="dict")
    # Ignore fields that have very high cardinality
    fields_for_correlation = []

    for field in fields:
        field_type = field["type"]
        # Temporary hack until histograms are separated from statistics
        if field["id"] not in statistics:
            statistics[field["id"]] = {}

        statistics[field["id"]]["histogram"] = _get_histogram(
            transformed_df, field["id"], field_type
        )

        _add_field_statistics(transformed_df, field, vm_dataset.dataset_options)
        # Fields with more than 10% distinct values should not be used for correlation
        if field["statistics"]["distinct"] < 0.1:
            fields_for_correlation.append(field["id"])

    correlation_matrix = associations(
        transformed_df[fields_for_correlation], compute_only=True, plot=False
    )["corr"]

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
        transformed_df, vm_dataset, correlation_matrix, n_top=15
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
        # Skip validating this while we add full support for dummy features
        # if feature["id"] not in df:
        #     raise ValueError(f"Feature {feature['id']} does not exist in the dataset")

        feature_map[feature["id"]] = feature

    return feature_map


def infer_pd_dataset_types(df, dataset_options=None, features=None):
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
    vm_dataset_features = {}

    # Load extra feature options for features that were passed manually
    extra_feature_map = _validate_dataset_features(df, features or [])

    # Exclude dummy variables from type inference
    dummy_variables = (
        dataset_options.get("dummy_variables", []) if dataset_options else []
    )
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
    dataset_types = typeset.infer_type(df[df_columns])

    for column, type in dataset_types.items():
        if str(type) == "Unsupported":
            if df[column].isnull().all():
                vm_dataset_features[column] = {"id": column, "type": "Null"}
            else:
                raise ValueError(
                    f"Unsupported type for column {column}. Please review all values in this dataset column."
                )
        else:
            vm_dataset_features[column] = {"id": column, "type": str(type)}

    # Set dataset_types to Dummy for each dummy variable
    for dummy in dummy_variables:
        vm_dataset_features[dummy] = {"id": dummy, "type": "Dummy"}

    # Finally, add the extra feature options that were passed manually if any
    for column, feature in extra_feature_map.items():
        vm_dataset_features[column].update(feature)

    return list(vm_dataset_features.values())


# 1. Accept descriptions from SDK
# 2. Accept type overrides from SDK
# 3. Run df.describe() for numerical and categorical fields
#       df[df.columns].astype('category')
def init_from_pd_dataset(df, dataset_options=None, targets=None, features=None):
    vm_dataset_features = infer_pd_dataset_types(df, dataset_options, features)

    shape = {
        "rows": df.shape[0],
        "columns": df.shape[1],
    }
    df_head = df.head().to_dict(orient="records")
    df_tail = df.tail().to_dict(orient="records")

    if targets:
        _validate_pd_dataset_targets(df, targets)

    return Dataset(
        fields=vm_dataset_features,  # TODO - deprecate naming in favor of features
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
        dataset_options=dataset_options,
    )


def analyze_vm_dataset(dataset, vm_dataset):
    """
    Analyzes a dataset instance and extracts different metrics from it

    :param dataset: A full input dataset. Only supports Pandas datasets at the moment.
    :param vm_dataset: VM Dataset metadata
    """
    dataset_class = dataset.__class__.__name__

    if dataset_class == "DataFrame":
        analyze_results = _analyze_pd_dataset(dataset, vm_dataset)
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    return analyze_results


def init_vm_dataset(
    dataset, dataset_type, dataset_options=None, targets=None, features=None
):
    """
    Initializes a validmind.Dataset by extracting metadata from a dataset instance
    """
    dataset_class = dataset.__class__.__name__

    if dataset_class == "DataFrame":
        vm_dataset = init_from_pd_dataset(dataset, dataset_options, targets, features)
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    vm_dataset.dataset_type = dataset_type

    return vm_dataset
