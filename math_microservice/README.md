# Math Microservice

Un microserviciu Python pentru operații matematice (pow, fibonacci, factorial), cu API REST și CLI, persistare SQLite, validare Pydantic, caching in-memory, monitoring Prometheus, authorization și logging.

## Structură proiect

- `app/` - codul sursă principal
- `tests/` - teste unitare
- `requirements.txt` - dependențe
- `.flake8` - configurare linting
- `Dockerfile` - rulare containerizată

## Instalare

```bash
pip install -r requirements.txt
```

## Utilizare

### API
```bash
uvicorn math_microservice.app.api:app --reload
```

### CLI
```bash
python -m math_microservice.app.cli pow --base 2 --exponent 8
python -m math_microservice.app.cli fibonacci --n 10
python -m math_microservice.app.cli factorial --n 5
```

### Authorization
Toate endpoint-urile REST necesită un token Bearer (default: `secret-token`).
Adaugă header-ul:
```
Authorization: Bearer secret-token
```
Poți schimba tokenul cu variabila de mediu `API_TOKEN`.

### Monitoring
Endpoint Prometheus la `/metrics` (ex: http://localhost:8000/metrics)

### Logging
Toate operațiile sunt logate în fișierul `math_microservice.log` (simulare streaming/log centralizat).

### Docker
```bash
docker build -t math-microservice .
docker run -e API_TOKEN=secret-token -p 8000:8000 math-microservice
```

## Testare
```bash
pytest
```
