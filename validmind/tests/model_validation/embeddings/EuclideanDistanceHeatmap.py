import numpy as np
import plotly.express as px
from sklearn.metrics.pairwise import euclidean_distances


def EuclideanDistanceHeatmap(
    dataset,
    model,
    title="Euclidean Distance Matrix",
    color="Euclidean Distance",
    xaxis_title="Index",
    yaxis_title="Index",
    color_scale="Blues",
):
    """
    Plots an interactive heatmap of Euclidean distances for embeddings stored in a DataFrame.

    Args:
        dataset (pd.DataFrame): DataFrame containing the embeddings.
        embedding_column (str): Column name where embeddings are stored as lists or arrays.
        title (str): Title of the heatmap.
        xaxis_title (str): Title for the X-axis.
        yaxis_title (str): Title for the Y-axis.
        color_scale (str): Color scale for the heatmap.
        rows_to_use (list[int]): List of indices specifying which rows to use for computation.

    Returns:
        None: Displays an interactive heatmap.
    """
    embeddings = np.stack(dataset.y_pred(model))

    # Calculate pairwise Euclidean distance
    distance_matrix = euclidean_distances(embeddings)

    # Create labels for axes
    indices = [f"{xaxis_title} {i+1}" for i in range(len(dataset.df))]

    # Create the heatmap using Plotly
    fig = px.imshow(
        distance_matrix,
        labels=dict(x=xaxis_title, y=yaxis_title, color=color),
        x=indices,
        y=indices,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=color_scale,
    )

    fig.update_layout(
        title=f"{title} - {model.input_id}",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
    )

    return fig