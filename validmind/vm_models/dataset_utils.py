# Copyright © 2023 ValidMind Inc. All rights reserved.

"""
Utilities for manipulating VMDataset objects
"""

from ydata_profiling.config import Settings
from ydata_profiling.model.typeset import ProfilingTypeSet

from ..errors import UnsupportedColumnTypeError
from ..logging import get_logger

logger = get_logger(__name__)


def parse_dataset_variables(df, options=None):
    """
    Infers the data types for each column using ydata_profiling's
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
        logger.info(
            f"Excluding the following dummy variables from type inference: {dummy_variables}"
        )

    typeset = ProfilingTypeSet(Settings())
    variable_types = typeset.infer_type(df[df_columns])

    for column, type in variable_types.items():
        if str(type) == "Unsupported":
            if df[column].isnull().all():
                vm_dataset_variables[column] = {"id": column, "type": "Null"}
            else:
                raise UnsupportedColumnTypeError(
                    f"Unsupported type for column {column}. Please review all values in this dataset column."
                )
        else:
            vm_dataset_variables[column] = {"id": column, "type": str(type)}

    # Set variable_types to Dummy for each dummy variable
    for dummy in dummy_variables:
        vm_dataset_variables[dummy] = {"id": dummy, "type": "Dummy"}

    return list(vm_dataset_variables.values())
