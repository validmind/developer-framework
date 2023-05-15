# Core Library Tests

## Model Validation Tests for SKLearn-Compatible Models

### Model Validation Metrics

Metrics functions models trained with sklearn or that provide
a sklearn-like API


### _class_ validmind.model_validation.sklearn.metrics.CharacteristicStabilityIndex(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Characteristic Stability Index between two datasets


#### name(_: ClassVar[str_ _ = 'csi_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### value_formatter(_: ClassVar[str | None_ _ = 'key_values_ )

#### run()
Calculates PSI for each of the dataset features


### _class_ validmind.model_validation.sklearn.metrics.ConfusionMatrix(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Confusion Matrix


#### name(_: ClassVar[str_ _ = 'confusion_matrix_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### summary(metric_value)
Return the metric summary. Should be overridden by subclasses. Defaults to None.
The metric summary allows renderers (e.g. Word and ValidMind UI) to display a
short summary of the metric results.

We return None here because the metric summary is optional.


#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.PermutationFeatureImportance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Permutation Feature Importance


#### name(_: ClassVar[str_ _ = 'pfi_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.PrecisionRecallCurve(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Precision Recall Curve


#### name(_: ClassVar[str_ _ = 'pr_curve_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.ClassifierPerformance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Test that outputs the performance of the model on the training or test data.


#### default_params(_: ClassVar[dict_ _ = {'metrics': ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>, 'f1': functools.partial(<function f1_score>, zero_division=0), 'precision': functools.partial(<function precision_score>, zero_division=0), 'recall': functools.partial(<function recall_score>, zero_division=0), 'roc_auc': <function roc_auc_score>_ )

#### metric_definitions(_ = {'accuracy': 'Overall, how often is the model correct?', 'f1': 'Harmonic mean of precision and recall', 'precision': 'When the model predicts "{target_column}", how often is it correct?', 'recall': 'When it\\'s actually "{target_column}", how often does the model predict "{target_column}"?', 'roc_auc': 'Area under the Receiver Operating Characteristic curve'_ )

#### metric_formulas(_ = {'accuracy': 'TP + TN / (TP + TN + FP + FN)', 'f1': '2 x (Precision x Recall) / (Precision + Recall)', 'precision': 'TP / (TP + FP)', 'recall': 'TP / (TP + FN)', 'roc_auc': 'TPR / FPR'_ )

#### summary(metric_value: dict)
Return the metric summary. Should be overridden by subclasses. Defaults to None.
The metric summary allows renderers (e.g. Word and ValidMind UI) to display a
short summary of the metric results.

We return None here because the metric summary is optional.


#### y_true()

#### y_pred()

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.ClassifierInSamplePerformance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `ClassifierPerformance`

Test that outputs the performance of the model on the training data.


#### name(_: ClassVar[str_ _ = 'classifier_in_sample_performance_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'model.train_ds'_ )

#### description()
Return the metric description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### y_true()

#### y_pred()

### _class_ validmind.model_validation.sklearn.metrics.ClassifierOutOfSamplePerformance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `ClassifierPerformance`

Test that outputs the performance of the model on the test data.


#### name(_: ClassVar[str_ _ = 'classifier_out_of_sample_performance_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'model.test_ds'_ )

#### description()
Return the metric description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### y_true()

#### y_pred()

### _class_ validmind.model_validation.sklearn.metrics.ROCCurve(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

ROC Curve


#### name(_: ClassVar[str_ _ = 'roc_curve_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.SHAPGlobalImportance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

SHAP Global Importance


#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### name(_: ClassVar[str_ _ = 'shap_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.PopulationStabilityIndex(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Population Stability Index between two datasets


#### name(_: ClassVar[str_ _ = 'psi_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### value_formatter(_: ClassVar[str | None_ _ = 'records_ )

#### run()
Run the metric calculation and cache its results

### Data Validation Threshold Tests

Threshold based tests


### _class_ validmind.model_validation.sklearn.threshold_tests.MinimumAccuracy(test_context: TestContext, params: dict | None = None, result: TestResults | None = None)
Bases: `ThresholdTest`

Test that the model’s prediction accuracy on a dataset meets or
exceeds a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'accuracy_score_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.7_ )

#### summary(results: List[TestResult], all_passed: bool)
The accuracy score test returns results like these:
[{“values”: {“score”: 0.734375, “threshold”: 0.7}, “passed”: true}]


#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.MinimumF1Score(test_context: TestContext, params: dict | None = None, result: TestResults | None = None)
Bases: `ThresholdTest`

Test that the model’s F1 score on the validation dataset meets or
exceeds a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'f1_score_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.5_ )

#### summary(results: List[TestResult], all_passed: bool)
The f1 score test returns results like these:
[{“values”: {“score”: 0.734375, “threshold”: 0.7}, “passed”: true}]


#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.MinimumROCAUCScore(test_context: TestContext, params: dict | None = None, result: TestResults | None = None)
Bases: `ThresholdTest`

Test that the model’s ROC AUC score on the validation dataset meets or
exceeds a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'roc_auc_score_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.5_ )

#### summary(results: List[TestResult], all_passed: bool)
The roc auc score test returns results like these:
[{“values”: {“score”: 0.734375, “threshold”: 0.7}, “passed”: true}]


#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.TrainingTestDegradation(test_context: TestContext, params: dict | None = None, result: TestResults | None = None)
Bases: `ThresholdTest`

Test that the degradation in performance between the training and test datasets
does not exceed a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'training_test_degradation_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model'_ )

#### default_params(_: ClassVar[dict_ _ = {'max_threshold': 0.1, 'metrics': ['accuracy', 'precision', 'recall', 'f1']_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>, 'f1': functools.partial(<function f1_score>, zero_division=0), 'precision': functools.partial(<function precision_score>, zero_division=0), 'recall': functools.partial(<function recall_score>, zero_division=0)_ )

#### summary(results: List[TestResult], all_passed: bool)
The training test degradation test returns results like these:
[{“values”:

> {“test_score”: 0.7225, “train_score”: 0.7316666666666667, “degradation”: 0.012528473804100214}, “test_name”: “accuracy”, “passed”: true}, …]


#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.OverfitDiagnosis(test_context: TestContext, params: dict | None = None, result: TestResults | None = None)
Bases: `ThresholdTest`

Test that identify overfit regions with high residuals by histogram slicing techniques.


#### category(_: ClassVar[str_ _ = 'model_diagnosis_ )

#### name(_: ClassVar[str_ _ = 'overfit_regions_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'model.train_ds', 'model.test_ds'_ )

#### default_params(_: ClassVar[dict_ _ = {'cut_off_percentage': 4, 'features_columns': None_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>_ )

#### description()
Return the test description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.WeakspotsDiagnosis(test_context: TestContext, params: dict | None = None, result: TestResults | None = None)
Bases: `ThresholdTest`

Test that identify weak regions with high residuals by histogram slicing techniques.


#### category(_: ClassVar[str_ _ = 'model_diagnosis_ )

#### name(_: ClassVar[str_ _ = 'weak_spots_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'model.train_ds', 'model.test_ds'_ )

#### default_params(_: ClassVar[dict_ _ = {'features_columns': None, 'thresholds': {'accuracy': 0.75, 'f1': 0.7, 'precision': 0.5, 'recall': 0.5}_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>, 'f1': functools.partial(<function f1_score>, zero_division=0), 'precision': functools.partial(<function precision_score>, zero_division=0), 'recall': functools.partial(<function recall_score>, zero_division=0)_ )

#### description()
Return the test description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.RobustnessDiagnosis(test_context: TestContext, params: dict | None = None, result: TestResults | None = None)
Bases: `ThresholdTest`

Test robustness of model by perturbing the features column values by adding noise within scale
stardard deviation.


#### category(_: ClassVar[str_ _ = 'model_diagnosis_ )

#### name(_: ClassVar[str_ _ = 'robustness_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'model.train_ds', 'model.test_ds'_ )

#### default_params(_: ClassVar[dict_ _ = {'features_columns': None, 'scaling_factor_std_dev_list': [0.01, 0.02]_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>_ )

#### description()
Return the test description. Should be overridden by subclasses. Defaults
to returning the class’ docstring


#### run()
Run the test and cache its results


#### add_noise_std_dev(values: List[float], x_std_dev: float)
Adds Gaussian noise to a list of values.


* **Parameters**

    
    * **values** (*list**[**float**]*) – A list of numerical values to which noise is added.


    * **x_std_dev** (*float*) – A scaling factor for the standard deviation of the noise.



* **Returns**

    A tuple containing:


        * A list of noisy values, where each value is the sum of the corresponding value

        in the input list and a randomly generated value sampled from a Gaussian distribution
        with mean 0 and standard deviation x_std_dev times the standard deviation of the input list.
        - The standard deviation of the input list of values.




* **Return type**

    tuple[list[float], float]
