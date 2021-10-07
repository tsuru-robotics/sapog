# This node exists to request a NodeID from allocator_node.py
import asyncio
import os
import pathlib
import sys

import uavcan.pnp.NodeIDAllocationData_1_0

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo
from random import random, seed
import pyuavcan
import datetime
import uavcan.si.unit.temperature.Scalar_1_0

was_timer_restarted = False


async def handle_received_allocation(msg: uavcan.pnp.NodeIDAllocationData_1_0,
                                     sender: pyuavcan.transport.TransferFrom) -> None:
    global was_timer_restarted
    node_id = msg.allocated_node_id[0]
    print(f"Node2 has received an allocation {node_id}.")
    os.environ["UAVCAN__NODE__ID"] = str(node_id)


async def main() -> None:
    global was_timer_restarted
    os.environ["UAVCAN__CAN__IFACE"] = "socketcan:slcan0"
    os.environ["UAVCAN__CAN__MTU"] = "8"
    os.environ["UAVCAN__NODE__ID"] = "0"

    seed(datetime.datetime.now())

    with make_node(NodeInfo(name="com.zubax.sapog.tests.node1"), "databases/node1.db") as node:
        allocate_subscriber = node.make_subscriber(uavcan.pnp.NodeIDAllocationData_1_0)
        allocate_subscriber.receive_in_background(handle_received_allocation)
        allocate_request = node.make_publisher(uavcan.pnp.NodeIDAllocationData_1_0)
        was_timer_restarted = False
        while os.environ["UAVCAN__NODE__ID"] == "0":
            await asyncio.sleep(random() * 2)
            if was_timer_restarted:
                was_timer_restarted = False
                continue
            request = uavcan.pnp.NodeIDAllocationData_1_0(os.getpid() % 100)
            await allocate_request.publish(request)
        print("I have received my NodeID")
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
