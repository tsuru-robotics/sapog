#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import pathlib
from typing import Optional, List

import sys

import pycyphal

import my_nodes
import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import time

from make_registry import make_registry

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pycyphal.application import make_node, NodeInfo, register


def make_simple_node_allocator():
    internal_table = {}

    async def allocate_nr_of_nodes(nr: Optional[int] = None, continuous: bool = False,
                                   node_to_use: Optional[pycyphal.application.Node] = None,
                                   interfaces: Optional[List[str]] = [], time_budget_seconds: Optional[int] = None) \
            -> List[my_nodes.NodeInfo]:
        if not node_to_use:
            registry01 = make_registry(use_all_interfaces=True)
            node = make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), registry01)
        else:
            node = node_to_use
        allocated_nodes: List[my_nodes.NodeInfo] = []
        allocation_counter = 0
        allocate_responder = node.make_publisher(uavcan.pnp.NodeIDAllocationData_1_0)
        allocate_subscription = node.make_subscriber(uavcan.pnp.NodeIDAllocationData_1_0)

        async def allocate_one_node(msg, _) -> my_nodes.NodeInfo:
            nonlocal allocation_counter
            hw_id_already_allocated = any(node.hw_id == str(msg.unique_id_hash) for node in allocated_nodes)
            if hw_id_already_allocated:
                return None
            assert isinstance(msg, uavcan.pnp.NodeIDAllocationData_1_0)
            their_unique_id = msg.unique_id_hash
            if (their_node_id := internal_table.get(their_unique_id)) is not None:
                print(f"NodeID {their_node_id} requested another NodeID, one is enough!")
                return
            assigned_node_id = 21 + allocation_counter
            new_id = uavcan.node.ID_1_0(assigned_node_id)
            response = uavcan.pnp.NodeIDAllocationData_1_0(msg.unique_id_hash, [new_id])
            new_node_info = my_nodes.NodeInfo(str(msg.unique_id_hash), interfaces, node_id=new_id.value)
            allocated_nodes.append(new_node_info)
            allocation_counter += 1
            await allocate_responder.publish(response)
            return new_node_info

        if continuous:
            # Need to set up a listener on every interface because that's the only way to know which interface the
            # allocation request originates from
            if time_budget_seconds is not None:
                started_time = time.time()
            while True:
                try:
                    message, metadata = await allocate_subscription.receive_for(1.3)
                    await allocate_one_node(message, metadata)
                except TypeError:
                    continue
                finally:
                    if time_budget_seconds and time.time() - started_time > time_budget_seconds:
                        break
        else:
            while allocation_counter < nr:
                allocate_message = await allocate_subscription.receive_for(1.3)
                if not allocate_message:
                    break
                message, metadata = allocate_message
                await allocate_one_node(message, metadata)
        return allocated_nodes

    return allocate_nr_of_nodes


if __name__ == "__main__":
    try:
        asyncio.run(make_simple_node_allocator()(None, continuous=True))
    except KeyboardInterrupt:
        pass
