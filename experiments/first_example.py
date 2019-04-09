import logging
from time import sleep


log = logging.getLogger(__name__)


def slow_identity(n, seconds=2):
    sleep(seconds)
    return n


def fib(n):
    """
    Very slow function:
    for n=30 ~ 0.5 sec
    for n=31 ~ 1 sec
    for n=32 ~ 1.5 sec
    """
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def get_5_numbers(name):
    log.debug('run get_5_numbers')
    result = tuple(map(int, name.split()))
    if len(result) == 5:
        return result
    raise ValueError


def slow_1(a, s):
    log.debug('run slow_1')
    return slow_identity(a, s)


def slow_2(b, s):
    log.debug('run slow_2')
    return slow_identity(b, s)


def slow_3(c, s):
    log.debug('run slow_3')
    return slow_identity(c, s)


def get_sum(a1, b1, c1):
    log.debug('run get_sum')
    return a1 + b1 + c1


def fib_1(n):
    log.debug('run fib_1')
    return fib(n)


def fib_2(n):
    log.debug('run fib_2')
    return fib(n)


def fib_3(n):
    log.debug('run fib_3')
    return fib(n)


def check(x, y, z):
    log.debug('run check')
    return len({x, y, z}) == 1


def get_result(u, v):
    log.debug('run get_result')
    if v:
        return u
    raise ValueError
