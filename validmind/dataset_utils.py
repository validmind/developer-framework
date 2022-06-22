"""
Utilities for inspecting and extracting statistics from client datasets
"""
import numpy as np
from pandas_profiling.config import Settings
from pandas_profiling.model.typeset import ProfilingTypeSet


from .dataset import Dataset

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


def _analyze_pd_dataset(df, fields, analyze_opts=None):
    """
    Runs basic analysis tasks on a Pandas dataset:

    - Descriptive statistics
    - Pearson correlation matrix
    - Histograms for distribution of values
    """
    # TODO - accept analyze_opts to configure how to extract different metrics
    statistics = df.describe().to_dict(orient="dict")
    # TODO - fix statistics to be consistent since it doesn't operate on categorical fields
    rows = df.shape[0]

    for field in fields:
        field_type = field["type"]
        # Temporary hack until histograms are separated from statistics
        if field["id"] not in statistics:
            statistics[field["id"]] = {}

        statistics[field["id"]]["histogram"] = _get_histogram(
            df, field["id"], field_type
        )

        statistics[field["id"]]["count"] = rows
        statistics[field["id"]]["n_missing"] = df[field["id"]].isna().sum()
        statistics[field["id"]]["missing"] = statistics[field["id"]]["n_missing"] / len(
            df[field["id"]]
        )

    correlation_matrix = df.corr().to_dict(orient="records")
    # Transform to the current format expected by the UI
    correlations = [
        [
            {
                "field": key,
                "value": value,
            }
            for key, value in correlation_row.items()
        ]
        for correlation_row in correlation_matrix
    ]

    return {
        "correlations": {
            "pearson": correlations,
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


def init_from_pd_dataset(df, targets=None):
    typeset = ProfilingTypeSet(Settings())
    dataset_types = typeset.infer_type(df)

    fields = [
        {"id": field, "type": str(dataset_types[field])}
        for field in df.columns.tolist()
    ]
    shape = {
        "rows": df.shape[0],
        "columns": df.shape[1],
    }
    df_head = df.head().to_dict(orient="records")
    df_tail = df.tail().to_dict(orient="records")

    if targets:
        _validate_pd_dataset_targets(df, targets)

    return Dataset(
        fields=fields,
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


def analyze_vm_dataset(dataset, fields, analyze_opts=None):
    """
    Analyzes a dataset instance and extracts different metrics from it
    """
    dataset_class = dataset.__class__.__name__

    if dataset_class == "DataFrame":
        analyze_results = _analyze_pd_dataset(dataset, fields, analyze_opts)
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    return analyze_results


def init_vm_dataset(dataset, dataset_type, targets=None):
    """
    Initializes a validmind.Dataset by extracting metadata from a dataset instance
    """
    dataset_class = dataset.__class__.__name__

    if dataset_class == "DataFrame":
        vm_dataset = init_from_pd_dataset(dataset, targets)
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    vm_dataset.dataset_type = dataset_type

    return vm_dataset
