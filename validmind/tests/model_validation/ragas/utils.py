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
    stored in a column. Also supports

    Args:
        df (pd.DataFrame): The DataFrame to rename columns in.
        column_map (dict): A dictionary mapping where the keys are the new column names
        that ragas expects and the values are one of the following:
            - The column name in the input dataframe
            - A string in the format "root_col.sub_col" to get a sub-column from a dictionary
            stored in a column.
            - A function that takes the value of the column and returns the value to be
            stored in the new column.

    Returns:
        pd.DataFrame: The DataFrame with columns renamed.
    """
    new_df = df.copy()

    for col_in_df, new_name in column_map.items():
        if callable(new_name):
            try:
                new_df[new_name] = new_df[col_in_df].apply(new_name)
            except Exception as e:
                raise ValueError(
                    f"Error applying function to column '{col_in_df}': {str(e)}"
                )

        elif "." in col_in_df:
            root_col, sub_col = col_in_df.split(".")

            if root_col in new_df.columns:
                new_df[new_name] = new_df[root_col].apply(
                    lambda x: _udf_get_sub_col(x, root_col, sub_col)
                )

            else:
                raise KeyError(f"Column '{root_col}' not found in DataFrame.")

        else:
            new_df.rename(columns={col_in_df: new_name}, inplace=True)

    return new_df
