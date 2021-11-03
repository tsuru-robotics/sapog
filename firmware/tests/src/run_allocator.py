import asyncio
from time import sleep
from _await_wrap import wrap_await
from allocator import make_allocator

if __name__ == "__main__":
    packed = wrap_await(make_allocator("1"))
    node = packed.node
    allocator = packed.centralized_allocator
    tracker = packed.tracker
    while True:
        sleep(1)
    node.close()
