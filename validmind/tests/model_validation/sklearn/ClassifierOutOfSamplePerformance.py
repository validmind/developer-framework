# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance


@dataclass
class ClassifierOutOfSamplePerformance(ClassifierPerformance):
    """
    Assesses ML model's performance on out-of-sample data to measure generalization and guard against overfitting.

    **Purpose**: This test is designed to assess the performance of a Machine Learning model on out-of-sample data,
    specifically data not utilized during the training phase. The performance metrics used in the test (accuracy,
    precision, recall, and F1 score) serve to measure the model's generalization capability towards unseen data. The
    primary goal is to ensure that the model has not overfitted to the training data and retains the ability to make
    accurate predictions on novel data.

    **Test Mechanism**: The mechanism for this test involves applying the performance metrics to the predictions made
    by the model on the test dataset. These are then compared with the actual outcomes. It is assumed that the test
    dataset remains unutilized during the model training phase, therefore providing an unbiased and fair evaluation of
    the model's generalization capabilities. The various metrics used include:
    - Accuracy: The ratio of correct predictions
    - Precision: The ratio of correct positive predictions
    - Recall: The ratio of actual positives that were correctly predicted
    - F1 Score: Harmonic mean of precision and recall, effectively balancing both.

    **Signs of High Risk**:
    - Low accuracy rate.
    - Low precision and recall rates.
    - Low F1 score.
    - Significant discrepancies between the model's performance on training data and testing data, indicating
    overfitting.

    **Strengths**:
    - The test provides a realistic assessment of a model's predictive performance on unseen data, thereby estimating
    its generalizability.
    - It incorporates several performance metrics into the evaluation, offering a comprehensive look at performance.
    - The test aids in the detection of overfitting, a crucial factor for all machine learning models.

    **Limitations**:
    - The effectiveness of this test is significantly dependent on the quality and the representativeness of the test
    dataset. Performance metrics may not accurately reflect the true performance of the model if the test database is
    not a good representative of the real-world data the model will be working on.
    - The metrics used (accuracy, precision, recall and F1 score) make the assumption that all errors and
    misclassifications bear equal importance. This, however, may not align with certain real-world scenarios where some
    types of errors might have more significant implications than others.
    """

    name = "classifier_out_of_sample_performance"
    required_inputs = ["model", "model.test_ds"]
    metadata = {
        "task_types": ["classification", "text_classification"],
        "tags": [
            "sklearn",
            "binary_classification",
            "multiclass_classification",
            "model_performance",
        ],
    }

    def y_true(self):
        return self.model.y_test_true

    def y_pred(self):
        return self.model.y_test_predict
