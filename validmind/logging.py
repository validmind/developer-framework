"""ValidMind logging module."""

import logging
import os
import time

import sentry_sdk
from sentry_sdk.utils import event_from_exception, exc_info_from_error

from .__version__ import __version__

__log_level = None
__dsn = "https://48f446843657444aa1e2c0d716ef864b@o1241367.ingest.sentry.io/4505239625465856"


def _get_log_level():
    """Get the log level from the environment variable if not already set"""
    if __log_level is not None:
        return __log_level

    log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
    if log_level_str not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid log level: {log_level_str}")

    return logging.getLevelName(log_level_str)


def init_sentry(server_config):
    """Initialize Sentry SDK for sending logs back to ValidMind

    This will usually only be called by the api_client module to initialize the
    sentry connection after the user calls `validmind.init()`. This is because the DSN
    and other config options will be returned by the API.

    Args:
        config (dict): The config dictionary returned by the API
            - send_logs (bool): Whether to send logs to Sentry (gets removed)
            - dsn (str): The Sentry DSN
            ...: Other config options for Sentry
    """
    if server_config.get("send_logs", False) is False:
        return

    config = {
        "dsn": __dsn,
        "traces_sample_rate": 1.0,
        "release": f"validmind-python@{__version__}",
        "in_app_include": ["validmind"],
        "environment": "production",
    }
    config.update({k: v for k, v in server_config.items() if k != "send_logs"})
    sentry_sdk.init(**config)


def get_logger(name="validmind", log_level=None):
    """Get a logger for the given name"""
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level or _get_log_level())
    logger.addHandler(handler)

    return logger


def log_performance(func, name=None, logger=None, force=False):
    """Decorator to log the time it takes to run a function

    Args:
        func (function): The function to decorate
        name (str, optional): The name of the function. Defaults to None.
        logger (logging.Logger, optional): The logger to use. Defaults to None.
        force (bool, optional): Whether to force logging even if env var is off

    Returns:
        function: The decorated function
    """
    # check if log level is set to debug
    if _get_log_level() != logging.DEBUG and not force:
        return func

    if logger is None:
        logger = get_logger()

    if name is None:
        name = func.__name__

    def wrap(*args, **kwargs):
        time1 = time.perf_counter()
        return_val = func(*args, **kwargs)
        time2 = time.perf_counter()

        logger.info("%s function took %0.3f ms" % (name, (time2 - time1) * 1000.0))

        return return_val

    return wrap


async def log_performance_async(func, name=None, logger=None, force=False):
    """Decorator to log the time it takes to run an async function

    Args:
        func (function): The function to decorate
        name (str, optional): The name of the function. Defaults to None.
        logger (logging.Logger, optional): The logger to use. Defaults to None.
        force (bool, optional): Whether to force logging even if env var is off

    Returns:
        function: The decorated function
    """
    # check if log level is set to debug
    if _get_log_level() != logging.DEBUG and not force:
        return func

    if logger is None:
        logger = get_logger()

    if name is None:
        name = func.__name__

    async def wrap(*args, **kwargs):
        time1 = time.perf_counter()
        return_val = await func(*args, **kwargs)
        time2 = time.perf_counter()

        logger.info("%s function took %0.3f ms" % (name, (time2 - time1) * 1000.0))

        return return_val

    return wrap


def send_single_error(error: Exception):
    """Send a single error to Sentry

    Args:
        error (Exception): The exception to send
    """
    event, hint = event_from_exception(exc_info_from_error(error))
    client = sentry_sdk.Client(__dsn, release=f"validmind-python@{__version__}")
    client.capture_event(event, hint=hint)

    time.sleep(0.25)  # wait for the event to be sent
