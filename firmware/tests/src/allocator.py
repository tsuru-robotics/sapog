"""For node id allocation in testing environments."""
#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#

import asyncio
import pathlib
import sys
from abc import ABC
from asyncio import Event
from typing import Optional

import pyuavcan.dsdl
import typing

from pyuavcan.application._node_factory import SimpleNode
from pyuavcan.dsdl import FixedPortObject

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, str(namespace_path.absolute()))

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

from pyuavcan.application import make_node, NodeInfo, Node, register
from pyuavcan.application.node_tracker import NodeTracker
from pyuavcan.application.plug_and_play import CentralizedAllocator, Allocator
from pyuavcan.transport import _tracer, Tracer, Transfer
from pyuavcan.application.node_tracker import Entry


async def reset_node_id(sending_node: Node, current_target_node_id: int) -> bool:
    print(f"Resetting node_id of {current_target_node_id}")
    service_client = sending_node.make_client(uavcan.register.Access_1_0, current_target_node_id)
    msg = uavcan.register.Access_1_0.Request()
    my_array = uavcan.primitive.array.Integer64_1_0()
    my_array.value = [1]
    msg.name.name = "uavcan.node.id"
    msg.value.integer64 = my_array
    response = await service_client.call(msg)
    print(response)


hw_id_type = typing.Union[typing.List[int], bytes, bytearray]


class OneTimeAllocator(Allocator, ABC):
    """This class is used for testing if allocation works on Sapog

    It creates a Node that will be used as an allocator."""

    def __init__(self, target_name: str):
        print("One time allocator constructed.")
        registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
        registry01["uavcan.can.iface"] = "socketcan:slcan0 socketcan:slcan1"
        registry01["uavcan.can.mtu"] = 8
        registry01["uavcan.node.id"] = 1
        self.node = make_node(NodeInfo(name="one_time_allocator_node"), registry01)
        self.tracker = NodeTracker(self.node)
        self.one_node_allocated_event = asyncio.Event()
        self.allocated_node_id = None
        self.allocated_node_name = None

        def get_info_handler(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
            if not target_name:
                raise Exception("Target name is missing")

            if next_entry and next_entry.info is not None:
                entry = next_entry.info
            else:
                entry = self.tracker.registry[node_id]
            if target_name \
                    and hasattr(entry.info, "name") and target_name != entry.info.name:
                return
            self.allocated_node_id = node_id
            self.allocated_node_name = next_entry.info.name
            self.one_node_allocated_event.set()

        self.tracker.add_update_handler(get_info_handler)
        centralized_allocator = CentralizedAllocator(self.node)
        self.node.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.node.close()


get_info_handler_type = typing.Callable[[int, Optional[Entry], Optional[Entry]], None]
get_info_handler_wrapper_type = Optional[typing.Callable[[Allocator, Event], get_info_handler_type]]
capture_handler_type = typing.Callable[[_tracer.Capture], None]
capture_handler_wrapper_type = Optional[
    typing.Callable[[Tracer, typing.Dict[int, FixedPortObject]], capture_handler_type]]


async def run_continuous_allocator(time_out: Optional[int] = None, allocator_id: int = 1,
                                   name="com.zubax.sapog.tests.allocator"):
    event = asyncio.Event()
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = "socketcan:slcan0"
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = 1
    with make_node(NodeInfo(name="allocator_node"), registry01) as node:
        centralized_allocator = CentralizedAllocator(node)
        while True:
            await asyncio.sleep(0.1)
    return True


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run_continuous_allocator())
    except KeyboardInterrupt:
        pass
