#!/usr/bin/env python3
"""Write a coroutine called async_generator that takes no arguments.

The coroutine will loop 10 times, each time asynchronously wait 1
second, then yield a random number between 0 and 10. Use the random module.

The return type of generator functions can be annotated by the
generic type Generator[yield_type, send_type, return_type] provided
by typing.py module
"""

import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """Async generator that yields random numbers between 0 and 10."""
    for digit in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
