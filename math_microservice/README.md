# Math Microservice

A Python microservice for math operations (power, Fibonacci, factorial, GCD, prime check) with REST API, CLI, async workers, advanced logging, authentication, and flexible persistence.

## Features

- **Math API:** Endpoints for pow, fibonacci, factorial, gcd, is_prime
- **Async workers:** Fast, non-blocking calculations
- **Caching:** In-memory cache for repeated requests
- **Logging:** Streaming log system with queue and file output
- **Authentication:** User registration, login, and role-based access (admin/user)
- **Persistence:** Choose SQLite, in-memory, or file-based storage
- **Monitoring:** Prometheus metrics at `/metrics`
- **CLI:** Command line interface for all operations
- **UI:** Simple web interface for API, registration, and history
- **Docker:** Containerized for easy deployment

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API server

```bash
uvicorn math_microservice.app.api:app --reload
```

### 3. Use the CLI

```bash
python -m math_microservice.app.cli pow --base 2 --exponent 8
python -m math_microservice.app.cli fibonacci --n 10
python -m math_microservice.app.cli factorial --n 5
```

### 4. Register and login (API)

- Register: `POST /register` with `{"username": "yourname", "password": "yourpass"}`
- Login: `POST /login` with `{"username": "yourname", "password": "yourpass"}`
- Use token `username:password` as Bearer for all requests

### 5. Change persistence mode

Set environment variable `PERSISTENCE_MODE` to `sqlite`, `memory`, or `file` before running.

### 6. Run with Docker

```bash
docker build -t math-microservice .
docker run -e PERSISTENCE_MODE=sqlite -p 8000:8000 math-microservice
```

### 7. Access the UI

Open [http://localhost:8000/ui](http://localhost:8000/ui) in your browser.

### 8. Monitoring

Visit [http://localhost:8000/metrics](http://localhost:8000/metrics) for Prometheus metrics.

### 9. Run tests

```bash
pytest
```

## Directory Overview

- `app/` - Main code for API, CLI, logic, models, database, and utilities
- `tests/` - Unit tests for all features
- `requirements.txt` - List of needed Python packages
- `Dockerfile` - Instructions to build and run the project in a container
- `math_microservice.db` - SQLite database file (if using sqlite mode)
- `math_microservice.log` - Log file for all operations

---

This project is easy to use, extend, and run for anyone who needs math operations as a service.
