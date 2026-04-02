# Math Microservice API

A RESTful microservice for mathematical operations, built with clean architecture patterns in Python.

## Tech Stack

- **Language:** Python
- **Architecture:** Microservice with layered structure
- **Database:** SQLite
- **Testing:** Unit tests with pytest
- **Code Quality:** Flake8 linting, Dockerfile for containerization

## Project Structure

```
├── app/              # Application source code
├── tests/            # Unit and integration tests
├── Dockerfile        # Container configuration
├── requirements.txt  # Python dependencies
└── .flake8          # Linting configuration
```

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
python -m app

# Run tests
pytest tests/ -v
```

## Docker

```bash
docker build -t math-microservice .
docker run -p 8000:8000 math-microservice
```

