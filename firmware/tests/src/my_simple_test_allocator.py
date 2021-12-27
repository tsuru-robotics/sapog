import pathlib
import sys

import pyuavcan

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
from _await_wrap import wrap_await
from utils import get_interfaces_by_hw_id

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo, register


def make_simple_node_allocator():
    internal_table = {}

    def allocate_nr_of_nodes(nr: int, continuous: bool = False):
        allocated_nodes = {}
        for device, interfaces in get_interfaces_by_hw_id():
            allocated_hw_ids = []
            allocation_counter = 0
            registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
            registry01["uavcan.can.iface"] = " ".join(interfaces)
            registry01["uavcan.can.mtu"] = 8
            registry01["uavcan.node.id"] = 6
            with make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), registry01) as node:
                allocate_responder = node.make_publisher(uavcan.pnp.NodeIDAllocationData_1_0)
                allocate_subscription = node.make_subscriber(uavcan.pnp.NodeIDAllocationData_1_0)

                def allocate_one_node(msg, _):
                    nonlocal allocation_counter
                    if msg.unique_id_hash in allocated_hw_ids:
                        return None
                    assert isinstance(msg, uavcan.pnp.NodeIDAllocationData_1_0)
                    their_unique_id = msg.unique_id_hash
                    if (their_node_id := internal_table.get(their_unique_id)) is not None:
                        print(f"NodeID {their_node_id} requested another NodeID, one is enough!")
                        return
                    # else:
                    assigned_node_id = 21 + allocation_counter
                    new_id = uavcan.node.ID_1_0(assigned_node_id)
                    response = uavcan.pnp.NodeIDAllocationData_1_0(msg.unique_id_hash, [new_id])
                    allocated_nodes[assigned_node_id] = str(msg.unique_id_hash)
                    allocated_hw_ids.append(str(msg.unique_id_hash))
                    allocation_counter += 1
                    wrap_await(allocate_responder.publish(response))

                if continuous:
                    while True:
                        message, metadata = wrap_await(allocate_subscription.receive_for(1.3))
                        allocate_one_node(message, metadata)
                else:
                    while allocation_counter < nr:
                        allocate_message = wrap_await(allocate_subscription.receive_for(1.3))
                        if not allocate_message:
                            break
                        message, metadata = allocate_message
                        allocate_one_node(message, metadata)
        return allocated_nodes

    return allocate_nr_of_nodes


if __name__ == "__main__":
    try:
        make_simple_node_allocator()(None, continuous=True)
    except KeyboardInterrupt:
        pass
