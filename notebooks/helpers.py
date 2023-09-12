from validmind.tests import describe_test, load_test
from validmind.utils import run_async
from validmind.vm_models import TestContext


def run_test(test_name, params={}, *args, **kwargs):
    # The call to .data.values returns:
    # array([['ID:', 'validmind.data_validation.TimeSeriesOutliers'], ...
    test_details = describe_test(test_name)
    full_test_id = test_details.data.values[0][1]

    test_context = TestContext(*args, **kwargs)

    test = load_test(full_test_id)(test_context)
    # Fix this: we cannot pass params via load_test()
    test.params = params
    test.run()
    run_async(test.result.log)
    test.result.show()
