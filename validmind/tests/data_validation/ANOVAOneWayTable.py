# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

import pandas as pd
from scipy.stats import f_oneway

from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


@dataclass
class ANOVAOneWayTable(Metric):
    """
    **Purpose**: The ANOVA (Analysis of Variance) One Way Table metric is used to evaluate whether the mean of
    numerical variables differs across different groups identified by the target or categorical variables. It plays a
    key role in identifying whether categorical variables have a significant effect on the numerical variables of
    interest. This metric helps in understanding and detecting features that are statistically significant with regard
    to the target variable in a given dataset.

    **Test Mechanism**: This metric performs an ANOVA F-test on each of the numerical variables against the target.
    Should no specific features be indicated, the test is conducted on all numerical features. A p-value is generated
    for each test and compared against a specified threshold, defaulting to 0.05 if none is given. The feature is
    marked as 'Pass' if the p-value is less than or equal to the specified threshold, indicating that there is a
    significant difference in the means of the groups, and 'Fail' otherwise. The test results are returned in a
    DataFrame indicating the variable name, F statistic value, p-value, threshold, and pass/fail status for each
    numerical variable.

    **Signs of High Risk**: High risk or failure in the model may be indicated by a large number of 'Fail' results in
    the ANOVA F-test. This suggests that many numerical variables in the dataset display no statistically significant
    difference across the target variable groups, potentially leading to underperforming predictions. Additionally,
    features with high p-values also indicate a high risk as they display a larger chance of obtaining the observed
    data given that the null hypothesis is true.

    **Strengths**:
    - The ANOVA One Way Table is an efficient tool in identifying statistically significant features as it compares the
    means of multiple groups simultaneously.
    - This metric is flexible and can handle situations where numerical features have not been specified by testing all
    numerical features in the dataset.
    - It provides a convenient way to measure the statistical significance of numerical variables and assists in
    picking those variables that significantly influence the classifier's predictions.

    **Limitations**:
    - The ANOVA One Way Table metric assumes that the data is normally distributed, which might not be the case,
    potentially leading to inaccurate test results.
    - The F-test is sensitive to variance changes, and therefore, this metric might not perform well in datasets with
    high variance.
    - The ANOVA One Way test does not indicate which specific group means are statistically different from each other;
    it merely tells that there is a difference.
    - The metric does not provide insight into interactions between variables, and it might fail to detect significant
    effects due to these interactions.
    """

    name = "anova_one_way_table"
    required_inputs = ["dataset"]
    default_params = {"features": None, "p_threshold": 0.05}
    metadata = {
        "task_types": ["classification"],
        "tags": [
            "tabular_data",
            "statistical_test",
            "multiclass_classification",
            "binary_classification",
            "numerical_data",
        ],
    }

    def run(self):
        features = self.params["features"]
        p_threshold = self.params["p_threshold"]

        # Select all numerical features if none are specified
        if features is None:
            features = self.dataset.get_numeric_features_columns()

        anova_results = self.anova_numerical_features(features, p_threshold)

        return self.cache_results(
            {
                "anova_results": anova_results.to_dict(orient="records"),
            }
        )

    def anova_numerical_features(self, features, p_threshold):
        target_column = self.dataset.target_column
        df = self.dataset.df

        # Ensure the columns exist in the dataframe
        for var in features:
            if var not in df.columns:
                raise ValueError(f"The column '{var}' does not exist in the dataframe.")
        if target_column not in df.columns:
            raise ValueError(
                f"The target column '{target_column}' does not exist in the dataframe."
            )

        # Ensure the target variable is not included in num_vars
        if target_column in features:
            features.remove(target_column)

        results = []

        for var in features:
            # Perform the ANOVA test
            class_0 = df[df[target_column] == 0][var]
            class_1 = df[df[target_column] == 1][var]

            f, p = f_oneway(class_0, class_1)

            # Add the result to the list of results
            results.append(
                [var, f, p, p_threshold, "Pass" if p <= p_threshold else "Fail"]
            )

        # Convert results to a DataFrame and return
        results_df = pd.DataFrame(
            results,
            columns=["Variable", "F statistic", "p-value", "Threshold", "Pass/Fail"],
        )

        # Sort by p-value in ascending order
        results_df = results_df.sort_values(by="p-value")

        return results_df

    def summary(self, metric_value):
        anova_results_table = metric_value["anova_results"]
        return ResultSummary(
            results=[
                ResultTable(
                    data=anova_results_table,
                    metadata=ResultTableMetadata(
                        title="ANOVA F-Test Results for Numerical Features"
                    ),
                )
            ]
        )
