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


def get_5_numbers():
    return 1, 1, 2, 1, 3, 1, 30, 30, 30


def slow_1(a, s):
    return slow_1(a, s)


def slow_2(b, s):
    return slow_1(b, s)


def slow_3(c, s):
    return slow_1(c, s)


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
        print(u)
    print('some error')
