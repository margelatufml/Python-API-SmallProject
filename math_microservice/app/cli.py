import click
from .services import pow_func, fibonacci, factorial
from .db import insert_operation, list_operations
from .utils import log_operation

@click.group()
def cli():
    """Math Microservice CLI"""
    pass

@cli.command()
@click.option('--base', type=float, required=True, help='Baza pentru pow')
@click.option('--exponent', type=float, required=True, help='Exponentul pentru pow')
def pow(base, exponent):
    result = pow_func(base, exponent)
    insert_operation('pow', {'base': base, 'exponent': exponent}, {'result': result})
    log_operation('pow', {'base': base, 'exponent': exponent}, {'result': result})
    click.echo(f"Rezultat: {result}")

@cli.command()
@click.option('--n', type=int, required=True, help='Indexul pentru fibonacci (>=0)')
def fibonacci_cmd(n):
    result = fibonacci(n)
    insert_operation('fibonacci', {'n': n}, {'result': result})
    log_operation('fibonacci', {'n': n}, {'result': result})
    click.echo(f"Rezultat: {result}")

@cli.command()
@click.option('--n', type=int, required=True, help='Numărul pentru factorial (>=0)')
def factorial_cmd(n):
    result = factorial(n)
    insert_operation('factorial', {'n': n}, {'result': result})
    log_operation('factorial', {'n': n}, {'result': result})
    click.echo(f"Rezultat: {result}")

@cli.command()
def history():
    for rec in list_operations():
        click.echo(f"[{rec.timestamp}] {rec.operation} {rec.input_data} = {rec.result}")

if __name__ == "__main__":
    cli()
