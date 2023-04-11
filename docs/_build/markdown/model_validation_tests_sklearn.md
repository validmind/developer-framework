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


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.CharacteristicStabilityIndex(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Characteristic Stability Index between two datasets


#### type(_: ClassVar[str_ _ = 'training_ )

#### scope(_: ClassVar[str_ _ = 'training:validation_ )

#### key(_: ClassVar[str_ _ = 'csi_ )

#### value_formatter(_: ClassVar[str | None_ _ = 'key_values_ )

#### run()
Calculates PSI for each of the dataset features


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.ConfusionMatrix(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Confusion Matrix


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'confusion_matrix_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.F1Score(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

F1 Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'f1_score_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.PermutationFeatureImportance(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Permutation Feature Importance


#### type(_: ClassVar[str_ _ = 'training_ )

#### scope(_: ClassVar[str_ _ = 'training_dataset_ )

#### key(_: ClassVar[str_ _ = 'pfi_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.PrecisionRecallCurve(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Precision Recall Curve


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'pr_curve_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.PrecisionScore(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Precision Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'precision_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.RecallScore(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

Recall Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'recall_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.ROCAUCScore(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

ROC AUC Score


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'roc_auc_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.ROCCurve(test_context: TestContext, params: dict | None = None, result: TestPlanMetricResult | None = None)
Bases: `Metric`

ROC Curve


#### type(_: ClassVar[str_ _ = 'evaluation_ )

#### scope(_: ClassVar[str_ _ = 'test_ )

#### key(_: ClassVar[str_ _ = 'roc_curve_ )

#### run()
Run the metric calculation and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.metrics.SHAPGlobalImportance(test_context: TestContext, result: TestPlanMetricResult | None = None)
Bases: `TestContextUtils`

SHAP Global Importance. Custom metric


#### test_type(_: ClassVar[str_ _ = 'SHAPGlobalImportance_ )

#### test_context(_: TestContex_ )

#### name(_ = 'shap_ )

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


#### test_context(_: TestContex_ )
### Data Validation Threshold Tests

Threshold based tests


### _class_ validmind.model_validation.sklearn.threshold_tests.AccuracyTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the accuracy score is above a threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'accuracy_score_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.7_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.threshold_tests.F1ScoreTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the F1 score is above a threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'f1_score_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.5_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.threshold_tests.ROCAUCScoreTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the ROC AUC score is above a threshold.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'roc_auc_score_ )

#### default_params(_: ClassVar[dict_ _ = {'min_threshold': 0.5_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )

### _class_ validmind.model_validation.sklearn.threshold_tests.TrainingTestDegradationTest(test_context: TestContext, params: dict | None = None, test_results: TestResults | None = None)
Bases: `ThresholdTest`

Test that the training set metrics are better than the test set metrics.


#### category(_: ClassVar[str_ _ = 'model_performance_ )

#### name(_: ClassVar[str_ _ = 'training_test_degradation_ )

#### default_params(_: ClassVar[dict_ _ = {'metrics': ['accuracy', 'precision', 'recall', 'f1']_ )

#### default_metrics(_ = {'accuracy': <function accuracy_score>, 'f1': <function f1_score>, 'precision': <function precision_score>, 'recall': <function recall_score>_ )

#### run()
Run the test and cache its results


#### test_context(_: TestContex_ )
