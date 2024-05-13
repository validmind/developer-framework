# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


def _udf_get_sub_col(x, root_col, sub_col):
    if not isinstance(x, dict):
        raise TypeError(f"Expected a dictionary in column '{root_col}', got {type(x)}.")

    if sub_col not in x:
        raise KeyError(
            f"Sub-column '{sub_col}' not found in dictionary in column '{root_col}'."
        )

    return x[sub_col]


def get_renamed_columns(df, column_map):
    """Get a new df with columns renamed according to the column_map

    Supports sub-column notation for getting values out of dictionaries that may be
    stored in a column.

    Args:
        df (pd.DataFrame): The DataFrame to rename columns in.
        column_map (dict): A dictionary mapping old column names to new column names.

    Returns:
        pd.DataFrame: The DataFrame with columns renamed.
    """
    new_df = df.copy()

    for col_key, col_name in column_map.items():
        if "." in col_name:
            root_col, sub_col = col_name.split(".")
            if root_col in new_df.columns:
                new_df[col_key] = new_df[root_col].apply(
                    lambda x: _udf_get_sub_col(x, root_col, sub_col)
                )

            else:
                raise KeyError(f"Column '{root_col}' not found in DataFrame.")

        else:
            new_df.rename(columns={col_key: col_name}, inplace=True)

    return new_df
