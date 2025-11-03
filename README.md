## **Assignment 8 – FastAPI Calculator**

**Author:** Nandan Kumar
**Date:** October 27, 2025

---

## **Project Overview**

This project implements a **FastAPI-based web calculator** that performs four basic arithmetic operations — **addition**, **subtraction**, **multiplication**, and **division** — through a modern web interface and RESTful API endpoints.

It demonstrates the **end-to-end web development process**, including **backend development**, **frontend integration**, **automated testing**, **logging**, **security scanning**, **containerization**, and **continuous integration (CI/CD)** using **GitHub Actions** and **Docker**.

---

## **Learning Objectives**

Through this project, I learned to:

* Build and test web applications using **FastAPI**
* Connect backend and frontend components effectively
* Write **unit**, **integration**, and **end-to-end (E2E)** tests using **Pytest** and **Playwright**
* Apply structured **logging** for monitoring and debugging
* Automate workflows using **GitHub Actions**
* Containerize and deploy applications using **Docker**
* Perform **security vulnerability scanning** using **Trivy**

---

## **Application Structure**

| File                                             | Description                         |
| ------------------------------------------------ | ----------------------------------- |
| **app/operations.py**                            | Core arithmetic logic and logging   |
| **templates/index.html**                         | Frontend calculator UI              |
| **tests/unit/test_calculator.py**                | Unit tests for operations           |
| **tests/integration/test_fastapi_calculator.py** | Integration tests for API endpoints |
| **tests/e2e/test_e2e.py**                        | End-to-end Playwright tests         |
| **Dockerfile**                                   | Defines Docker build instructions   |
| **main.py**                                      | FastAPI entry point                 |
| **pytest.ini**                                   | Test and coverage settings          |
| **requirements.txt**                             | Python dependency list              |

---

## **Setup and Installation**

### ** Clone the Repository**

```bash
git clone https://github.com/nandanksingh/IS601_Assignment8.git
cd IS601_Assignment8
```

### ** Create and Activate Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

### ** Install Dependencies**

```bash
pip install -r requirements.txt
```

### ** Run the Application**

```bash
uvicorn main:app --reload
```

Open in your browser → **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## **Running with Docker**

### ** Build and Run the Container**

```bash
docker-compose up --build
```

### ** Access the Application**

 [http://localhost:8000](http://localhost:8000)

### ** Stop the Container**

```bash
docker-compose down
```

---

## **Published Docker Image**

The image is publicly available on **Docker Hub**:

🔗 [https://hub.docker.com/r/nandanksingh/module8_fastapi_calculator](https://hub.docker.com/r/nandanksingh/module8_fastapi_calculator)

### **Pull the Image**

```bash
docker pull nandanksingh/module8_fastapi_calculator:latest
```

### **Run the Container**

```bash
docker run -d -p 8000:8000 nandanksingh/module8_fastapi_calculator:latest
```

### **Verify Deployment**

* Web App → [http://localhost:8000](http://localhost:8000)
* Health Endpoint → [http://localhost:8000/health](http://localhost:8000/health)

---

## **Testing and Coverage**

The project includes **Unit**, **Integration**, and **E2E** tests.
All tests are executed automatically via **GitHub Actions**, ensuring a **minimum of 90% coverage**.

### **Test Commands**

```bash
# Run all tests with coverage
pytest -v --cov=app --cov=main --cov-report=term-missing --cov-fail-under=90

# Run only unit + integration tests
pytest -m "not e2e" --cov=app --cov=main

# Run only E2E tests (Playwright)
pytest -m "e2e" --headed -v
```

---

### **Coverage Summary**

| Category          | Coverage   |Status   |
| ----------------- | ---------- |-------- |
| Unit Tests        | 100%       |  Passed |
| Integration Tests | 100%       |  Passed |
| End-to-End Tests  | Functional |  Passed |

---

##  **Security Validation (Trivy Scan)**

The Docker image `fastapi-calculator:test` was scanned using **Trivy** to detect vulnerabilities in both the application and system layers.

### **Scan Command Used**

```bash
trivy image --ignorefile .trivyignore --show-suppressed fastapi-calculator:test
```

### **Results Summary**

* **Python packages:** 0 vulnerabilities (CRITICAL/HIGH/MEDIUM)
* **Suppressed CVEs:** Known, non-exploitable Starlette/h11 issues ignored via `.trivyignore`
* **System CVEs:** Found in Debian base image (kernel-related, non-exploitable)

### **Security Assurance**

The application runs as a **non-root user** in the container.
All known issues in the **FastAPI–Starlette–h11** dependency chain were reviewed and marked safe.
Remaining CVEs belong to the Debian base image and are **not exploitable** in this setup.

**Final Security Status:**  *No active high or critical vulnerabilities detected.*

---

## **CI/CD Pipeline Status**

All three stages in the GitHub Actions workflow passed successfully:

| Stage         | Result | Description                              |
| --------------| ------ | ---------------------------------------- |
|  **Test**     | Passed | Unit + Integration + E2E tests           |
|  **Security** | Passed | Trivy vulnerability scan                 |
|  **Deploy**   | Passed | Docker image built & pushed to DockerHub |

---

### **Deployment Confirmation**

After the CI/CD pipeline completed:

1. The Docker image was automatically pushed to DockerHub.
2. Deployment was verified by pulling the image and running it locally:

   ```bash
   docker pull nandanksingh/module8_fastapi_calculator:latest
   docker run -d -p 8000:8000 nandanksingh/module8_fastapi_calculator:latest
   ```
3. The `/health` endpoint returned:

   ```json
   {"status": "ok", "message": "FastAPI Calculator is running smoothly."}
   ```

**Final Verification:** Application, tests, and security scans all passed successfully.

---

## **CI/CD Status Badge**

Add this badge to your repository for visual pipeline status:

```markdown
![CI/CD](https://github.com/nandanksingh/IS601_Assignment8/actions/workflows/test.yml/badge.svg)
```

> Automated CI/CD pipeline includes Unit Testing, E2E Testing (Playwright),
> Trivy vulnerability scanning, and DockerHub deployment.

---

## **Technology Stack**

| Category         | Tools              |
| ---------------- | ------------------ |
| Language         | Python 3.12        |
| Framework        | FastAPI            |
| Testing          | Pytest, Playwright |
| CI/CD            | GitHub Actions     |
| Security         | Trivy              |
| Containerization | Docker             |
| Deployment       | Docker Hub         |
| Logging          | Python Logging     |
| Server           | Uvicorn            |

---

## **Reflection**

This project gave me hands-on experience with **modern DevOps workflows** — combining **testing, security scanning, and automated deployment** in one pipeline.
Building this calculator with FastAPI helped me understand **web APIs**, while integrating **Trivy and GitHub Actions** strengthened my knowledge of **secure software delivery**.

---

## **Conclusion**

The **FastAPI Calculator** is a secure, containerized, and fully automated application that demonstrates the real-world integration of **FastAPI**, **Pytest**, **Playwright**, **Trivy**, and **Docker** in a professional CI/CD pipeline.


