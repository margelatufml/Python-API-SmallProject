from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import PowRequest, PowResponse, FibonacciRequest, FibonacciResponse, FactorialRequest, FactorialResponse, GcdRequest, GcdResponse, IsPrimeRequest, IsPrimeResponse
from .services import pow_func, fibonacci, factorial, gcd, is_prime
from .db import insert_operation, list_operations
from .utils import cache_get, cache_set, log_operation
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.responses import HTMLResponse

import os

# Token simplu pentru authorization
API_TOKEN = os.environ.get("API_TOKEN", "secret-token")
auth_scheme = HTTPBearer()

def authorize(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

app = FastAPI(title="Math Microservice")

# Monitoring Prometheus
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.post("/pow", response_model=PowResponse, dependencies=[Depends(authorize)])
def pow_endpoint(req: PowRequest):
    cache_key = ("pow", req.base, req.exponent)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = pow_func(req.base, req.exponent)
        cache_set(cache_key, result)
    insert_operation("pow", req.dict(), {"result": result})
    log_operation("pow", req.dict(), {"result": result})
    return PowResponse(result=result)

@app.post("/fibonacci", response_model=FibonacciResponse, dependencies=[Depends(authorize)])
def fibonacci_endpoint(req: FibonacciRequest):
    cache_key = ("fibonacci", req.n)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = fibonacci(req.n)
        cache_set(cache_key, result)
    insert_operation("fibonacci", req.dict(), {"result": result})
    log_operation("fibonacci", req.dict(), {"result": result})
    return FibonacciResponse(result=result)

@app.post("/factorial", response_model=FactorialResponse, dependencies=[Depends(authorize)])
def factorial_endpoint(req: FactorialRequest):
    cache_key = ("factorial", req.n)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = factorial(req.n)
        cache_set(cache_key, result)
    insert_operation("factorial", req.dict(), {"result": result})
    log_operation("factorial", req.dict(), {"result": result})
    return FactorialResponse(result=result)

@app.post("/gcd", response_model=GcdResponse, dependencies=[Depends(authorize)])
def gcd_endpoint(req: GcdRequest):
    cache_key = ("gcd", req.a, req.b)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = gcd(req.a, req.b)
        cache_set(cache_key, result)
    insert_operation("gcd", req.dict(), {"result": result})
    log_operation("gcd", req.dict(), {"result": result})
    return GcdResponse(result=result)

@app.post("/is_prime", response_model=IsPrimeResponse, dependencies=[Depends(authorize)])
def is_prime_endpoint(req: IsPrimeRequest):
    cache_key = ("is_prime", req.n)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = is_prime(req.n)
        cache_set(cache_key, result)
    insert_operation("is_prime", req.dict(), {"result": result})
    log_operation("is_prime", req.dict(), {"result": result})
    return IsPrimeResponse(result=result)

@app.get("/history", dependencies=[Depends(authorize)])
def history():
    return [rec.dict() for rec in list_operations()]

@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <head><title>Math Microservice UI</title></head>
    <body>
    <h1>Math Microservice UI</h1>
    <form method='post' action='/ui' style='margin-bottom:2em;'>
      <label>Operation:
        <select name='op'>
          <option value='pow'>pow</option>
          <option value='fibonacci'>fibonacci</option>
          <option value='factorial'>factorial</option>
          <option value='gcd'>gcd</option>
          <option value='is_prime'>is_prime</option>
        </select>
      </label><br><br>
      <label>Base/A/N: <input name='a' type='number' step='any'></label><br>
      <label>Exponent/B: <input name='b' type='number' step='any'></label><br>
      <input type='submit' value='Compute'>
    </form>
    <div id='result'>{{result}}</div>
    </body></html>
    """

@app.post("/ui", response_class=HTMLResponse)
async def ui_post(request: Request):
    form = await request.form()
    op = form.get('op')
    a = form.get('a')
    b = form.get('b')
    token = "secret-token"
    headers = {"Authorization": f"Bearer {token}"}
    import httpx
    url = "http://localhost:8000"
    data = {}
    endpoint = ""
    if op == "pow":
        endpoint = "/pow"
        data = {"base": float(a), "exponent": float(b)}
    elif op == "fibonacci":
        endpoint = "/fibonacci"
        data = {"n": int(a)}
    elif op == "factorial":
        endpoint = "/factorial"
        data = {"n": int(a)}
    elif op == "gcd":
        endpoint = "/gcd"
        data = {"a": int(a), "b": int(b)}
    elif op == "is_prime":
        endpoint = "/is_prime"
        data = {"n": int(a)}
    else:
        return HTMLResponse("<b>Invalid operation</b>")
    try:
        r = httpx.post(url + endpoint, json=data, headers=headers, timeout=5)
        result = r.json()
    except Exception as e:
        result = {"error": str(e)}
    html = f"""
    <html><head><title>Math Microservice UI</title></head><body>
    <h1>Math Microservice UI</h1>
    <form method='post' action='/ui' style='margin-bottom:2em;'>
      <label>Operation:
        <select name='op'>
          <option value='pow' {'selected' if op=='pow' else ''}>pow</option>
          <option value='fibonacci' {'selected' if op=='fibonacci' else ''}>fibonacci</option>
          <option value='factorial' {'selected' if op=='factorial' else ''}>factorial</option>
          <option value='gcd' {'selected' if op=='gcd' else ''}>gcd</option>
          <option value='is_prime' {'selected' if op=='is_prime' else ''}>is_prime</option>
        </select>
      </label><br><br>
      <label>Base/A/N: <input name='a' type='number' step='any' value='{a}'></label><br>
      <label>Exponent/B: <input name='b' type='number' step='any' value='{b}'></label><br>
      <input type='submit' value='Compute'>
    </form>
    <div id='result'><b>Result:</b> {result}</div>
    </body></html>
    """
    return HTMLResponse(html)
