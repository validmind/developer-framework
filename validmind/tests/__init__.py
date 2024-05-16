# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

"""All Tests for ValidMind"""

import importlib
import inspect
import json
import sys
from pathlib import Path
from pprint import pformat
from typing import Dict
from uuid import uuid4

import pandas as pd
from ipywidgets import HTML, Accordion

from ..errors import LoadTestError
from ..html_templates.content_blocks import test_content_block_html
from ..logging import get_logger
from ..unit_metrics import run_metric
from ..unit_metrics.composite import load_composite_metric
from ..utils import (
    NumpyEncoder,
    display,
    format_dataframe,
    fuzzy_match,
    md_to_html,
    test_id_to_name,
)
from ..vm_models import TestContext, TestInput
from .decorator import metric, tags, tasks
from .test_providers import LocalTestProvider, TestProvider

logger = get_logger(__name__)


__all__ = [
    "data_validation",
    "model_validation",
    "prompt_validation",
    "list_tests",
    "load_test",
    "describe_test",
    "register_test_provider",
    "LoadTestError",
    "LocalTestProvider",
    # Decorators for functional metrics
    "metric",
    "tags",
    "tasks",
]

__tests = None
__test_classes = None

__test_providers: Dict[str, TestProvider] = {}
__custom_tests: Dict[str, object] = {}


def _test_description(test_class, truncate=True):
    description = inspect.getdoc(test_class).strip()

    if truncate and len(description.split("\n")) > 5:
        return description.strip().split("\n")[0] + "..."

    return description


def _load_tests(test_ids):
    global __test_classes

    if __test_classes is None:
        __test_classes = {}
        for test_id in test_ids:
            __test_classes[test_id] = load_test(test_id)


def _pretty_list_tests(tests, truncate=True):
    _load_tests(tests)

    table = [
        {
            "ID": test_id,
            "Name": test_id_to_name(test_id),
            "Test Type": __test_classes[test_id].test_type,
            "Description": _test_description(__test_classes[test_id], truncate),
            "Required Inputs": __test_classes[test_id].required_inputs,
            "Params": __test_classes[test_id].default_params or {},
        }
        for test_id in tests
    ]

    return format_dataframe(pd.DataFrame(table))


def _initialize_test_classes():
    """
    Initialize and populate the __test_classes global variable.
    """
    global __test_classes

    if __test_classes is None:
        __test_classes = {}
        for path in Path(__file__).parent.glob("**/*.py"):
            if path.name.startswith("__") or not path.name[0].isupper():
                continue  # skip special files and non-class files
            test_id = path.stem  # or any other way to define test_id
            __test_classes[test_id] = load_test(
                test_id
            )  # Assuming a function load_test exists


def list_tags():
    """
    List unique tags from all test classes.
    """
    _initialize_test_classes()

    unique_tags = set()

    for test_class in __test_classes.values():
        if hasattr(test_class, "metadata") and "tags" in test_class.metadata:
            for tag in test_class.metadata["tags"]:
                unique_tags.add(tag)

    return list(unique_tags)


def list_tasks_and_tags():
    """
    List all task types and their associated tags, with one row per task type and
    all tags for a task type in one row.

    Returns:
        pandas.DataFrame: A DataFrame with 'Task Type' and concatenated 'Tags'.
    """
    _initialize_test_classes()
    task_tags_dict = {}

    for test_class in __test_classes.values():
        if hasattr(test_class, "metadata"):
            task_types = test_class.metadata.get("task_types", [])
            tags = test_class.metadata.get("tags", [])

            for task_type in task_types:
                if task_type not in task_tags_dict:
                    task_tags_dict[task_type] = set()
                task_tags_dict[task_type].update(tags)

    # Convert the dictionary into a DataFrame
    task_tags_data = [
        {"Task Type": task_type, "Tags": ", ".join(tags)}
        for task_type, tags in task_tags_dict.items()
    ]
    return format_dataframe(pd.DataFrame(task_tags_data))


def list_task_types():
    """
    List unique task types from all test classes.
    """
    _initialize_test_classes()

    unique_task_types = set()

    for test_class in __test_classes.values():
        if hasattr(test_class, "metadata") and "task_types" in test_class.metadata:
            for task_type in test_class.metadata["task_types"]:
                unique_task_types.add(task_type)

    return list(unique_task_types)


def list_tests(filter=None, task=None, tags=None, pretty=True, truncate=True):
    """List all tests in the tests directory.

    Args:
        filter (str, optional): Find tests where the ID, task_type or tags match the
            filter string. Defaults to None.
        task (str, optional): Find tests that match the task type. Can be used to
            narrow down matches from the filter string. Defaults to None.
        tags (list, optional): Find tests that match list of tags. Can be used to
            narrow down matches from the filter string. Defaults to None.
        pretty (bool, optional): If True, returns a pandas DataFrame with a
            formatted table. Defaults to True.
        truncate (bool, optional): If True, truncates the test description to the first
            line. Defaults to True. (only used if pretty=True)

    Returns:
        list or pandas.DataFrame: A list of all tests or a formatted table.
    """
    global __tests

    if __tests is None:
        __tests = []

        directories = [p.name for p in Path(__file__).parent.iterdir() if p.is_dir()]

        for d in directories:
            for path in Path(__file__).parent.joinpath(d).glob("**/**/*.py"):
                if path.name.startswith("__") or not path.name[0].isupper():
                    continue  # skip __init__.py and other special files as well as non Test files

                test_id = (
                    f"validmind.{d}.{path.parent.stem}.{path.stem}"
                    if path.parent.parent.stem == d
                    else f"validmind.{d}.{path.stem}"
                )
                __tests.append(test_id)

    tests = __tests

    # first filter by the filter string since it's the most general search
    if filter is not None:
        _load_tests(tests)

        matched_by_id = [
            test_id for test_id in tests if filter.lower() in test_id.lower()
        ]
        matched_by_task = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and any(
                filter.lower() in task.lower()
                for task in __test_classes[test_id].metadata["task_types"]
            )
        ]
        matched_by_tags = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and any(
                fuzzy_match(tag, filter.lower())
                for tag in __test_classes[test_id].metadata["tags"]
            )
        ]

        tests = list(set(matched_by_id + matched_by_task + matched_by_tags))

    # then filter by task type and tags since they are more specific
    if task is not None:
        _load_tests(tests)

        tests = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and task in __test_classes[test_id].metadata["task_types"]
        ]

    if tags is not None:
        _load_tests(tests)

        tests = [
            test_id
            for test_id in tests
            if hasattr(__test_classes[test_id], "metadata")
            and all(tag in __test_classes[test_id].metadata["tags"] for tag in tags)
        ]

    if pretty:
        return _pretty_list_tests(tests, truncate=truncate)

    return tests


def _load_validmind_test(test_id, reload=False):
    parts = test_id.split(":")[0].split(".")

    test_module = ".".join(parts[1:-1])
    test_class = parts[-1]

    error = None
    test = None

    try:
        full_path = f"validmind.tests.{test_module}.{test_class}"

        if reload and full_path in sys.modules:
            module = importlib.reload(sys.modules[full_path])
        else:
            module = importlib.import_module(full_path)

        test = getattr(module, test_class)
    except ModuleNotFoundError as e:
        error = f"Unable to load test {test_id}. {e}"
    except AttributeError:
        error = f"Unable to load test {test_id}. Test not in module: {test_class}"

    return error, test


def load_test(test_id: str, reload=False):
    """Load a test by test ID

    Test IDs are in the format `namespace.path_to_module.TestClassOrFuncName[:result_id]`.
    The result ID is optional and is used to distinguish between multiple results from the
    running the same test.

    Args:
        test_id (str): The test ID in the format `namespace.path_to_module.TestName[:result_id]`
        reload (bool, optional): Whether to reload the test module. Defaults to False.
    """
    # TODO: we should use a dedicated class for test IDs to handle this consistently
    test_id, result_id = test_id.split(":", 1) if ":" in test_id else (test_id, None)

    error = None
    namespace = test_id.split(".", 1)[0]

    # TODO: lets implement an extensible loading system instead of this ugly if/else
    if test_id in __custom_tests:
        test = __custom_tests[test_id]

    elif test_id.startswith("validmind.composite_metric"):
        error, test = load_composite_metric(test_id)

    elif namespace == "validmind":
        error, test = _load_validmind_test(test_id, reload=reload)

    elif namespace in __test_providers:
        try:
            test = __test_providers[namespace].load_test(test_id.split(".", 1)[1])
        except Exception as e:
            error = (
                f"Unable to load test {test_id} from test provider: "
                f"{__test_providers[namespace]}\n Got Exception: {e}"
            )

    else:
        error = f"Unable to load test {test_id}. No test provider found."

    if error:
        logger.error(error)
        raise LoadTestError(error)

    if inspect.isfunction(test):
        # if its a function, we decorate it and then load the class
        # TODO: simplify this as we move towards all functional metrics
        # "_" is used here so it doesn't conflict with other test ids
        metric("_")(test)
        test = __custom_tests["_"]

    test.test_id = f"{test_id}:{result_id}" if result_id else test_id

    return test


def describe_test(test_id: str = None, raw: bool = False, show: bool = True):
    """Get or show details about the test

    This function can be used to see test details including the test name, description,
    required inputs and default params. It can also be used to get a dictionary of the
    above information for programmatic use.

    Args:
        test_id (str, optional): The test ID. Defaults to None.
        raw (bool, optional): If True, returns a dictionary with the test details.
            Defaults to False.
    """
    test = load_test(test_id)

    details = {
        "ID": test_id,
        "Name": test_id_to_name(test_id),
        "Test Type": test.test_type,
        "Required Inputs": test.required_inputs,
        "Params": test.default_params or {},
        "Description": inspect.getdoc(test).strip() or "",
    }

    if raw:
        return details

    html = test_content_block_html.format(
        test_id=test_id,
        uuid=str(uuid4()),
        title=f'{details["Name"]}',
        description=md_to_html(details["Description"].strip()),
        required_inputs=", ".join(details["Required Inputs"] or ["None"]),
        params_table="\n".join(
            [
                f"<tr><td>{param}</td><td>{pformat(value, indent=4)}</td></tr>"
                for param, value in details["Params"].items()
            ]
        ),
        table_display="table" if details["Params"] else "none",
        example_inputs=json.dumps(
            {name: f"my_vm_{name}" for name in details["Required Inputs"]},
            indent=4,
        ),
        example_params=json.dumps(details["Params"] or {}, indent=4, cls=NumpyEncoder),
        instructions_display="block" if show else "none",
    )

    if not show:
        return html

    display(
        Accordion(
            children=[HTML(html)],
            titles=[f"Test Description: {details['Name']} ('{test_id}')"],
        )
    )


def run_test(
    test_id: str = None,
    name: str = None,
    unit_metrics: list = None,
    params: dict = None,
    inputs=None,
    output_template=None,
    show=True,
    **kwargs,
):
    """Run a test by test ID

    Args:
        test_id (str, option): The test ID to run - required when running a single test
            i.e. when not running multiple unit metrics
        name (str, optional): The name of the test (used to create a composite metric
            out of multiple unit metrics) - required when running multiple unit metrics
        unit_metrics (list, optional): A list of unit metric IDs to run as a composite
            metric - required when running multiple unit metrics
        params (dict, optional): A dictionary of params to override the default params
        inputs: A dictionary of test inputs to pass to the Test
        output_template (str, optional): A template to use for customizing the output
        show (bool, optional): Whether to display the results. Defaults to True.
        **kwargs: Any extra arguments will be passed in via the TestInput object. i.e.:
            - dataset: A validmind Dataset object or a Pandas DataFrame
            - model: A model to use for the test
            - models: A list of models to use for the test
            other inputs can be accessed inside the test via `self.inputs["input_name"]`
    """
    if not test_id and not name and not unit_metrics:
        raise ValueError(
            "`test_id` or `name` and `unit_metrics` must be provided to run a test"
        )

    if (unit_metrics and not name) or (name and not unit_metrics):
        raise ValueError("`name` and `unit_metrics` must be provided together")

    if test_id and test_id.startswith("validmind.unit_metrics"):
        # TODO: as we move towards a more unified approach to metrics
        # we will want to make everything functional and remove the
        # separation between unit metrics and "normal" metrics
        return run_metric(test_id, inputs=inputs, params=params, show=show)

    if unit_metrics:
        metric_id_name = "".join(word[0].upper() + word[1:] for word in name.split())
        test_id = f"validmind.composite_metric.{metric_id_name}"

        error, TestClass = load_composite_metric(
            unit_metrics=unit_metrics, metric_name=metric_id_name
        )

        if error:
            raise LoadTestError(error)

    else:
        TestClass = load_test(test_id, reload=True)

    test = TestClass(
        test_id=test_id,
        context=TestContext(),
        inputs=TestInput({**kwargs, **(inputs or {})}),
        output_template=output_template,
        params=params,
    )

    test.run()

    if show:
        test.result.show()

    return test.result


def register_test_provider(namespace: str, test_provider: TestProvider) -> None:
    """Register an external test provider

    Args:
        namespace (str): The namespace of the test provider
        test_provider (TestProvider): The test provider
    """
    __test_providers[namespace] = test_provider


def _register_custom_test(test_id: str, test_class: object):
    __custom_tests[test_id] = test_class
