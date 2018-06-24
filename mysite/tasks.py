# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .celeryconf import app

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@app.task
def power(n):
    """Return 2 to the n'th power"""
    return 2 ** n


@app.task
def fib(n):
    """Return the n'th Fibonacci number.
    """
    if n < 0:
        raise ValueError("Fibonacci numbers are only defined for n >= 0.")
    return _fib(n)


def _fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return _fib(n - 1) + _fib(n - 2)

# mapping from names to tasks

TASK_MAPPING = {
    'power': power,
    'fibonacci': fib
}

@app.task
def add(x, y):
    return x + y

