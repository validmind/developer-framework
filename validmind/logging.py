"""ValidMind logging module."""

import logging
import os
import time

import sentry_sdk

from .__version__ import __version__


def init_sentry(config):
    """Initialize Sentry SDK for sending logs back to ValidMind

    This will usually only be called by the api_client module to initialize the sentry
    connection after the user calls `validmind.init()`. This is because the DSN and
    other config options will be returned by the API.

    Args:
        dsn (str, optional): The Sentry DSN to use. Defaults to None.
    """
    default_config = {
        "dsn": os.environ.get("VM_SENTRY_DSN"),
        "traces_sample_rate": 1.0,
        "release": f"validmind-python@{__version__}",
        "in_app_include": ["validmind"],
    }
    config = {**default_config, **config}

    if config["dsn"] is None:
        get_logger().warning("Tried to initialize Sentry but no DSN was provided")
        return

    sentry_sdk.init(**config)


def get_logger(name="validmind", log_level=None):
    """Get a logger for the given name"""
    if log_level is None:
        log_level = os.environ.get("VM_LOG_LEVEL", "INFO")

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logger


def log_performance(func, logger=None):
    """Decorator to log the time it takes to run a function

    Args:
        func (function): The function to decorate
        logger (logging.Logger, optional): The logger to use. Defaults to None.

    Returns:
        function: The decorated function
    """
    if logger is None:
        logger = get_logger()

    def wrap(*args, **kwargs):
        time1 = time.perf_counter()
        return_val = func(*args, **kwargs)
        time2 = time.perf_counter()

        logger.info(
            "%s function took %0.3f ms" % (func.__name__, (time2 - time1) * 1000.0)
        )

        return return_val

    return wrap
