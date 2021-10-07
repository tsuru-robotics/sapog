import asyncio
import os
import pathlib
import sys

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo

internal_table = {}


async def main() -> None:
    os.environ["UAVCAN__CAN__IFACE"] = "socketcan:slcan0"
    os.environ["UAVCAN__CAN__MTU"] = "8"
    os.environ["UAVCAN__NODE__ID"] = "42"
    with make_node(NodeInfo(name="com.zubax.sapog.tests.node1"), "databases/node1.db") as node:
        allocate_responder = node.make_publisher(uavcan.pnp.NodeIDAllocationData_1_0)
        allocate_subscription = node.make_subscriber(uavcan.pnp.NodeIDAllocationData_1_0)
        async for m, _metadata in allocate_subscription:
            print("Allocator received a request for an new NodeID allocation.")
            assert isinstance(m, uavcan.pnp.NodeIDAllocationData_1_0)
            their_unique_id = m.unique_id_hash
            if (their_node_id := internal_table.get(their_unique_id)) is None:
                new_id = uavcan.node.ID_1_0()
                new_id.value = 21
                response = uavcan.pnp.NodeIDAllocationData_1_0(m.unique_id_hash, [new_id])
                await allocate_responder.publish(response)
            else:
                print(f"NodeID {their_node_id} requested another NodeID, one is enough!")
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
