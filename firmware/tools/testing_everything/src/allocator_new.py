import asyncio
import os
import pathlib
import sys
from typing import Optional

from pyuavcan.application.node_tracker import Entry

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo, node_tracker
from pyuavcan.application.plug_and_play import Allocator





async def main() -> None:
    os.environ["UAVCAN__CAN__IFACE"] = "socketcan:slcan0"
    os.environ["UAVCAN__CAN__MTU"] = "8"
    os.environ["UAVCAN__NODE__ID"] = "42"
    with make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), "databases/node1.db") as node:
        t = node_tracker()
        a = Allocator()

        def handle_getinfo_update(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
            a.register_node(node_id)
        t.add_update_handler(handle_getinfo_update)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
