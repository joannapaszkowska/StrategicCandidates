from numba import jit

USE_NUMBA = True


def set_numba(numba):
    global USE_NUMBA
    USE_NUMBA = numba


def conditional_jit():
    def decorator(func):
        if not USE_NUMBA:
            return func
        return jit(nopython=True)(func)
    return decorator
