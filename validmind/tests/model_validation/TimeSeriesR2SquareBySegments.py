# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import pandas as pd
import plotly.express as px
from sklearn import metrics

from validmind import tags, tasks


@tags("model_performance", "sklearn")
@tasks("regression", "time_series_forecasting")
def TimeSeriesR2SquareBySegments(datasets, models, segments=None):
    """
    Plot R-Squared values for each model over specified time segments and generate a bar chart
    with the results.

    **Purpose**: The purpose of this function is to plot the R-Squared values for different models applied to various segments of the time series data.

    **Parameters**:
    - datasets: List of datasets to evaluate.
    - models: List of models to evaluate.
    - segments: Dictionary with 'start_date' and 'end_date' keys containing lists of start and end dates for each segments. If None, the time series will be segmented into two halves.

    **Test Mechanism**: The function iterates through each dataset-model pair, calculates the R-Squared values for specified time segments, and generates a bar chart with these results.

    **Signs of High Risk**:
    - If the R-Squared values are significantly low for certain segments, it could indicate that the model is not explaining much of the variability in the dataset for those segments.

    **Strengths**:
    - Provides a visual representation of model performance across different time segments.
    - Allows for identification of segments where models perform poorly.

    **Limitations**:
    - Assumes that the dataset is provided as a DataFrameDataset object with `y`, `y_pred`, and `feature_columns` attributes.
    - Requires that `dataset.y_pred(model)` returns the predicted values for the model.
    - Assumes that `y_true` and `y_pred` are pandas Series with datetime indices.
    """
    results_list = []

    for dataset, model in zip(datasets, models):
        dataset_name = dataset.input_id
        model_name = model.input_id

        y_true = dataset.y
        y_pred = dataset.y_pred(model)

        # Ensure y_true and y_pred are pandas Series with the same index
        if not isinstance(y_true, pd.Series):
            y_true = pd.Series(y_true, index=dataset.df.index)
        if not isinstance(y_pred, pd.Series):
            y_pred = pd.Series(y_pred, index=dataset.df.index)

        index = dataset.df.index

        if segments is None:
            mid_point = len(index) // 2
            segments = {
                "start_date": [index.min(), index[mid_point]],
                "end_date": [index[mid_point - 1], index.max()],
            }

        for segment_index, (start_date, end_date) in enumerate(
            zip(segments["start_date"], segments["end_date"])
        ):
            mask = (index >= start_date) & (index <= end_date)
            y_true_segment = y_true.loc[mask]
            y_pred_segment = y_pred.loc[mask]

            if len(y_true_segment) > 0 and len(y_pred_segment) > 0:
                r2s = metrics.r2_score(y_true_segment, y_pred_segment)
                results_list.append(
                    {
                        "Model": model_name,
                        "Dataset": dataset_name,
                        "Segments": f"Segment {segment_index + 1}",
                        "Start Date": start_date,
                        "End Date": end_date,
                        "R-Squared": r2s,
                    }
                )

    # Convert results list to a DataFrame
    results_df = pd.DataFrame(results_list)

    # Plotting
    fig = px.bar(
        results_df,
        x="Segments",
        y="R-Squared",
        color="Model",
        barmode="group",
        title="R-Squared Comparison by Segment and Model",
        labels={
            "R-Squared": "R-Squared Value",
            "Segment": "Time Segment",
            "Model": "Model",
        },
    )

    return fig, results_df
