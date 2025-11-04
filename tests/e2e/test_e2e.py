# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 11/03/2025
# Assignment-9: Working with Raw SQL in pgAdmin
# File: tests/e2e/test_e2e.py
# ----------------------------------------------------------
# Description:
# End-to-End (E2E) tests for the FastAPI Calculator web app.
# These tests use Playwright to simulate real user interactions
# with the browser and verify frontend–backend integration.
# In this assignment, E2E testing complements PostgreSQL setup
# in Docker Compose, ensuring that the app remains functional
# while database and API layers operate together.
# ----------------------------------------------------------

import pytest
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE_URL = "http://localhost:8000"


# ----------------------------------------------------------
# Fixture: Launch browser once per module
# ----------------------------------------------------------
@pytest.fixture(scope="module")
def browser():
    """Launch a Chromium browser instance for all E2E tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Create and close a new page for each E2E test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


# ----------------------------------------------------------
# Test: Homepage loads
# ----------------------------------------------------------
@pytest.mark.e2e
def test_homepage_loads(page):
    """Verify homepage loads successfully and shows correct title."""
    page.goto(BASE_URL)
    title_text = page.text_content("h1")
    assert title_text and "FastAPI Calculator" in title_text, "Homepage title missing or incorrect."


# ----------------------------------------------------------
# Test: Addition
# ----------------------------------------------------------
@pytest.mark.e2e
def test_addition(page):
    """Verify adding two numbers updates result correctly."""
    page.goto(BASE_URL)
    page.fill("#a", "5")
    page.fill("#b", "7")
    page.click("text=Add")
    page.wait_for_selector("#result")
    result_text = page.text_content("#result")
    assert "Result: 12" in result_text


# ----------------------------------------------------------
# Test: Subtraction
# ----------------------------------------------------------
@pytest.mark.e2e
def test_subtraction(page):
    """Verify subtraction displays correct result."""
    page.goto(BASE_URL)
    page.fill("#a", "15")
    page.fill("#b", "4")
    page.click("text=Subtract")
    page.wait_for_selector("#result")
    result_text = page.text_content("#result")
    assert "Result: 11" in result_text


# ----------------------------------------------------------
# Test: Multiplication
# ----------------------------------------------------------
@pytest.mark.e2e
def test_multiplication(page):
    """Verify multiplication displays correct result."""
    page.goto(BASE_URL)
    page.fill("#a", "6")
    page.fill("#b", "3")
    page.click("text=Multiply")
    page.wait_for_selector("#result")
    result_text = page.text_content("#result")
    assert "Result: 18" in result_text


# ----------------------------------------------------------
# Test: Division
# ----------------------------------------------------------
@pytest.mark.e2e
def test_division(page):
    """Verify division displays correct result."""
    page.goto(BASE_URL)
    page.fill("#a", "20")
    page.fill("#b", "5")
    page.click("text=Divide")
    page.wait_for_selector("#result")
    result_text = page.text_content("#result")
    assert "Result: 4" in result_text


# ----------------------------------------------------------
# Test: Division by zero
# ----------------------------------------------------------
@pytest.mark.e2e
def test_divide_by_zero(page):
    """Verify dividing by zero displays proper error message."""
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "0")
    page.click("text=Divide")
    try:
        page.wait_for_selector("#result", timeout=3000)
    except PlaywrightTimeoutError:
        pytest.fail("Result element not found after division by zero.")
    result_text = page.text_content("#result")
    assert "Error: Cannot divide by zero" in result_text


# ----------------------------------------------------------
# Test: Invalid input handling
# ----------------------------------------------------------
@pytest.mark.e2e
def test_invalid_input(page):
    """Verify non-numeric input triggers an error message."""
    page.goto(BASE_URL)
    page.fill("#a", "abc")
    page.fill("#b", "3")
    page.click("text=Add")
    page.wait_for_selector("#result")
    result_text = page.text_content("#result")
    assert "Error" in result_text


# ----------------------------------------------------------
# Test: Missing input handling
# ----------------------------------------------------------
@pytest.mark.e2e
def test_missing_input(page):
    """Verify that leaving input fields empty produces an error message."""
    page.goto(BASE_URL)
    page.fill("#a", "")
    page.fill("#b", "")
    page.click("text=Add")
    page.wait_for_selector("#result")
    result_text = page.text_content("#result")
    assert "Error" in result_text
