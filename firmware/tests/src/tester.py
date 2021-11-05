#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#

import asyncio
import dataclasses
import pathlib
import sys
import typing

import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo, register
from pyuavcan.presentation._presentation import MessageClass

from _await_wrap import wrap_await
from allocator import OneTimeAllocator

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path.absolute())

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
import reg.drone.physics.acoustics.Note_0_1

node_under_testing_name = "io.px4.sapog"


def make_registry(node_id: int):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = "socketcan:slcan0"
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = node_id
    return registry01


def test_write_register():
    target_node_id, target_node_name = allocate_one_node_id()
    registry01 = make_registry(3)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
        service_client = node.make_client(uavcan.register.Access_1_0, target_node_id)
        msg = uavcan.register.Access_1_0.Request()
        my_array = uavcan.primitive.array.Integer64_1_0()
        my_array.value = [1]
        msg.name.name = "uavcan_node_id"
        msg.value.integer64 = my_array
        response = wrap_await(asyncio.wait_for(service_client.call(msg), 0.5))
        assert response is not None


hw_id_type = typing.Union[typing.List[int], bytes, bytearray]


def configure_note_register():
    print(reg.drone.physics.acoustics.Note_0_1)


def test_esc_spin_2_seconds():
    pass


def allocate_one_node_id():
    with OneTimeAllocator(node_under_testing_name) as allocator:
        wrap_await(asyncio.wait_for(allocator.one_node_allocated_event.wait(), 3))
        return allocator.allocated_node_id, allocator.allocated_node_name


def test_allows_allocation_of_node_id():
    try:
        allocate_one_node_id()
        assert True
    except TimeoutError:
        assert False


def test_restart_node():
    node_id, node_name = allocate_one_node_id()
    registry01 = make_registry(3)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
        target_node_id = node_id
        service_client = node.make_client(uavcan.node.ExecuteCommand_1_1, target_node_id)
        msg = uavcan.node.ExecuteCommand_1_1.Request()
        msg.command = msg.COMMAND_RESTART
        response = wrap_await(service_client.call(msg))
        node.close()
        assert response is not None


def test_has_heartbeat():
    node_id, node_name = allocate_one_node_id()
    try:
        registry01 = make_registry(3)
        with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
            subscriber = node.make_subscriber(uavcan.node.Heartbeat_1_0)
            event = asyncio.Event()

            def hb_handler(message_class: MessageClass, transfer_from: pyuavcan.transport._transfer.TransferFrom):
                if transfer_from.source_node_id == node_id:
                    event.set()

            subscriber.receive_in_background(hb_handler)
            wrap_await(asyncio.wait_for(event.wait(), 2))
            assert True
    except TimeoutError:
        assert False


if __name__ == "__main__":
    configure_note_register()
