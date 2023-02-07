"""
Figure objects track the figure schema supported by the ValidMind API
"""


from dataclasses import dataclass


@dataclass
class Figure:
    """
    Figure objects track the schema supported by the ValidMind API
    """

    key: str
    metadata: dict
    figure: object

    def serialize(self):
        """
        Serializes the Figure to a dictionary so it can be sent to the API
        """
        return {
            "key": self.key,
            "metadata": self.metadata,
            "figure": self.figure,
        }
