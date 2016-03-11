try:
    import asyncio
    PYTHON = 3
except ImportError:
    PYTHON = 2


LOOP = None


def coroutine(func):
    """
    This method wraps asyncio coroutines.
    """
    coro = func
    if not asyncio.iscoroutine(func):
        coro = asyncio.coroutine(func)
    return coro


def schedule(coro, *, loop=None):
    """
    This method schedule an awaitable to the asyncio loop. This wrapper aim to
    support backward compatibility with any verions of Python 3.
    """
    try:
        return asyncio.ensure_future(coro, loop=loop or LOOP)
    except AttributeError:
        # Before Python 3.4.4 version
        return asyncio.async(coro, loop=loop or LOOP)


def run(func):
    """
    Start a main method within an asyncio loop context (if available).
    """
    global LOOP

    if PYTHON >= 3:
        LOOP = asyncio.get_event_loop() or asyncio.new_event_loop()
        asyncio.set_event_loop(LOOP)

        coro = coroutine(func)
        LOOP.run_until_complete(coro())
        LOOP.close()
    else:
        func()
