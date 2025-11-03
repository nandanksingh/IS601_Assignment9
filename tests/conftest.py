# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 10/27/2025
# Assignment-8: FastAPI Calculator
# File: tests/conftest.py
# ----------------------------------------------------------
# Description:
# Provides reusable pytest fixtures for end-to-end (E2E)
# testing of the FastAPI Calculator web application.
# Automatically starts the FastAPI server, initializes a
# headless Playwright browser, and ensures all resources
# are cleanly closed after testing.
# ----------------------------------------------------------

import subprocess
import time
import pytest
import requests
from playwright.sync_api import sync_playwright


# ----------------------------------------------------------
# Fixture: Start and stop FastAPI server
# ----------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def fastapi_server():
    """
    Start the FastAPI app before running E2E tests
    and stop it after all tests finish.
    """
    print("\n🚀 Starting FastAPI server for E2E tests...")
    server = subprocess.Popen(["python", "main.py"])
    url = "http://127.0.0.1:8000/"
    started = False

    # Wait for the server to become responsive
    for _ in range(30):
        try:
            if requests.get(url).status_code == 200:
                started = True
                print("✅ FastAPI server is running.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)

    if not started:
        server.terminate()
        raise RuntimeError("❌ FastAPI server did not start in time.")

    yield  # Run the tests

    # Graceful shutdown
    print("\n🛑 Stopping FastAPI server...")
    try:
        server.terminate()
        server.wait(timeout=10)
        print("✅ FastAPI server stopped successfully.")
    except Exception:
        print("⚠️ Could not cleanly stop the FastAPI server.")


# ----------------------------------------------------------
# Fixture: Initialize Playwright
# ----------------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    """Manage Playwright instance lifecycle."""
    with sync_playwright() as playwright:
        yield playwright


# ----------------------------------------------------------
# Fixture: Launch Chromium browser
# ----------------------------------------------------------
@pytest.fixture(scope="session")
def browser(playwright_instance):
    """
    Launch a headless Chromium browser for the test session.
    Headless mode ensures automation runs without UI display.
    """
    print("🧭 Launching Chromium browser (headless)...")
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()
    print("✅ Browser closed.")


# ----------------------------------------------------------
# Fixture: Create a fresh page for each test
# ----------------------------------------------------------
@pytest.fixture(scope="function")
def page(browser):
    """
    Provide a clean browser page (tab) for each E2E test.
    Prevents test interference and keeps state isolated.
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
