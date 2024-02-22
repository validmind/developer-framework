# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

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
    documentation_template: object
    running_on_colab: bool = False

    def __post_init__(self):
        """
        Set additional attributes when initializing the class
        """
        # check if running on notebook and set running_on_colab
        try:
            from google.colab import drive  # noqa

            self.running_on_colab = True
        except ImportError:
            self.running_on_colab = False

    def is_json_plots_enabled(self):
        """
        Returns True if the JSON plots feature flag is enabled on the backend
        """
        return self.feature_flags.get("generate_json_plots", False)

    def can_log_figures(self):
        """Returns True if the client can log figures to the API"""
        return self.feature_flags.get("log_figures", False)

    def can_log_output_template(self):
        """Returns True if the client can log output templates to the API"""
        return self.feature_flags.get("output_templates", False)


client_config = ClientConfig(
    project=None, feature_flags={}, documentation_template=None
)
