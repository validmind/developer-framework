# Copyright © 2023 ValidMind Inc. All rights reserved.

from dataclasses import dataclass

from .ClassifierPerformance import ClassifierPerformance


@dataclass
class ClassifierOutOfSamplePerformance(ClassifierPerformance):
    """
    **Purpose**: This test is designed to assess the performance of a Machine Learning model on out-of-sample data -
    i.e., data not used during the training phase. This test uses a variety of metrics (e.g., accuracy, precision,
    recall, F1 score) to evaluate how well the trained model generalizes to unseen data. It helps to ensure that the
    model is not overfitting the training data and is capable of making accurate predictions on new, unseen data.

    **Test Mechanism**: The test invokes the metrics on the model's predicted outcomes for the testing data set and
    compares those predictions to the actual outcomes. If the testing data set is properly set aside during the model
    training and is not used in any way in the model learning process, it should provide a fair and unbiased measure of
    how well the model can generalize. The metrics used typically include accuracy (proportion of correct predictions),
    precision (proportion of positive predictions that were correct), recall (proportion of actual positives that were
    predicted correctly), and F1 score (a single statistic that balances precision and recall).

    **Signs of High Risk**: Indications of high risk might include a low accuracy rate, low precision and recall rates,
    a low F1 score, or significant discrepancies between the model's performance on training data and on testing data.
    The latter may point to overfitting, meaning the model may not generalize well to new data.

    **Strengths**: The major strength of this test is its ability to measure a model's predictive performance on unseen
    data, thereby giving a fair estimate of its generalizability. This test takes into account various performance
    metrics to provide a comprehensive performance evaluation. It also helps detect overfitting, an important aspect to
    consider for any machine learning model.

    **Limitations**: This test's limitations are centered around the dependability of the test dataset. If the test
    dataset is not a good representative of the real-world data the model will be applied to, the performance metrics
    may not accurately reflect the true performance of the model. It's also worth noting that all the metrics used
    (accuracy, precision, recall and F1 score) assume that all errors or misclassifications are equally important,
    which is not always the case in real-world scenarios.
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
