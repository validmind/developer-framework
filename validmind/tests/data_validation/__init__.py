"""
Data Validation module
"""
import importlib
import inspect
from pathlib import Path

# loop through all files in `./metrics` and `./threshold_tests` and import the test classes in them
for path in Path(__file__).parent.glob("**/*.py"):
    if path.name.startswith("__"):
        continue

    module = importlib.import_module(f"{__name__}.{path.parent.name}.{path.stem}")
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            globals()[name] = obj
