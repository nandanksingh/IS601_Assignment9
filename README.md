# **Assignment 9 – Working with Raw SQL in pgAdmin**

**Author:** Nandan Kumar
**Date:** November 3, 2025

---

## **Project Overview**

This assignment extends my earlier **FastAPI Calculator** into a full-stack, database-driven web application powered by **PostgreSQL** and **pgAdmin**, all containerized using **Docker Compose**.

The goal was to explore how real-world web applications connect to and manipulate databases using **raw SQL commands** instead of ORM abstractions.

The multi-service environment includes:

* **FastAPI** – Application backend
* **PostgreSQL** – Relational database
* **pgAdmin 4** – Browser-based DB management tool

This setup mirrors professional DevOps workflows and ensures isolation, portability, and reproducibility.

---

## **Environment Setup**

### **Docker Compose Services**

| Service     | Description                 | Port |
| :---------- | :-------------------------- | :--- |
| **web**     | FastAPI backend application | 8000 |
| **db**      | PostgreSQL database         | 5432 |
| **pgadmin** | GUI for managing PostgreSQL | 5050 |

**Run the stack:**

```bash
docker-compose up --build
```

**Access points:**

* [http://localhost:8000](http://localhost:8000) → FastAPI
* [http://localhost:5050](http://localhost:5050) → pgAdmin

**Stop the stack:**

```bash
docker-compose down
```

---

## **Docker Image Details**

After successful testing, the complete image was built and tagged as:

```bash
docker build -t nandanksingh/module9_sql_pgadmin:pgSQL_1 .
```

**Docker Hub Repository:**
[https://hub.docker.com/r/nandanksingh/module9_sql_pgadmin](https://hub.docker.com/r/nandanksingh/module9_sql_pgadmin)

This image contains the entire FastAPI + PostgreSQL + pgAdmin environment and can be reused for future experiments.

---

## **Database Configuration**

**pgAdmin Login**

* Email → `admin@example.com`
* Password → `admin`

**Database Connection**

* Host → `db`
* User → `postgres`
* Password → `postgres`
* Database → `fastapi_db`

Once connected, I opened **Query Tool** in pgAdmin to execute all SQL commands step by step.

---

## **SQL Operations**

All commands are also saved in **`database_operations.sql`** for reference.

---

### **(A) Create Tables**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE calculations (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(20) NOT NULL,
    operand_a FLOAT NOT NULL,
    operand_b FLOAT NOT NULL,
    result FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Explanation:**
Defines two related tables — `users` and `calculations`.
Each user can have many calculations (**one-to-many relationship**).
Cascade delete ensures data integrity when a user is removed.

---

### **(B) Insert Records**

```sql
INSERT INTO users (username, email)
VALUES ('alice', 'alice@example.com'),
       ('bob', 'bob@example.com');

INSERT INTO calculations (operation, operand_a, operand_b, result, user_id)
VALUES ('add', 2, 3, 5, 1),
       ('divide', 10, 2, 5, 1),
       ('multiply', 4, 5, 20, 2);
```

**Explanation:**
Populates both tables with test data to verify the relational link between users and their operations.

---

### **(C) Query Data**

```sql
-- Retrieve all users
SELECT * FROM users;

-- Retrieve all calculations
SELECT * FROM calculations;

-- Join users and calculations
SELECT u.username, c.operation, c.operand_a, c.operand_b, c.result
FROM calculations c
JOIN users u ON c.user_id = u.id;
```

**Explanation:**
The JOIN query displays which user performed which operation, confirming proper foreign-key relationships.

---

### **(D) Update a Record**

```sql
UPDATE calculations
SET result = 6
WHERE id = 1;
```

**Explanation:**
Corrects a stored result, proving the ability to modify data accurately.

---

### **(E) Delete a Record**

```sql
DELETE FROM calculations
WHERE id = 2;
```

**Explanation:**
Removes a specific record while preserving overall table integrity.

---

##  **Results and Verification**

All SQL commands executed successfully in pgAdmin with confirmation messages such as:

```
Query returned successfully: 1 row affected
```

Screenshots were captured for each operation — creation, insertion, querying, update, and deletion — to document the process.

---

##  **Container Health Verification**

| Container       |Status    | Purpose                          |
| :-------------- |:---------| :------------------------------- |
| **fastapi_app** |  Healthy | Served FastAPI endpoints on 8000 |
| **postgres_db** |  Healthy | Stored user and calculation data |
| **pgadmin**     |  Running | Provided GUI on port 5050        |

Logs confirmed continuous successful health-check pings and container connectivity.

---

##  **Reflection**

This assignment gave me hands-on experience integrating web applications with relational databases inside a containerized setup.

Using **Docker Compose** made managing multiple services effortless — one command spun up an entire environment.
Working directly with **raw SQL** improved my understanding of how data is structured, related, and manipulated at its core.

Initially, I encountered small issues such as port conflicts and connection settings, but fixing them strengthened my understanding of Docker networking and pgAdmin configuration.

This experience built a strong foundation for upcoming topics like **ORM frameworks**, **database migrations**, and **query optimization**, helping me think like a data-driven backend developer.

---

##  **Conclusion**

The project demonstrates how **FastAPI**, **PostgreSQL**, and **pgAdmin** can operate seamlessly in a containerized ecosystem.
By completing all five fundamental SQL operations — **CREATE**, **INSERT**, **SELECT**, **UPDATE**, and **DELETE** — I achieved full end-to-end data management.

This module bridged theory and practice, giving me a complete view of backend application design using modern DevOps tools.

---

##  **Final Docker Image**

| Repository                                                                                        | Tag       | Description                                   |
| :------------------------------------------------------------------------------------------------ | :-------- | :-------------------------------------------- |
| **[nandanksingh/module9_sql_pgadmin](https://hub.docker.com/r/nandanksingh/module9_sql_pgadmin)** | `pgSQL_1` | Contains FastAPI + PostgreSQL + pgAdmin stack |

**Pull and run:**

```bash
docker pull nandanksingh/module9_sql_pgadmin:pgSQL_1
docker run -d -p 8000:8000 nandanksingh/module9_sql_pgadmin:pgSQL_1
```

---

## **Quick Start for Reviewers**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/nandanksingh/IS601_Assignment9.git
   cd IS601_Assignment9
   ```
2. **Start Containers**

   ```bash
   docker-compose up --build
   ```
3. **Access the Apps**

   * FastAPI → [http://localhost:8000](http://localhost:8000)
   * pgAdmin → [http://localhost:5050](http://localhost:5050)
4. **Login to pgAdmin**

   * Email: `admin@example.com`
   * Password: `admin`
5. **Connect to Server `db`**

   * Database: `fastapi_db`
6. **Open Query Tool** and run SQL from `database_operations.sql`.

---

##  **Technology Stack**

| Category                 | Tools / Frameworks     |
| :----------------------- | :--------------------- |
| **Programming Language** | Python 3.12            |
| **Web Framework**        | FastAPI                |
| **Database**             | PostgreSQL 15          |
| **DB Management**        | pgAdmin 4              |
| **Testing**              | Pytest, Playwright     |
| **Containerization**     | Docker, Docker Compose |
| **CI/CD**                | GitHub Actions         |
| **Image Tag**            | `pgSQL_1`              |

---

**This project combines software engineering and data-management principles — turning abstract SQL concepts into a practical, containerized backend system ready for professional development environments.**

---
