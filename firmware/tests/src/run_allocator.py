import asyncio
from time import sleep
from _await_wrap import wrap_await
from allocator import make_allocator


async def main():
    packed = await make_allocator("1")

    while True:
        await asyncio.sleep(0.04)
    node.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
