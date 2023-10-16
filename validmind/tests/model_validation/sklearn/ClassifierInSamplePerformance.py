# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance


@dataclass
class ClassifierInSamplePerformance(ClassifierPerformance):
    """
    Evaluates ML model's in-sample performance using accuracy, precision, recall, and F1 score to assess generalization
    and overfitting.

    **Purpose**: The purpose of this metric is to evaluate the performance of the machine learning model on the
    training data. This test gauges the model's ability to generalize its predictions to new, unseen data and assesses
    the level of the model's overfitting on the training set by measuring commonly-used metrics such as accuracy,
    precision, recall, and F1 score.

    **Test Mechanism**: The implementation of this test incorporates various metrics including accuracy, precision,
    recall, and F1 score. These metrics are applied on the model's predictions of the training set and compared with
    the true output. The accuracy evaluates the proportion of correct predictions out of the total predictions.
    Meanwhile, precision measures the accurate positive predictions relative to the total number of positive
    predictions. The recall metric indicates the proportion of true positive predictions in relation to the overall
    number of actual positives in the dataset. Lastly, the F1 score represents the harmonic mean of precision and
    recall, thus providing a comprehensive appraisal of the model's performance.

    **Signs of High Risk**:
    - A near-perfect performance on all metrics on the training data, coupled with inferior performance on unseen data,
    may be indicative of overfitting. This constitutes a high-risk scenario.
    - Low values on any of these metrics may signal an underperforming model, posing a potential risk for
    production-grade applications.

    **Strengths**:
    - Using conventional metrics such as accuracy, precision, recall, and F1 score allows for an all-encompassing
    evaluation of the model's performance.
    - The results are interpretable due to the widespread use and understanding of these metrics in the machine
    learning field.
    - Being applied to the training set, this test can detect overfitting early in the model's development stage.

    **Limitations**:
    - Although these metrics yield valuable insights, they are susceptible to biases inherent in the training data.
    - There's always a chance for disparity between the model's performance in the training set and performance with
    new, unseen data.
    - Therefore, this test should be supplemented with additional validation tactics, such as k-fold cross-validation
    or out-of-sample testing, to provide a more unbiased evaluation of the model's performance.
    """

    name = "classifier_in_sample_performance"
    required_inputs = ["model", "model.train_ds"]
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
        return self.model.y_train_true

    def y_pred(self):
        return self.model.y_train_predict
