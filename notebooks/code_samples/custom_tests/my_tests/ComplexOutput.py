# Saved from __main__.complex_output
# Test ID: my_custom_metrics.ComplexOutput

import numpy as np
import plotly_express as px


def ComplexOutput():
    """This metric demonstrates how to return many tables and figures in a single metric"""
    # create a couple tables
    table = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
    table2 = [{"C": 5, "D": 6}, {"C": 7, "D": 8}]

    # create a few figures showing some random data
    fig1 = px.line(x=np.arange(10), y=np.random.rand(10), title="Random Line Plot")
    fig2 = px.bar(x=["A", "B", "C"], y=np.random.rand(3), title="Random Bar Plot")
    fig3 = px.scatter(
        x=np.random.rand(10), y=np.random.rand(10), title="Random Scatter Plot"
    )

    return (
        {
            "My Cool Table": table,
            "Another Table": table2,
        },
        fig1,
        fig2,
        fig3,
    )
