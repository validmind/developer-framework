# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from validmind.vm_models import Metric


@dataclass
class DatasetCorrelations(Metric):
    """
    **Purpose**: The DatasetCorrelations metric is employed to examine the relationship between variables in a dataset,
    specifically designed for numerical and categorical data types. Using Pearson's R, Cramer's V, and Correlation
    ratios, it helps in understanding the linear relationship between numerical variables, association between
    categorical ones, and between numerical-categorical variables respectively. This allows for better awareness
    regarding dependency between features, which is crucial for optimizing model performance and understanding the
    model's behavior and predictors.

    **Test Mechanism**: During its execution, DatasetCorrelations initiates the calculation of the aforementioned
    correlation coefficients for the provided dataset. It leverages the built-in method 'get_correlations()',
    populating the 'correlations' attribute in the dataset object. It then invokes 'get_correlation_plots()' to
    generate graphical representations of these correlations. Finally, the correlation details and figures are cached
    for further study and analysis. The test does not dictate specific thresholds or grading scales.

    **Signs of High Risk**: Signs of high risk might involve the presence of high correlation levels between input
    variables (multicollinearity), which can jeopardize the interpretability of the model and lead to overfitting.
    Additionally, the absence of any significant correlations, which suggests that the variables might not have
    predictive power.

    **Strengths**: The test boasts the advantage of being comprehensive; it covers the correlation study of numerical,
    categorical, and numerical-categorical variables. Thus, it negates the need for multiple individual tests.
    Furthermore, it not only provides numerical correlation values, but also visualization plots, aiding in a more
    intuitive understanding of relationships between variables.

    **Limitations**: This metric, however, is limited by the fact that it only detects linear relationships and
    associations; nonlinear relationships may go unnoticed. Also, given the absence of specified thresholds for
    determining correlation significance, the interpretation of the results is dependent on the user's expertise.
    Lastly, it doesn't handle missing values in the dataset, which need to be treated beforehand.
    """

    name = "dataset_correlations"
    required_inputs = ["dataset"]
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "time_series_data", "correlation"],
    }

    # TODO: allow more metric metadata to be set, not just scope
    def __post_init__(self):
        self.scope = self.dataset.type

    def run(self):
        # This will populate the "correlations" attribute in the dataset object
        self.dataset.get_correlations()
        correlation_plots = self.dataset.get_correlation_plots()
        return self.cache_results(self.dataset.correlations, figures=correlation_plots)
