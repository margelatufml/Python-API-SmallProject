import pytest
import asyncio
from app.services import pow_func, fibonacci, factorial, gcd, is_prime

def test_pow_func():
    assert asyncio.run(pow_func(2, 3)) == 8
    assert asyncio.run(pow_func(5, 0)) == 1
    assert asyncio.run(pow_func(9, 0.5)) == 3

def test_fibonacci():
    assert asyncio.run(fibonacci(0)) == 0
    assert asyncio.run(fibonacci(1)) == 1
    assert asyncio.run(fibonacci(5)) == 5
    assert asyncio.run(fibonacci(10)) == 55

def test_factorial():
    assert asyncio.run(factorial(0)) == 1
    assert asyncio.run(factorial(1)) == 1
    assert asyncio.run(factorial(5)) == 120
    assert asyncio.run(factorial(7)) == 5040

def test_gcd():
    assert asyncio.run(gcd(54, 24)) == 6
    assert asyncio.run(gcd(0, 5)) == 5
    assert asyncio.run(gcd(7, 0)) == 7
    assert asyncio.run(gcd(-8, 12)) == 4

def test_is_prime():
    assert asyncio.run(is_prime(2)) is True
    assert asyncio.run(is_prime(3)) is True
    assert asyncio.run(is_prime(4)) is False
    assert asyncio.run(is_prime(17)) is True
    assert asyncio.run(is_prime(1)) is False
    assert asyncio.run(is_prime(0)) is False
