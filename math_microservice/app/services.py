
# Async/multithreading worker support
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

def pow_func_sync(base: float, exponent: float) -> float:
    return base ** exponent

def fibonacci_sync(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def factorial_sync(n: int) -> int:
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def gcd_sync(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

def is_prime_sync(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Async wrappers
async def pow_func(base: float, exponent: float) -> float:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, pow_func_sync, base, exponent)

async def fibonacci(n: int) -> int:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, fibonacci_sync, n)

async def factorial(n: int) -> int:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, factorial_sync, n)

async def gcd(a: int, b: int) -> int:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, gcd_sync, a, b)

async def is_prime(n: int) -> bool:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, is_prime_sync, n)
