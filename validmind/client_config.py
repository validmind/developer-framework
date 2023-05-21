"""
Central class to track configuration of the developer framework
client against the ValidMind API
"""

from dataclasses import dataclass


@dataclass
class ClientConfig:
    """
    Configuration class for the ValidMind API client. This is instantiated
    when initializing the API client.
    """

    project: object
    feature_flags: dict
    template: object

    def is_json_plots_enabled(self):
        """
        Returns True if the JSON plots feature flag is enabled on the backend
        """
        return self.feature_flags.get("generate_json_plots", False)


client_config = ClientConfig(project=None, feature_flags={}, template=None)
