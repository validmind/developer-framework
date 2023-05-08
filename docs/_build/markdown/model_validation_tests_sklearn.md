# Core Library Tests

## Model Validation Tests for SKLearn-Compatible Models

### Model Validation Metrics

Metrics functions models trained with sklearn or that provide
a sklearn-like API


### _class_ validmind.model_validation.sklearn.metrics.AccuracyScore(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Accuracy Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'accuracy_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.CharacteristicStabilityIndex(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Characteristic Stability Index between two datasets


#### type(_: ClassVar[str_ _ = 'training_ )

#### scope(_: ClassVar[str_ _ = 'training:validation_ )

#### key(_: ClassVar[str_ _ = 'csi_ )

#### value_formatter(_: ClassVar[str | None_ _ = 'key_values_ )

#### run()
Calculates PSI for each of the dataset features


### _class_ validmind.model_validation.sklearn.metrics.ConfusionMatrix(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Confusion Matrix


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'confusion_matrix_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.F1Score(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

F1 Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'f1_score_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.PermutationFeatureImportance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Permutation Feature Importance


#### type(_: ClassVar[str_ _ = 'training_ )

#### scope(_: ClassVar[str_ _ = 'training_dataset_ )

#### key(_: ClassVar[str_ _ = 'pfi_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.PrecisionRecallCurve(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Precision Recall Curve


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'pr_curve_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.PrecisionScore(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Precision Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'precision_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.RecallScore(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Recall Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'recall_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.ROCAUCScore(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

ROC AUC Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'roc_auc_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.ROCCurve(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

ROC Curve


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'roc_curve_ )

#### run()
Run the metric calculation and cache its results


### _class_ validmind.model_validation.sklearn.metrics.SHAPGlobalImportance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `TestContextUtils`

SHAP Global Importance. Custom metric


#### test_context(_: TestContex_ )

#### test_type(_: ClassVar[str_ _ = 'SHAPGlobalImportance_ )

#### default_params(_: ClassVar[dict_ _ = {_ )

#### name(_ = 'shap_ )

#### params(_: dic_ _ = Non_ )

#### result(_: TestPlanMetricResul_ _ = Non_ )

#### run()

### _class_ validmind.model_validation.sklearn.metrics.PopulationStabilityIndex(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Population Stability Index between two datasets


#### type(_: ClassVar[str_ _ = 'training_ )

#### scope(_: ClassVar[str_ _ = 'training:validation_ )

#### key(_: ClassVar[str_ _ = 'psi_ )

#### value_formatter(_: ClassVar[str | None_ _ = 'records_ )

#### run()
Run the metric calculation and cache its results

### Data Validation Threshold Tests

Threshold based tests


### _class_ validmind.model_validation.sklearn.threshold_tests.MinimumAccuracy(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the model’s prediction accuracy on a dataset meets or
exceeds a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'accuracy_score_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.7_ )

#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.MinimumF1Score(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the model’s F1 score on the validation dataset meets or
exceeds a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'f1_score_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.5_ )

#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.MinimumROCAUCScore(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the model’s ROC AUC score on the validation dataset meets or
exceeds a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'roc_auc_score_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.5_ )

#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.TrainingTestDegradation(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the degradation in performance between the training and test datasets
does not exceed a predefined threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'training_test_degradation_ )

#### default_params(_: ClassVar[dict_ _ = {'metrics': ['accuracy', 'precision', 'recall', 'f1']_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>, 'f1': functools.partial(<function f1_score>, zero_division=0), 'precision': functools.partial(<function precision_score>, zero_division=0), 'recall': functools.partial(<function recall_score>, zero_division=0)_ )

#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.OverfitDiagnosis(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that identify overfit regions with high residuals by histogram slicing techniques.


#### category(_: ClassVar[str_ _ = 'model_diagnosis_ )

#### name(_: ClassVar[str_ _ = 'overfit_regions_ )

#### default_params(_: ClassVar[dict_ _ = {'cut_off_percentage': 4, 'features_columns': None_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>_ )

#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.WeakspotsDiagnosis(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that identify weak regions with high residuals by histogram slicing techniques.


#### category(_: ClassVar[str_ _ = 'model_diagnosis_ )

#### name(_: ClassVar[str_ _ = 'weak_spots_ )

#### default_params(_: ClassVar[dict_ _ = {'features_columns': None, 'thresholds': {'accuracy': 0.75, 'f1': 0.7, 'precision': 0.5, 'recall': 0.5}_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>, 'f1': functools.partial(<function f1_score>, zero_division=0), 'precision': functools.partial(<function precision_score>, zero_division=0), 'recall': functools.partial(<function recall_score>, zero_division=0)_ )

#### run()
Run the test and cache its results


### _class_ validmind.model_validation.sklearn.threshold_tests.RobustnessDiagnosis(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test robustness of model by perturbing the features column values


#### category(_: ClassVar[str_ _ = 'model_diagnosis_ )

#### name(_: ClassVar[str_ _ = 'robustness_ )

#### default_params(_: ClassVar[dict_ _ = {'features_columns': None, 'scaling_factor_std_dev_list': [0.01, 0.02]_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>_ )

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
