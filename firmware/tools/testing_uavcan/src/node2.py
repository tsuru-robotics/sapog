import asyncio
import os
import pathlib
import sys

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo


async def main() -> None:
    os.environ["UAVCAN__NODE__ID"] = "43"
    os.environ["UAVCAN__UDP__IFACE"] = "127.0.0.1"
    with make_node(NodeInfo(name="com.zubax.sapog.tests.node1"), "databases/node1.db") as node:
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
