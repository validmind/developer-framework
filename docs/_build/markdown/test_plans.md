# Test Plans

Test Plans entry point


### validmind.test_plans.list_plans(pretty: bool = True)
Returns a list of all available test plans


### validmind.test_plans.list_tests(test_type: str = 'all', pretty: bool = True)
Returns a list of all available tests.


### validmind.test_plans.get_by_name(name: str)
Returns the test plan by name


### validmind.test_plans.describe_plan(plan_id: str)
Returns a description of the test plan


### validmind.test_plans.register_test_plan(plan_id: str, plan: TestPlan)
Registers a custom test plan

## Test Plans for SKLearn-Compatible Classifiers

Test plan for sklearn classifier models

Ideal setup is to have the API client to read a
custom test plan from the project’s configuration


### _class_ validmind.test_plans.sklearn_classifier.SKLearnClassifierMetrics(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, train_ds: Dataset = None, test_ds: Dataset = None, pbar: tqdm = None)
Bases: `TestPlan`

Test plan for sklearn classifier metrics


#### name(_: ClassVar[str_ _ = 'sklearn_classifier_metrics_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'train_ds', 'test_ds'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.model_validation.model_metadata.ModelMetadata'>, <class 'validmind.model_validation.sklearn.metrics.AccuracyScore'>, <class 'validmind.model_validation.sklearn.metrics.ConfusionMatrix'>, <class 'validmind.model_validation.sklearn.metrics.F1Score'>, <class 'validmind.model_validation.sklearn.metrics.PermutationFeatureImportance'>, <class 'validmind.model_validation.sklearn.metrics.PrecisionRecallCurve'>, <class 'validmind.model_validation.sklearn.metrics.PrecisionScore'>, <class 'validmind.model_validation.sklearn.metrics.RecallScore'>, <class 'validmind.model_validation.sklearn.metrics.ROCAUCScore'>, <class 'validmind.model_validation.sklearn.metrics.ROCCurve'>, <class 'validmind.model_validation.sklearn.metrics.CharacteristicStabilityIndex'>, <class 'validmind.model_validation.sklearn.metrics.PopulationStabilityIndex'>, <class 'validmind.model_validation.sklearn.metrics.SHAPGlobalImportance'>_ )

### _class_ validmind.test_plans.sklearn_classifier.SKLearnClassifierPerformance(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, train_ds: Dataset = None, test_ds: Dataset = None, pbar: tqdm = None)
Bases: `TestPlan`

Test plan for sklearn classifier models


#### name(_: ClassVar[str_ _ = 'sklearn_classifier_validation_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'train_ds', 'test_ds'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.model_validation.sklearn.threshold_tests.AccuracyTest'>, <class 'validmind.model_validation.sklearn.threshold_tests.F1ScoreTest'>, <class 'validmind.model_validation.sklearn.threshold_tests.ROCAUCScoreTest'>, <class 'validmind.model_validation.sklearn.threshold_tests.TrainingTestDegradationTest'>_ )

### _class_ validmind.test_plans.sklearn_classifier.SKLearnClassifierDiagnosis(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, train_ds: Dataset = None, test_ds: Dataset = None, pbar: tqdm = None)
Bases: `TestPlan`

Test plan for sklearn classifier model diagnosis tests


#### name(_: ClassVar[str_ _ = 'sklearn_classifier_model_diagnosis_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'train_ds', 'test_ds'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.model_validation.sklearn.threshold_tests.OverfitDiagnosisTest'>, <class 'validmind.model_validation.sklearn.threshold_tests.WeakspotsDiagnosisTest'>, <class 'validmind.model_validation.sklearn.threshold_tests.RobustnessDiagnosisTest'>_ )

### _class_ validmind.test_plans.sklearn_classifier.SKLearnClassifier(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, train_ds: Dataset = None, test_ds: Dataset = None, pbar: tqdm = None)
Bases: `TestPlan`

Test plan for sklearn classifier models that includes
both metrics and validation tests


#### name(_: ClassVar[str_ _ = 'sklearn_classifier_ )

#### required_context(_: ClassVar[List[str]_ _ = ['model', 'train_ds', 'test_ds'_ )

#### test_plans(_: ClassVar[List[object]_ _ = [<class 'validmind.test_plans.sklearn_classifier.SKLearnClassifierMetrics'>, <class 'validmind.test_plans.sklearn_classifier.SKLearnClassifierPerformance'>, <class 'validmind.test_plans.sklearn_classifier.SKLearnClassifierDiagnosis'>_ )
## Test Plans for Tabular Datasets

Test plan for tabular datasets

Ideal setup is to have the API client to read a
custom test plan from the project’s configuration


### _class_ validmind.test_plans.tabular_datasets.TabularDatasetDescription(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, train_ds: Dataset = None, test_ds: Dataset = None, pbar: tqdm = None)
Bases: `TestPlan`

Test plan to extract metadata and descriptive
statistics from a tabular dataset


#### name(_: ClassVar[str_ _ = 'tabular_dataset_description_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.data_validation.metrics.DatasetMetadata'>, <class 'validmind.data_validation.metrics.DatasetDescription'>, <class 'validmind.data_validation.metrics.DatasetCorrelations'>_ )

### _class_ validmind.test_plans.tabular_datasets.TabularDataQuality(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, train_ds: Dataset = None, test_ds: Dataset = None, pbar: tqdm = None)
Bases: `TestPlan`

Test plan for data quality on tabular datasets


#### name(_: ClassVar[str_ _ = 'tabular_data_quality_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### tests(_: ClassVar[List[object]_ _ = [<class 'validmind.data_validation.threshold_tests.ClassImbalanceTest'>, <class 'validmind.data_validation.threshold_tests.DuplicatesTest'>, <class 'validmind.data_validation.threshold_tests.HighCardinalityTest'>, <class 'validmind.data_validation.threshold_tests.HighPearsonCorrelationTest'>, <class 'validmind.data_validation.threshold_tests.MissingValuesTest'>, <class 'validmind.data_validation.threshold_tests.SkewnessTest'>, <class 'validmind.data_validation.threshold_tests.UniqueRowsTest'>, <class 'validmind.data_validation.threshold_tests.ZerosTest'>_ )

### _class_ validmind.test_plans.tabular_datasets.TabularDataset(config: {} = None, test_context: TestContext = None, _test_plan_instances: List[object] = None, dataset: Dataset = None, model: Model = None, train_ds: Dataset = None, test_ds: Dataset = None, pbar: tqdm = None)
Bases: `TestPlan`

Test plan for generic tabular datasets


#### name(_: ClassVar[str_ _ = 'tabular_dataset_ )

#### required_context(_: ClassVar[List[str]_ _ = ['dataset'_ )

#### test_plans(_: ClassVar[List[object]_ _ = [<class 'validmind.test_plans.tabular_datasets.TabularDatasetDescription'>, <class 'validmind.test_plans.tabular_datasets.TabularDataQuality'>_ )
