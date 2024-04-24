# Saved from __main__.parameter_example
# Original Test ID: my_custom_metrics.ParameterExample
# New Test ID: <test_provider_namespace>.ParameterExample

import plotly_express as px


def ParameterExample(
    plot_title="Default Plot Title", x_col="sepal_width", y_col="sepal_length"
):
    """This metric takes two parameters and creates a scatter plot based on them.

    The purpose of this metric is to demonstrate how to create a metric that takes
    parameters and uses them to generate a plot. This can be useful for creating
    metrics that are more flexible and can be used in a variety of scenarios.
    """
    # return px.scatter(px.data.iris(), x=x_col, y=y_col, color="species")
    return px.scatter(
        px.data.iris(), x=x_col, y=y_col, color="species", title=plot_title
    )
