import pytest
from app.services import pow_func, fibonacci, factorial, gcd, is_prime

def test_pow_func():
    assert pow_func(2, 3) == 8
    assert pow_func(5, 0) == 1
    assert pow_func(9, 0.5) == 3

def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(5) == 5
    assert fibonacci(10) == 55

def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(7) == 5040

def test_gcd():
    assert gcd(54, 24) == 6
    assert gcd(0, 5) == 5
    assert gcd(7, 0) == 7
    assert gcd(-8, 12) == 4

def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(17) is True
    assert is_prime(1) is False
    assert is_prime(0) is False
