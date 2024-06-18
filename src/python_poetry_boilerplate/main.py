#!/usr/bin/env python

import logging

from rich import print
from rich.logging import RichHandler

from python_poetry_boilerplate.config.env import DEFAULT_TZ, LOG_LEVEL


def something(input: str) -> bool:
    """
    Simple function that returns True if the input is a string.
    For test purposes only.

    Args:
        input (str): Any input string

    Returns:
        bool: Boolean indicating whether the function was successful or not
    """
    return isinstance(input, str)


def main():
    """
    Main entry point for the application.
    """
    # setup basic logging
    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(module)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=LOG_LEVEL.upper(),
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    logging.info(f"LOG_LEVEL: {logging.getLevelName(logging.root.level)}")
    logging.info(f"DEFAULT_TZ: {DEFAULT_TZ}")

    input = "Hello world!"

    if something(input):
        print(input)
    else:
        print("Nope!")
