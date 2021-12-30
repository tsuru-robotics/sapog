import pathlib
import typing
from typing import Optional, List

import sys

import pyuavcan
from pyuavcan.application._node import MessageClass
from pyuavcan.transport.redundant._session import RedundantTransferFrom

import my_nodes
import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
from _await_wrap import wrap_await
import time

from utils import make_registry

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo, register


def make_simple_node_allocator():
    from utils import get_available_slcan_interfaces
    internal_table = {}

    def allocate_nr_of_nodes(nr: Optional[int] = None, continuous: bool = False,
                             node_to_use: Optional[pyuavcan.application.Node] = None,
                             interfaces: Optional[List[str]] = [],
                             node_id_to_use: Optional[int] = 6, time_budget_seconds: Optional[int] = None) \
            -> List[my_nodes.NodeInfo]:
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
        allocated_nodes: List[my_nodes.NodeInfo] = []
        allocation_counter = 0
        allocate_responder = node.make_publisher(uavcan.pnp.NodeIDAllocationData_1_0)
        allocate_subscription = node.make_subscriber(uavcan.pnp.NodeIDAllocationData_1_0)

        def allocate_one_node(msg, _) -> my_nodes.NodeInfo:
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
            new_node_info = my_nodes.NodeInfo(str(msg.unique_id_hash), interfaces, node_id=new_id)
            allocated_nodes.append(new_node_info)
            allocation_counter += 1
            wrap_await(allocate_responder.publish(response))
            return new_node_info

        if continuous:
            # Need to set up a listener on every interface because that's the only way to know which interface the
            # allocation request originates from

            def allocation_request_reception(message_class: uavcan.pnp.NodeIDAllocationData_1_0,
                                             transfer_from: pyuavcan.transport.TransferFrom):
                def hw_id_matcher(node_info):
                    node_info.hw_id == message_class.unique_id_hash

                if isinstance(transfer_from, RedundantTransferFrom):
                    tr_ses = allocate_subscription.transport_session
                    assert isinstance(tr_ses, pyuavcan.transport.redundant.RedundantSession)
                    iface_index = tr_ses.inferiors.index(transfer_from.inferior_session)
                    if (existing_entry := next(filter(hw_id_matcher, allocated_nodes), None)) is not None:
                        existing_entry.append()
                else:
                    assert False
                    print("You only have one interface, why did you call this function?")

            allocate_subscription.receive_in_background()
            if time_budget_seconds is not None:
                started_time = time.time()
            while True:
                message, metadata = wrap_await(allocate_subscription.receive_for(1.3))
                allocate_one_node(message, metadata)
                if time_budget_seconds and time.time() - started_time > time_budget_seconds:
                    break
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
