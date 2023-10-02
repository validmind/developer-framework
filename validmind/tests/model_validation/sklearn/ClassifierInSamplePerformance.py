# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance


@dataclass
class ClassifierInSamplePerformance(ClassifierPerformance):
    """
    **Purpose**: The purpose of this metric is to evaluate the performance of the machine learning model on the
    training data. It measures commonly-used metrics such as accuracy, precision, recall, and F1 score. This test is
    typically used to gauge the model's ability to generalize its predictions to new, unseen data. It also measures the
    model's level of overfitting on the training set.

    **Test Mechanism**: This test uses metrics like accuracy, precision, recall, and F1 score. It applies these metrics
    to the model's predictions on the training set, and compares them with the true values. The accuracy measures the
    ratio of correct predictions to the total number of predictions. Precision gauges the number of true positive
    predictions relative to the total number of positive predictions. Recall indicates the number of true positive
    predictions relative to the total number of actual positives in the dataset. Finally, F1 score is the harmonic mean
    of precision and recall, providing an overall measure of the model's performance.

    **Signs of High Risk**: If the model has near perfect performance on all metrics on the training data but performs
    poorly on unseen data, it could be a sign of overfitting and hence, a high-risk scenario. Also, low values on any
    of these metrics can indicate an underperforming model, which may pose risk in production-grade applications.

    **Strengths**: Analyzing the model's performance using standard metrics like accuracy, precision, recall, and F1
    score allows for a well-rounded assessment. The output is easy-to-interpret because they are widely used and
    understood in the machine learning community. Besides, since this test is applied to the training set, it can help
    detect instances of overfitting early in the model's development.

    **Limitations**: While these metrics provide useful insights, they are prone to biases in the training data. The
    model may perform well on the training set and yet perform poorly on new, unseen data. Therefore, this test should
    be complemented with additional validation techniques, such as k-fold cross-validation or out-of-sample testing, to
    ensure a less biased evaluation of the model's performance.
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
