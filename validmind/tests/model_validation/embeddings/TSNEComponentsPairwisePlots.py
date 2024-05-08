import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import itertools


def TSNEComponentsPairwisePlots(
    dataset,
    model,
    n_components=2,
    perplexity=30,
    title="t-SNE",
):
    """
    Plots individual scatter plots for pairwise combinations of t-SNE components of embeddings.

    Args:
        dataset (pd.DataFrame): DataFrame containing the embeddings.
        model (model object): Model object with an 'input_id' attribute.
        n_components (int): Number of t-SNE components to calculate.
        perplexity (int): Perplexity parameter for the t-SNE algorithm.
        title (str): Title of the plot.

    Returns:
        tuple: A tuple of Plotly figure objects, each showing a scatter plot of two t-SNE components.
    """
    # Get embeddings from the dataset using the model
    embeddings = np.stack(dataset.y_pred(model))

    # Standardize the embeddings
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)

    # Perform t-SNE
    tsne = TSNE(n_components=n_components, perplexity=perplexity)
    tsne_results = tsne.fit_transform(embeddings_scaled)

    # Prepare DataFrame for Plotly
    tsne_df = pd.DataFrame(
        tsne_results, columns=[f"Component {i+1}" for i in range(n_components)]
    )

    # List to store each plot
    plots = []

    # Create plots for each pair of t-SNE components (if n_components > 1)
    if n_components > 1:
        for comp1, comp2 in itertools.combinations(range(1, n_components + 1), 2):
            fig = px.scatter(
                tsne_df,
                x=f"Component {comp1}",
                y=f"Component {comp2}",
                title=f"{title} - {getattr(model, 'input_id', 'Unknown Model')}",
                labels={
                    f"Component {comp1}": f"Component {comp1}",
                    f"Component {comp2}": f"Component {comp2}",
                },
            )
            plots.append(fig)
    else:
        fig = px.scatter(
            tsne_df,
            x=f"Component 1",
            y=f"Component 1",
            title=f"{title} - {getattr(model, 'input_id', 'Unknown Model')}",
            labels={
                "Component 1": "Component 1",
            },
        )
        plots.append(fig)

    # Return the list of plots as a tuple
    return tuple(plots)
