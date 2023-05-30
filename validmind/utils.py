import asyncio
import json
import math

from typing import Any

import nest_asyncio
import numpy as np

from IPython.core import getipython
from numpy import ndarray
from tabulate import tabulate


DEFAULT_BIG_NUMBER_DECIMALS = 2
DEFAULT_SMALL_NUMBER_DECIMALS = 4


def is_notebook() -> bool:
    """
    Checks if the code is running in a Jupyter notebook or IPython shell

    https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
    """
    try:
        if getipython.get_ipython() is not None:
            return True
    except NameError:
        return False  # Probably standard Python interpreter

    return False


# hacky way to make async code run "synchronously" in colab
__loop: asyncio.AbstractEventLoop = None
try:
    from google.colab._shell import Shell  # type: ignore

    if isinstance(getipython.get_ipython(), Shell):
        __loop = asyncio.new_event_loop()
        nest_asyncio.apply(__loop)
except ModuleNotFoundError:
    if is_notebook():
        __loop = asyncio.new_event_loop()
        nest_asyncio.apply(__loop)


def nan_to_none(obj):
    if isinstance(obj, dict):
        return {k: nan_to_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [nan_to_none(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

    def encode(self, obj):
        obj = nan_to_none(obj)
        return super().encode(obj)

    def iterencode(self, obj, _one_shot: bool = ...):
        obj = nan_to_none(obj)
        return super().iterencode(obj, _one_shot)


def get_full_typename(o: Any) -> Any:
    """We determine types based on type names so we don't have to import
    (and therefore depend on) PyTorch, TensorFlow, etc.
    """
    instance_name = o.__class__.__module__ + "." + o.__class__.__name__
    if instance_name in ["builtins.module", "__builtin__.module"]:
        return o.__name__
    else:
        return instance_name


def is_matplotlib_typename(typename: str) -> bool:
    return typename.startswith("matplotlib.")


def is_plotly_typename(typename: str) -> bool:
    return typename.startswith("plotly.")


def precision_and_scale(x):
    """
    https://stackoverflow.com/questions/3018758/determine-precision-and-scale-of-particular-number-in-python

    Returns a (precision, scale) tuple for a given number.
    """
    max_digits = 14
    int_part = int(abs(x))
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
        return (magnitude, 0)
    frac_part = abs(x) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    scale = int(math.log10(frac_digits))
    return (magnitude + scale, scale)


def format_records(df):
    """
    Round the values on each dataframe's column to a given number of decimal places.
    The returned value is converted to a dict in "records" with Pandas's to_dict() function.

    We do this for display purposes before sending data to ValidMind. Rules:

    - Check if we are rendering "big" numbers greater than 10 or just numbers between 0 and 1
    - If the column's smallest number has more decimals 6, use that number's precision
      so we can avoid rendering a 0 instead
    - If the column's smallest number has less decimals than 6, use 6 decimal places
    """
    for col in df.columns:
        if df[col].dtype == "object":
            continue
        not_zero = df[col][df[col] != 0]
        min_number = not_zero.min()
        _, min_scale = precision_and_scale(min_number)

        if min_number >= 10:
            df[col] = df[col].round(DEFAULT_BIG_NUMBER_DECIMALS)
        elif min_scale > DEFAULT_SMALL_NUMBER_DECIMALS:
            df[col] = df[col].round(DEFAULT_SMALL_NUMBER_DECIMALS)
        else:
            df[col] = df[col].round(min_scale)

    return df.to_dict("records")


def format_key_values(key_values):
    """
    Round the values on each dict's value to a given number of decimal places.

    We do this for display purposes before sending data to ValidMind. Rules:

    - Assume the dict is in this form: {key1: value1, key2: value2, ...}
    - Check if we are rendering "big" numbers greater than 10 or just numbers between 0 and 1
    - If the column's smallest number has more decimals 6, use that number's precision
      so we can avoid rendering a 0 instead
    - If the column's smallest number has less decimals than 6, use 6 decimal places
    """
    min_number = min([v for v in key_values.values() if v != 0])
    _, min_scale = precision_and_scale(min_number)

    for key, value in key_values.items():
        # Some key values could be a single item ndarray, assert this
        if isinstance(value, ndarray):
            assert len(value) == 1, "Expected a single item ndarray"
            value = value[0]

        if min_number >= 10:
            key_values[key] = round(value, DEFAULT_BIG_NUMBER_DECIMALS)
        elif min_scale > DEFAULT_SMALL_NUMBER_DECIMALS:
            key_values[key] = round(value, DEFAULT_SMALL_NUMBER_DECIMALS)
        else:
            key_values[key] = round(value, min_scale)

    return key_values


def summarize_data_quality_results(results):
    """
    TODO: generalize this to work with metrics and test results

    Summarize the results of the data quality test suite
    """
    test_results = []
    for result in results:
        num_passed = len([r for r in result.results if r.passed])
        num_failed = len([r for r in result.results if not r.passed])

        percent_passed = (
            1 if len(result.results) == 0 else num_passed / len(result.results)
        )
        test_results.append(
            [
                result.test_name,
                result.passed,
                num_passed,
                num_failed,
                percent_passed * 100,
            ]
        )

    return tabulate(
        test_results,
        headers=["Test", "Passed", "# Passed", "# Errors", "% Passed"],
        numalign="right",
    )


def clean_docstring(docstring: str) -> str:
    """
    Clean up docstrings by removing leading and trailing whitespace and
    replacing newlines with spaces.
    """
    description = docstring.strip()
    paragraphs = description.split("\n\n")  # Split into paragraphs
    paragraphs = [
        " ".join([line.strip() for line in paragraph.split("\n")])
        for paragraph in paragraphs
    ]
    paragraphs = [
        paragraph.replace(" - ", "\n- ") for paragraph in paragraphs
    ]  # Add newline before list items
    # Join paragraphs with double newlines for markdown
    description = "\n\n".join(paragraphs)

    return description


def format_number(number):
    """
    Format a number for display purposes. If the number is a float, round it
    to 4 decimal places.
    """
    if isinstance(number, float):
        return round(number, 4)
    else:
        return number


def run_async(func, *args, name=None, **kwargs):
    """Helper function to run functions asynchronously

    This takes care of the complexity of running the logging functions asynchronously. It will
    detect the type of environment we are running in (ipython notebook or not) and run the
    function accordingly.

    Args:
        func (function): The function to run asynchronously
        *args: The arguments to pass to the function
        **kwargs: The keyword arguments to pass to the function

    Returns:
        The result of the function
    """
    try:
        if asyncio.get_event_loop().is_running() and is_notebook():
            if __loop:
                future = __loop.create_task(func(*args, **kwargs), name=name)
                # wait for the future result
                return __loop.run_until_complete(future)

            return asyncio.get_event_loop().create_task(
                func(*args, **kwargs), name=name
            )
    except RuntimeError:
        pass

    return asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))


def run_async_check(func, *args, **kwargs):
    """Helper function to run functions asynchronously if the task doesn't already exist"""
    if __loop:
        return  # we don't need this if we are using our own loop

    try:
        name = func.__name__

        for task in asyncio.all_tasks():
            if task.get_name() == name:
                return task

        return run_async(func, name=name, *args, **kwargs)

    except RuntimeError:
        pass
