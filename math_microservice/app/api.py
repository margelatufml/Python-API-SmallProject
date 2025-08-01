from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import PowRequest, PowResponse, FibonacciRequest, FibonacciResponse, FactorialRequest, FactorialResponse, GcdRequest, GcdResponse, IsPrimeRequest, IsPrimeResponse, UserCreate, UserLogin
from .services import pow_func, fibonacci, factorial, gcd, is_prime
from .db import insert_operation, list_operations, create_user, verify_user, get_user_role
from .utils import cache_get, cache_set, log_operation
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi.responses import HTMLResponse
import json

import os


# Advanced authentication/authorization
auth_scheme = HTTPBearer()

def authorize(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme), required_role: str = "user"):
    token = credentials.credentials
    # Token format: username:password
    try:
        username, password = token.split(":", 1)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token format")
    valid, role = verify_user(username, password)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if required_role and role != required_role and role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return username


app = FastAPI(title="Math Microservice")

# Monitoring Prometheus
# Monitoring Prometheus
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
# API endpoints

# User registration
@app.post("/register")
def register(user: UserCreate):
    try:
        create_user(user.username, user.password, user.role)
        return {"message": "User registered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# User login (returns token)
@app.post("/login")
def login(user: UserLogin):
    valid, role = verify_user(user.username, user.password)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Token is username:password (for demo, not secure for prod)
    return {"token": f"{user.username}:{user.password}", "role": role}

@app.post("/pow", response_model=PowResponse)
async def pow_endpoint(req: PowRequest, username: str = Depends(lambda cred=Depends(auth_scheme): authorize(cred, "user"))):
    cache_key = ("pow", req.base, req.exponent)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = await pow_func(req.base, req.exponent)
        cache_set(cache_key, result)
    insert_operation("pow", req.dict(), {"result": result})
    log_operation("pow", req.dict(), {"result": result})
    return PowResponse(result=result)

@app.post("/fibonacci", response_model=FibonacciResponse)
async def fibonacci_endpoint(req: FibonacciRequest, username: str = Depends(lambda cred=Depends(auth_scheme): authorize(cred, "user"))):
    cache_key = ("fibonacci", req.n)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = await fibonacci(req.n)
        cache_set(cache_key, result)
    insert_operation("fibonacci", req.dict(), {"result": result})
    log_operation("fibonacci", req.dict(), {"result": result})
    return FibonacciResponse(result=result)

@app.post("/factorial", response_model=FactorialResponse)
async def factorial_endpoint(req: FactorialRequest, username: str = Depends(lambda cred=Depends(auth_scheme): authorize(cred, "user"))):
    cache_key = ("factorial", req.n)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = await factorial(req.n)
        cache_set(cache_key, result)
    insert_operation("factorial", req.dict(), {"result": result})
    log_operation("factorial", req.dict(), {"result": result})
    return FactorialResponse(result=result)

@app.post("/gcd", response_model=GcdResponse)
async def gcd_endpoint(req: GcdRequest, username: str = Depends(lambda cred=Depends(auth_scheme): authorize(cred, "user"))):
    cache_key = ("gcd", req.a, req.b)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = await gcd(req.a, req.b)
        cache_set(cache_key, result)
    insert_operation("gcd", req.dict(), {"result": result})
    log_operation("gcd", req.dict(), {"result": result})
    return GcdResponse(result=result)

@app.post("/is_prime", response_model=IsPrimeResponse)
async def is_prime_endpoint(req: IsPrimeRequest, username: str = Depends(lambda cred=Depends(auth_scheme): authorize(cred, "user"))):
    cache_key = ("is_prime", req.n)
    cached = cache_get(cache_key)
    if cached is not None:
        result = cached
    else:
        result = await is_prime(req.n)
        cache_set(cache_key, result)
    insert_operation("is_prime", req.dict(), {"result": result})
    log_operation("is_prime", req.dict(), {"result": result})
    return IsPrimeResponse(result=result)

@app.get("/history")
def history(username: str = Depends(lambda cred=Depends(auth_scheme): authorize(cred, "admin"))):
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
      <label>Username: <input name='username' type='text'></label><br>
      <label>Password: <input name='password' type='password'></label><br>
      <input type='submit' value='Compute'>
    </form>
    <form method='post' action='/ui_register' style='margin-bottom:2em;'>
      <h3>Register</h3>
      <label>Username: <input name='username' type='text'></label>
      <label>Password: <input name='password' type='password'></label>
      <input type='submit' value='Register'>
    </form>
    <form method='post' action='/ui_history'>
      <input type='submit' value='Show History (admin only)'>
    </form>
    <a href='/metrics' target='_blank'>Prometheus Metrics</a>
    <div id='result'>{{result}}</div>
    </body></html>
    """

@app.post("/ui", response_class=HTMLResponse)
async def ui_post(request: Request):
    form = await request.form()
    op = form.get('op')
    a = form.get('a')
    b = form.get('b')
    username = form.get('username')
    password = form.get('password')
    token = f"{username}:{password}" if username and password else ""
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
      <label>Username: <input name='username' type='text' value='{username if username else ''}'></label><br>
      <label>Password: <input name='password' type='password' value='{password if password else ''}'></label><br>
      <input type='submit' value='Compute'>
    </form>
    <form method='post' action='/ui_register' style='margin-bottom:2em;'>
      <h3>Register</h3>
      <label>Username: <input name='username' type='text'></label>
      <label>Password: <input name='password' type='password'></label>
      <input type='submit' value='Register'>
    </form>
    <form method='post' action='/ui_history'>
      <input type='submit' value='Show History (admin only)'>
    </form>
    <a href='/metrics' target='_blank'>Prometheus Metrics</a>
    <div id='result'><b>Result:</b> {result}</div>
    </body></html>
    """
    return HTMLResponse(html)

# Register UI endpoint
@app.post("/ui_register", response_class=HTMLResponse)
async def ui_register(request: Request):
    form = await request.form()
    username = form.get('username')
    password = form.get('password')
    import httpx
    url = "http://localhost:8000/register"
    try:
        r = httpx.post(url, json={"username": username, "password": password, "role": "user"}, timeout=5)
        result = r.json()
    except Exception as e:
        result = {"error": str(e)}
    html = f"""
    <html><head><title>Register</title></head><body>
    <h1>Register</h1>
    <form method='post' action='/ui_register'>
      <label>Username: <input name='username' type='text' value='{username}'></label>
      <label>Password: <input name='password' type='password' value='{password}'></label>
      <input type='submit' value='Register'>
    </form>
    <div id='result'><b>Result:</b> {result}</div>
    <a href='/ui'>Back to UI</a>
    </body></html>
    """
    return HTMLResponse(html)

# History UI endpoint
@app.post("/ui_history", response_class=HTMLResponse)
async def ui_history(request: Request):
    # For demo, use admin:admin
    token = "admin:admin"
    headers = {"Authorization": f"Bearer {token}"}
    import httpx
    url = "http://localhost:8000/history"
    try:
        r = httpx.get(url, headers=headers, timeout=5)
        result = r.json()
    except Exception as e:
        result = {"error": str(e)}
    html = f"""
    <html><head><title>History</title></head><body>
    <h1>Operation History (admin only)</h1>
    <pre>{json.dumps(result, indent=2)}</pre>
    <a href='/ui'>Back to UI</a>
    </body></html>
    """
    return HTMLResponse(html)
