# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from validmind.vm_models import Metric


@dataclass
class DatasetCorrelations(Metric):
    """
    Extracts the correlation matrix for a dataset. The following coefficients
    are calculated:
    - Pearson's R for numerical variables
    - Cramer's V for categorical variables
    - Correlation ratios for categorical-numerical variables
    """

    name = "dataset_correlations"
    required_context = ["dataset"]

    # TODO: allow more metric metadata to be set, not just scope
    def __post_init__(self):
        self.scope = self.dataset.type

    def run(self):
        # This will populate the "correlations" attribute in the dataset object
        self.dataset.get_correlations()
        correlation_plots = self.dataset.get_correlation_plots()
        return self.cache_results(self.dataset.correlations, figures=correlation_plots)
