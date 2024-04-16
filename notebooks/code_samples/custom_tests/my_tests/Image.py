# Saved from __main__.image
# Test ID: my_custom_metrics.Image

import io
import matplotlib.pyplot as plt


def Image():
    """This metric demonstrates how to return an image in a metric"""

    # create a simple plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4])
    ax.set_title("Simple Line Plot")

    # save the plot as a PNG image (in-memory buffer)
    img_data = io.BytesIO()
    fig.savefig(img_data, format="png")
    img_data.seek(0)

    plt.close()  # close the plot to avoid displaying it

    return img_data.read()
