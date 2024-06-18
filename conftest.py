#!/usr/bin/env python
import pytest


@pytest.fixture
def str_input():
    """
    A fixture that returns a string input for testing purposes.

    Returns:
        str: The string input "Hello World!".
    """
    return "Hello World!"


@pytest.fixture
def int_input():
    """
    Fixture function that returns an integer input value.

    Returns:
        int: The integer input value.
    """
    return 23
