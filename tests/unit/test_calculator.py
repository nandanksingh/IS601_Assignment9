# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 10/27/2025
# Assignment 8: FastAPI Calculator
# File: tests/unit/test_calculator.py
# ----------------------------------------------------------
# Description:
# Unit tests for arithmetic functions in app/operations.py.
# Each test validates correct results for valid inputs and
# ensures proper error handling for invalid or zero division.
# ----------------------------------------------------------

import pytest
from app.operations import add, subtract, multiply, divide, _validate_numbers


# ----------------------------------------------------------
# Test add() function
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (3, 5, 8),
    (-2, 6, 4),
    (2.5, 1.5, 4.0),
    (0, 0, 0)
])
def test_add(a, b, expected):
    """Verify addition results with integers, negatives, and floats."""
    assert add(a, b) == expected


# ----------------------------------------------------------
# Test subtract() function
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (10, 4, 6),
    (4, 10, -6),
    (-3, -2, -1),
    (7.5, 2.5, 5.0)
])
def test_subtract(a, b, expected):
    """Verify subtraction results across positive, negative, and float values."""
    assert subtract(a, b) == expected


# ----------------------------------------------------------
# Test multiply() function
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (-2, 3, -6),
    (1.5, 2.0, 3.0),
    (0, 7, 0)
])
def test_multiply(a, b, expected):
    """Verify multiplication produces expected results for varied operands."""
    assert multiply(a, b) == expected


# ----------------------------------------------------------
# Test divide() function
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (8, 2, 4.0),
    (-9, 3, -3.0),
    (7.5, 2.5, 3.0),
    (0, 5, 0.0)
])
def test_divide(a, b, expected):
    """Verify division produces correct float results for valid inputs."""
    assert divide(a, b) == expected


# ----------------------------------------------------------
# Test divide() raises ValueError for divide by zero
# ----------------------------------------------------------
def test_divide_by_zero():
    """Ensure divide() raises ValueError when dividing by zero."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


# ----------------------------------------------------------
# Test _validate_numbers for invalid types
# ----------------------------------------------------------
@pytest.mark.parametrize("a, b", [
    ("abc", 5),
    (3, None),
    ([1, 2], 4),
])
def test_validate_numbers_invalid_type(a, b):
    """Ensure _validate_numbers() raises TypeError for non-numeric inputs."""
    with pytest.raises(TypeError, match="Both operands must be numbers"):
        _validate_numbers(a, b)
