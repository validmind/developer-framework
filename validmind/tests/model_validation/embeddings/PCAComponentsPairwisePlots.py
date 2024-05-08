import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import itertools


def PCAComponentsPairwisePlots(dataset, model, n_components=3):
    """
    Plots individual scatter plots for pairwise combinations of PCA components of embeddings.

    Args:
        dataset (pd.DataFrame): DataFrame containing the embeddings.
        model (model object): Model object with an 'input_id' attribute.
        n_components (int): Number of principal components to calculate.
        title (str): Title of the plot.

    Returns:
        tuple: A tuple of Plotly figure objects, each showing a scatter plot of two PCA components.
    """
    # Get embeddings from the dataset using the model
    embeddings = np.stack(dataset.y_pred(model))

    # Standardize the embeddings
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)

    # Perform PCA
    pca = PCA(n_components=n_components)
    pca_results = pca.fit_transform(embeddings_scaled)

    # Prepare DataFrame for Plotly
    pca_df = pd.DataFrame(
        pca_results, columns=[f"PC{i+1}" for i in range(n_components)]
    )

    # List to store each plot
    plots = []

    # Create plots for each pair of principal components
    for pc1, pc2 in itertools.combinations(range(1, n_components + 1), 2):
        fig = px.scatter(
            pca_df,
            x=f"PC{pc1}",
            y=f"PC{pc2}",
            title=f"{getattr(model, 'input_id', 'Unknown Model')} (PC{pc1} vs PC{pc2})",
            labels={
                f"PC{pc1}": f"Principal Component {pc1}",
                f"PC{pc2}": f"Principal Component {pc2}",
            },
        )
        plots.append(fig)

    # Return the list of plots as a tuple
    return tuple(plots)
