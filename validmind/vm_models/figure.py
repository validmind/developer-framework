"""
Figure objects track the figure schema supported by the ValidMind API
"""

from dataclasses import dataclass
from typing import Optional


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

    def serialize(self):
        """
        Serializes the Figure to a dictionary so it can be sent to the API
        """
        return {
            "key": self.key,
            "metadata": self.metadata or {},
            "figure": self.figure,
        }
