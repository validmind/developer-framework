from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


class MyCustomTest(Metric):
    """
    This is a custom test from my local file system.
    """

    type = "dataset"
    name = "my_custom_test"
    test_type = "metric"
    required_context = []
    default_params = {}

    def run(self):
        return self.cache_results({"foo": "bar"})

    def summary(self, results):
        return ResultSummary(
            results=[
                ResultTable(
                    data=[{"results": results}],
                    metadata=ResultTableMetadata(
                        title="Custom Test from External Test Provider"
                    ),
                )
            ]
        )
