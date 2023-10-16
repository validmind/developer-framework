import pandas as pd
from validmind.vm_models import Metric, ResultSummary, ResultTable, ResultTableMetadata


class MyCustomTest(Metric):
    """
    This is a custom test from my local file system.
    """

    # The metric name should match the content ID on the template
    name = "my_local_provider.tests.MyCustomTest"
    required_inputs = []
    default_params = {}

    def run(self):
        return self.cache_results([{"bar": "baz"}])

    def summary(self, results):
        return ResultSummary(
            results=[
                ResultTable(
                    data=pd.DataFrame(results),
                    metadata=ResultTableMetadata(
                        title="Results from Local File Test Provider"
                    ),
                )
            ]
        )
