# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 11/03/2025
# Assignment-9: Working with Raw SQL in pgAdmin
# File: app/operations.py
# ----------------------------------------------------------
# Description:
# Defines the core arithmetic functions for the FastAPI Calculator app.
# Each operation validates numeric inputs, logs execution details,
# and ensures consistent error handling for invalid data or operations.
#
# In this assignment, these functions act as the logical layer
# that can later interact with PostgreSQL for data storage and
# query testing using pgAdmin through Docker Compose.
# ----------------------------------------------------------

from typing import Union
import logging

# Type alias for numerical values
Number = Union[int, float]

# Configure module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ----------------------------------------------------------
# Helper: Validate numeric input
# ----------------------------------------------------------
def _validate_numbers(a: Number, b: Number) -> None:
    """Validate that both inputs are numeric types."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        logger.error(f"Invalid operands: a={a}, b={b}")
        raise TypeError("Both operands must be numbers.")
    return None


# ----------------------------------------------------------
# Add two numbers
# ----------------------------------------------------------
def add(a: Number, b: Number) -> Number:
    """Return the sum of two numbers."""
    _validate_numbers(a, b)
    result = a + b
    logger.info(f"Addition performed: {a} + {b} = {result}")
    return result


# ----------------------------------------------------------
# Subtract two numbers
# ----------------------------------------------------------
def subtract(a: Number, b: Number) -> Number:
    """Return the result of subtracting b from a."""
    _validate_numbers(a, b)
    result = a - b
    logger.info(f"Subtraction performed: {a} - {b} = {result}")
    return result


# ----------------------------------------------------------
# Multiply two numbers
# ----------------------------------------------------------
def multiply(a: Number, b: Number) -> Number:
    """Return the product of two numbers."""
    _validate_numbers(a, b)
    result = a * b
    logger.info(f"Multiplication performed: {a} * {b} = {result}")
    return result


# ----------------------------------------------------------
# Divide two numbers
# ----------------------------------------------------------
def divide(a: Number, b: Number) -> float:
    """Return the result of dividing a by b. Raises ValueError if b is zero."""
    _validate_numbers(a, b)
    if b == 0:
        logger.error(f"Division by zero attempted: a={a}, b={b}")
        raise ValueError("Cannot divide by zero.")
    result = a / b
    logger.info(f"Division performed: {a} / {b} = {result}")
    return result
