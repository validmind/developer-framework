# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial


import matplotlib.pyplot as plt
from sklearn import metrics
import pandas as pd
import plotly.express as px


def TimeseriesGroupbyPlot(dataset, model, date_column, groupby_column, y_column):
    """
    Timeseries Plot
    """
    df = dataset.df.copy()

    # Convert dates to datetime format
    df[date_column] = pd.to_datetime(df[date_column])

    # Sort dataframe by 'cust_ipid_nm' and 'bal_date'
    operational_deposit_df = df.groupby([groupby_column, date_column]).mean().reset_index()


    # Create the line plot
    fig = px.line(operational_deposit_df, x=date_column, y=y_column, color=groupby_column, markers=True,
                title=f"Time Series Line Plot of {y_column}",
                labels={date_column: date_column, y_column: y_column})


    return fig  # return the figure object itself
