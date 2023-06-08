"""
Data Validation Tests for ValidMind
"""

# use this to import all modules in non-module subdirectories

import importlib
import inspect
from pathlib import Path

# list all directories in this directory
directories = [p.name for p in Path(__file__).parent.iterdir() if p.is_dir()]

# if the directory has an __init__.py file, skip it since it's itself a module
for d in directories:
    if Path(__file__).parent.joinpath(d, "__init__.py").exists():
        continue

    # list all files in the directory
    for path in Path(__file__).parent.joinpath(d).glob("**/*.py"):
        if path.name.startswith("__"):  # skip __init__.py and other special files
            continue

        # import the file as a module
        module = importlib.import_module(f"{__name__}.{d}.{path.stem}")
        # get the class that matches the name of the file
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name == path.stem:
                # add the class to the global namespace
                globals()[name] = obj
