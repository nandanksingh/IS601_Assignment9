# ----------------------------------------------------------
# Author: Nandan Kumar
# Date: 11/03/2025
# Assignment-9: Working with Raw SQL in pgAdmin
# File: main.py
# ----------------------------------------------------------
# Description:
# Main FastAPI app integrating REST endpoints for
# arithmetic operations (addition, subtraction,
# multiplication, division) and PostgreSQL database setup.
# Includes logging, error handling, and health monitoring.
# ----------------------------------------------------------

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import logging
from app.operations import add, subtract, multiply, divide

# ----------------------------------------------------------
# Setup Logging
# ----------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# Initialize FastAPI app and Jinja2 templates
# ----------------------------------------------------------
app = FastAPI(
    title="FastAPI Calculator with PostgreSQL",
    description="Assignment-9: Demonstrating SQL operations with FastAPI + pgAdmin + PostgreSQL",
)
templates = Jinja2Templates(directory="templates")


# ----------------------------------------------------------
# Pydantic model for request body
# ----------------------------------------------------------
class OperationRequest(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")


# ----------------------------------------------------------
# Global Exception Handlers
# ----------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles invalid input validation errors (422 → 400)."""
    logger.error(f"Validation Error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid or missing numeric input."},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handles unexpected server errors."""
    logger.error(f"Unexpected Error: {exc}")
    return JSONResponse(status_code=400, content={"error": str(exc)})


# ----------------------------------------------------------
# Arithmetic Routes (REST API)
# ----------------------------------------------------------
@app.post("/add")
async def add_numbers(data: OperationRequest):
    """Add two numbers."""
    try:
        result = add(data.a, data.b)
        logger.info(f"Addition performed: {data.a} + {data.b} = {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Addition error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/subtract")
async def subtract_numbers(data: OperationRequest):
    """Subtract two numbers."""
    try:
        result = subtract(data.a, data.b)
        logger.info(f"Subtraction performed: {data.a} - {data.b} = {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Subtraction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/multiply")
async def multiply_numbers(data: OperationRequest):
    """Multiply two numbers."""
    try:
        result = multiply(data.a, data.b)
        logger.info(f"Multiplication performed: {data.a} * {data.b} = {result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"Multiplication error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/divide")
async def divide_numbers(data: OperationRequest):
    """Divide two numbers."""
    try:
        result = divide(data.a, data.b)
        logger.info(f"Division performed: {data.a} / {data.b} = {result}")
        return {"result": result}
    except ValueError as ve:
        logger.error(f"Division error: {ve}")
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        logger.error(f"Unexpected division error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------------------------------------
# Health Check Endpoint
# ----------------------------------------------------------
@app.get("/health")
async def health_check():
    """Health check endpoint for CI/CD and container monitoring."""
    logger.info("Health check ping received.")
    return {
        "status": "ok",
        "message": "FastAPI + PostgreSQL service is running successfully."
    }


# ----------------------------------------------------------
# Root Route (HTML Template)
# ----------------------------------------------------------
@app.get("/")
async def home(request: Request):
    """Render the homepage."""
    return templates.TemplateResponse("index.html", {"request": request})


# ----------------------------------------------------------
# Entry Point
# ----------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting FastAPI + PostgreSQL Integration App...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
