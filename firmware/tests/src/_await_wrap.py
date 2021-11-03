import asyncio


def wrap_await(async_def):
    """Makes the function given as an argument a synchronous function."""
    return asyncio.get_event_loop().run_until_complete(async_def)
