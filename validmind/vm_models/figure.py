"""
Figure objects track the figure schema supported by the ValidMind API
"""

import json
from dataclasses import dataclass
from io import BytesIO
from typing import Optional

import base64
import matplotlib
import plotly
import plotly.graph_objs as go
import ipywidgets as widgets

from ..client_config import client_config
from ..utils import get_full_typename


@dataclass
class Figure:
    """
    Figure objects track the schema supported by the ValidMind API
    """

    key: str
    figure: object
    metadata: Optional[dict] = None
    for_object: Optional[object] = None
    extras: Optional[dict] = None

    _type: str = "plot"

    def __post_init__(self):
        """
        Set default params if not provided
        """
        if self.for_object is not None:
            metadata = self.metadata or {}
            # Use underscore to avoid name collisions with user-defined metadata
            metadata["_type"] = self._get_for_object_type()
            metadata["_name"] = (
                self.for_object.name if hasattr(self.for_object, "name") else None
            )
            self.metadata = metadata

        # Wrap around with FigureWidget so that we can display interactive Plotly
        # plots in regular Jupyter notebooks. This is not supported on Google Colab.
        if (
            not client_config.running_on_colab
            and self.figure is not None
            and isinstance(self.figure, plotly.graph_objs._figure.Figure)
        ):
            self.figure = go.FigureWidget(self.figure)

    def is_matplotlib_figure(self) -> bool:
        """
        Returns True if the figure is a matplotlib figure
        """
        return isinstance(self.figure, matplotlib.figure.Figure)

    def is_plotly_figure(self) -> bool:
        """
        Returns True if the figure is a plotly figure
        """
        return isinstance(self.figure, plotly.graph_objs._figure.Figure) or isinstance(
            self.figure, plotly.graph_objs._figurewidget.FigureWidget
        )

    def _get_for_object_type(self):
        """
        Returns the type of the object this figure is for
        """
        # Avoid circular imports
        from .metric import Metric
        from .threshold_test import ThresholdTest

        if issubclass(self.for_object.__class__, Metric):
            return "metric"
        elif issubclass(self.for_object.__class__, ThresholdTest):
            return "threshold_test"
        else:
            raise ValueError(
                "Figure for_object must be a Metric or ThresholdTest object"
            )

    def _to_widget(self):
        """
        Returns the ipywidget compatible representation of the figure. Ideally
        we would render images as-is, but Plotly FigureWidgets don't work well
        on Google Colab when they are combined with ipywidgets.
        """
        if self.is_matplotlib_figure():
            tmpfile = BytesIO()
            self.figure.savefig(tmpfile, format="png")
            encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
            return widgets.HTML(
                value=f"""
                <img style="width:100%; height: auto;" src="data:image/png;base64,{encoded}"/>
                """
            )

        elif self.is_plotly_figure():
            # FigureWidget can be displayed as-is but not on Google Colab. In this case
            # we just return the image representation of the figure.
            if client_config.running_on_colab:
                png_file = self.figure.to_image(format="png")
                encoded = base64.b64encode(png_file).decode("utf-8")
                return widgets.HTML(
                    value=f"""
                    <img style="width:100%; height: auto;" src="data:image/png;base64,{encoded}"/>
                    """
                )
            else:
                return self.figure
        else:
            raise ValueError(
                f"Figure type {type(self.figure)} not supported for plotting"
            )

    def serialize(self):
        """
        Serializes the Figure to a dictionary so it can be sent to the API
        """
        return {
            "type": self._type,
            "key": self.key,
            "metadata": json.dumps(self.metadata, allow_nan=False),
        }

    def serialize_files(self):
        """Creates a `requests`-compatible files object to be sent to the API"""
        if self.is_matplotlib_figure():
            buffer = BytesIO()
            self.figure.savefig(buffer, bbox_inches="tight")
            buffer.seek(0)
            return {"image": (f"{self.key}.png", buffer, "image/png")}

        elif self.is_plotly_figure():
            # When using plotly, we need to use we will produce two files:
            # - a JSON file that will be used to display the figure in the UI
            # - a PNG file that will be used to display the figure in documents
            return {
                "image": (
                    f"{self.key}.png",
                    self.figure.to_image(format="png"),
                    "image/png",
                ),
                "json_image": (
                    f"{self.key}.json",
                    self.figure.to_json(),
                    "application/json",
                ),
            }

        raise ValueError(f"Unrecognized figure type: {get_full_typename(self.figure)}")
