"""
Utilities for inspecting and extracting statistics from client datasets
"""

from .dataset import Dataset


def _validate_pd_dataset_targets(df, dataset_targets):
    unique_targets = df[dataset_targets.target_column].unique()
    if len(unique_targets) != len(dataset_targets.class_labels):
        raise ValueError(
            f"The number of unique values ({unique_targets}) in the target column does not match the number of unique class labels."
        )

    for target in unique_targets:
        if str(target) not in dataset_targets.class_labels:
            raise ValueError(
                f'The target column contains a value ("{target}") that is not in the list of class labels.'
            )

    return True


def init_from_pd_dataset(df, dataset_targets=None):
    fields = [{"id": field} for field in df.columns.tolist()]
    shape = {
        "rows": df.shape[0],
        "columns": df.shape[1],
    }
    df_head = df.head().to_dict(orient="records")
    df_tail = df.tail().to_dict(orient="records")

    if dataset_targets:
        _validate_pd_dataset_targets(df, dataset_targets)

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
        targets=dataset_targets,
    )


def init_vm_dataset(dataset, dataset_type, dataset_targets=None):
    """
    Initializes a validmind.Dataset by extracting metadata from a dataset instance
    """
    dataset_class = dataset.__class__.__name__

    if dataset_class == "DataFrame":
        vm_dataset = init_from_pd_dataset(dataset, dataset_targets)
    else:
        raise ValueError("Only Pandas datasets are supported at the moment.")

    vm_dataset.dataset_type = dataset_type

    return vm_dataset
