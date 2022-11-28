import asyncio
import functools
import time
from typing import Callable, Any


async def sleep_func(sleep_seconds: int) -> int:
    print(f"Сплю {sleep_seconds}cek.")
    await asyncio.sleep(sleep_seconds)  # Приостановить sleep_func на sleep_seconds
    print(f"Спал {sleep_seconds}cek.")
    return sleep_seconds


def async_timer():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'выполняется {func} с аргументами {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func} завершилась за {total:.4f} с')

        return wrapped

    return wrapper
