import pathlib
from typing import Optional, List

import sys

import pyuavcan

import my_nodes
import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
from _await_wrap import wrap_await

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo, register


def make_simple_node_allocator(interfaces: Optional[List[str]] = [], node_id_to_use: int = 6,
                               node_to_use: Optional[pyuavcan.application.Node] = None):
    from utils import get_available_slcan_interfaces
    internal_table = {}
    if not node_to_use:
        registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
        if len(interfaces) == 0:
            interfaces = get_available_slcan_interfaces()

        registry01["uavcan.can.iface"] = " ".join(interfaces)
        registry01["uavcan.can.mtu"] = 8
        registry01["uavcan.node.id"] = node_id_to_use
        node = make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), registry01)
    else:
        node = node_to_use

    def allocate_nr_of_nodes(nr: int, continuous: bool = False) -> List[my_nodes.NodeInfo]:
        allocated_nodes: List[my_nodes.NodeInfo] = []
        allocation_counter = 0
        allocate_responder = node.make_publisher(uavcan.pnp.NodeIDAllocationData_1_0)
        allocate_subscription = node.make_subscriber(uavcan.pnp.NodeIDAllocationData_1_0)

        def allocate_one_node(msg, _):
            nonlocal allocation_counter
            hw_id_already_allocated = any(node.hw_id == str(msg.unique_id_hash) for node in allocated_nodes)
            if hw_id_already_allocated:
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
            allocated_nodes.append(
                my_nodes.NodeInfo(str(msg.unique_id_hash), interfaces, node_id=new_id))
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
