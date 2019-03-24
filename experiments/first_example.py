from time import sleep


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
    if name == 'first_example':
        return 1, 2, 3, 2, 31
    raise ValueError


def slow_1(a, s):
    return slow_identity(a, s)


def slow_2(b, s):
    return slow_identity(b, s)


def slow_3(c, s):
    return slow_identity(c, s)


def get_sum(a1, b1, c1):
    return a1 + b1 + c1


def fib_1(n):
    return fib(n)


def fib_2(n):
    return fib(n)


def fib_3(n):
    return fib(n)


def check(x, y, z):
    return len({x, y, z}) == 1


def get_result(u, v):
    if v:
        return u
    raise ValueError
