# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 11/03/2025
# Assignment-9: Working with Raw SQL in pgAdmin
# File: tests/integration/test_fastapi_calculator.py
# ----------------------------------------------------------
# Description:
# Integration tests for FastAPI Calculator endpoints.
# These tests verify API routes (/add, /subtract, /multiply, /divide)
# return correct JSON responses and handle invalid inputs gracefully.
#
# In this assignment, these routes simulate the API layer that could
# later be connected to a PostgreSQL database (via Docker Compose)
# for logging and relational data operations.
# ----------------------------------------------------------

import pytest
import asyncio
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from main import app


# ----------------------------------------------------------
# Fixture: FastAPI client
# ----------------------------------------------------------
@pytest.fixture(scope="module")
def client():
    """Create a reusable TestClient for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


# ----------------------------------------------------------
# /add endpoint
# ----------------------------------------------------------
def test_add_endpoint(client):
    response = client.post("/add", json={"a": 5, "b": 7})
    assert response.status_code == 200
    assert response.json() == {"result": 12}


# ----------------------------------------------------------
# /subtract endpoint
# ----------------------------------------------------------
def test_subtract_endpoint(client):
    response = client.post("/subtract", json={"a": 15, "b": 4})
    assert response.status_code == 200
    assert response.json() == {"result": 11}


# ----------------------------------------------------------
# /multiply endpoint
# ----------------------------------------------------------
def test_multiply_endpoint(client):
    response = client.post("/multiply", json={"a": 6, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 18}


# ----------------------------------------------------------
# /divide endpoint
# ----------------------------------------------------------
def test_divide_endpoint(client):
    response = client.post("/divide", json={"a": 20, "b": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 4.0}


# ----------------------------------------------------------
# /divide endpoint → Division by zero
# ----------------------------------------------------------
def test_divide_by_zero_error(client):
    """Ensure division by zero returns proper 400 error with JSON response."""
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert response.json() == {"error": "Cannot divide by zero."}


# ----------------------------------------------------------
# Invalid Input Validation Tests
# ----------------------------------------------------------
@pytest.mark.parametrize("endpoint, payload", [
    ("/add", {"a": None, "b": 5}),
    ("/subtract", {"a": 5, "b": None}),
    ("/multiply", {"a": None, "b": 3}),
    ("/divide", {"a": 7, "b": None}),
])
def test_invalid_type_triggers_typeerror(client, endpoint, payload):
    """Ensure endpoints return 400 for non-numeric or null inputs (custom handler)."""
    response = client.post(endpoint, json=payload)
    assert response.status_code == 400
    body = response.json()
    assert "error" in body
    assert "Invalid" in body["error"]


# ----------------------------------------------------------
# Health Check Endpoint
# ----------------------------------------------------------
def test_health_endpoint(client):
    """Ensure /health endpoint responds correctly."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"].lower() == "ok"
    assert "FastAPI Calculator" in data["message"]


# ----------------------------------------------------------
# Coverage Tests
# ----------------------------------------------------------
def test_generic_add_error_handling(monkeypatch, client):
    """Force add() to raise an exception to cover the /add route error block."""
    def mock_add(a, b):
        raise Exception("Mocked addition failure")

    import main
    import app.operations
    monkeypatch.setattr(main, "add", mock_add)
    monkeypatch.setattr(app.operations, "add", mock_add)

    response = client.post("/add", json={"a": 1, "b": 2})
    assert response.status_code == 400
    assert "Mocked addition failure" in response.text


def test_request_validation_error_handler():
    """Manually trigger async validation_exception_handler in main.py."""
    import main

    err = RequestValidationError([
        {"loc": ["body", "a"], "msg": "bad input", "type": "value_error"}
    ])

    response = asyncio.run(main.validation_exception_handler(None, err))
    assert response.status_code == 400
    body = response.body.decode()
    assert "Invalid or missing numeric input" in body
    assert "error" in body


def test_main_entrypoint(monkeypatch):
    """Ensure __main__ block in main.py is covered without running uvicorn."""
    import sys
    import main
    import importlib

    monkeypatch.setattr("uvicorn.run", lambda *args, **kwargs: None)
    sys.modules["__main__"] = main
    try:
        if hasattr(main, "__name__"):
            main.__name__ = "__main__"
        importlib.reload(main)
    finally:
        sys.modules["__main__"].__name__ = "main"


def test_global_exception_handler():
    """Trigger the global_exception_handler manually."""
    import main
    from starlette.responses import JSONResponse

    class DummyRequest:
        url = "http://testserver/error"

    response = asyncio.run(main.global_exception_handler(DummyRequest(), Exception("Simulated crash")))
    assert isinstance(response, JSONResponse)
    assert response.status_code == 400
    assert "Simulated crash" in response.body.decode()


def test_subtract_and_multiply_error_blocks(monkeypatch, client):
    """Force /subtract and /multiply to raise errors to hit exception blocks."""
    import main

    monkeypatch.setattr(main, "subtract", lambda a, b: (_ for _ in ()).throw(Exception("Subtraction fail")))
    res1 = client.post("/subtract", json={"a": 5, "b": 3})
    assert res1.status_code == 400
    assert "Subtraction fail" in res1.text

    monkeypatch.setattr(main, "multiply", lambda a, b: (_ for _ in ()).throw(Exception("Multiply fail")))
    res2 = client.post("/multiply", json={"a": 2, "b": 2})
    assert res2.status_code == 400
    assert "Multiply fail" in res2.text


def test_home_endpoint(client):
    """Covers GET / route (index.html render)."""
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers.get("content-type", "")


def test_divide_unexpected_exception(monkeypatch, client):
    """Trigger unexpected exception in /divide to hit Exception block."""
    import main

    def bad_divide(a, b):
        raise RuntimeError("Unexpected math error")

    monkeypatch.setattr(main, "divide", bad_divide)

    res = client.post("/divide", json={"a": 4, "b": 2})
    assert res.status_code == 400
    assert "Unexpected math error" in res.text
