"""
Custom setup to compile Cython files
"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "validmind/*.pyx", compiler_directives={"language_level": "3"}
    )
)
