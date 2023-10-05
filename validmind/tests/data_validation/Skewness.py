# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass
from typing import List

from ydata_profiling.config import Settings
from ydata_profiling.model.typeset import ProfilingTypeSet

from validmind.vm_models import (
    ResultSummary,
    ResultTable,
    ResultTableMetadata,
    ThresholdTest,
    ThresholdTestResult,
)


@dataclass
class Skewness(ThresholdTest):
    """
    **Purpose**: The Skewness test is designed to measure the degree to which a given distribution deviates from a
    normal distribution, indicating any asymmetry in the predictive model's data. The skewness metric can be positive
    (indicating a distribution with a long tail to the right) or negative (signifying a tail to the left). As
    consistency and correct data distribution is paramount to good model performance, understanding skewness can assist
    in identifying data quality issues, making it integral for data profiling in both classic classification and
    regression machine learning models.

    **Test Mechanism**: The test is performed by calculating the skewness of numerical columns in the dataset. The
    skewness is obtained from the DataFrame of the dataset, constrained to numerical data types. An absolute value for
    the skewness is compared against a maximum threshold (default value of 1). If the calculated value is less than
    this maximum threshold, the test is marked 'Pass'; otherwise, it's considered 'Fail'. The results are then cached,
    with the list of result classes for each column indicating the column name, the passed status, and its skewness
    value compliance.

    **Signs of High Risk**: Indicators of high risk or potential model performance issues associated with this test
    include high skewness levels that greatly exceed the max_threshold in a negative or positive direction,
    representing skewed distribution in data. If data appears consistently skewed, it can show that the underlying
    assumptions of the Machine Learning model may not apply, and can lead to poor model performance, wrong predictions,
    or biased inferences.

    **Strengths**: The skewness test allows for rapid identification of unequal data distributions, which may go
    unnoticed but may considerably affect the performance of a machine learning model. The test is flexible and can be
    adapted according to the users' needs, adjusting the maximum threshold parameter.

    **Limitations**: The test only runs on numeric columns, which means that data in non-numeric columns could still
    hold bias or problematic skewness not captured by this test. Secondly, it assumes data to follow a normal
    distribution, which might not always be a realistic expectation in real-world data. Finally, by relying heavily on
    a manually set threshold, the risk grading might be either too strict or too lenient depending on the chosen
    threshold, something that might require expertise and iterations to perfect.
    """

    category = "data_quality"
    name = "skewness"
    required_inputs = ["dataset"]
    default_params = {"max_threshold": 1}
    metadata = {
        "task_types": ["classification", "regression"],
        "tags": ["tabular_data", "data_quality"],
    }

    def summary(self, results: List[ThresholdTestResult], all_passed: bool):
        """
        The skewness test returns results like these:
        [{"values": {"skewness": 1.0}, "column": "NumOfProducts", "passed": false}]
        """
        results_table = [
            {
                "Column": result.column,
                "Skewness": result.values["skewness"],
                "Pass/Fail": "Pass" if result.passed else "Fail",
            }
            for result in results
        ]
        return ResultSummary(
            results=[
                ResultTable(
                    data=results_table,
                    metadata=ResultTableMetadata(title="Skewness Results for Dataset"),
                )
            ]
        )

    def run(self):
        typeset = ProfilingTypeSet(Settings())
        dataset_types = typeset.infer_type(self.dataset.df)

        skewness = self.dataset.df.skew(numeric_only=True)
        passed = all(abs(skewness) < self.params["max_threshold"])
        results = []

        for col in skewness.index:
            # Only calculate skewness for numerical columns
            if str(dataset_types[col]) != "Numeric":
                continue

            col_skewness = skewness[col]
            results.append(
                ThresholdTestResult(
                    column=col,
                    passed=abs(col_skewness) < self.params["max_threshold"],
                    values={
                        "skewness": col_skewness,
                    },
                )
            )

        return self.cache_results(results, passed=passed)
