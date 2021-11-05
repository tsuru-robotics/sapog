#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#

import asyncio
import dataclasses
import pathlib
import sys
import time
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

node_under_testing_hw_id = [49, 255, 213, 5, 77, 84, 49, 52, 81, 71, 5, 67, 144, 228, 1, 8]
node_under_testing_hash_of_hw_id = [49, 255, 213, 5, 77, 84, 49, 52, 81, 71, 5, 67, 240, 233, 1, 8]
node_under_testing_hw_id = node_under_testing_hash_of_hw_id


@dataclasses.dataclass
class SetupData:
    node: Node
    target_node_id: int


def do_cleanup(data: SetupData):
    data.node.close()


# def test_access_register():
#     setup = do_setup()
#     pass
#
#
# # make_my_allocator_node is a fixture from special_tracker
# def test_write_register():
#     setup = do_setup()
#     print(f"Resetting node_id of {setup.target_node_id}")
#     global already_ran
#     if already_ran:
#         return
#     already_ran = True
#     service_client = setup.node.make_client(uavcan.register.Access_1_0, setup.target_node_id)
#     msg = uavcan.register.Access_1_0.Request()
#     my_array = uavcan.primitive.array.Integer64_1_0()
#     my_array.value = [1]
#     msg.name.name = "uavcan_node_id"
#     msg.value.integer64 = my_array
#     response = await service_client.call(msg)
#     print(response)
#     setup.node.close()
hw_id_type = typing.Union[typing.List[int], bytes, bytearray]


def make_registry(node_id: int):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = "socketcan:slcan0"
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = node_id
    return registry01


async def get_any_target_node_id(test_conductor_node: Node):
    """Catch any node that is sending a heartbeat, make sure that it isn't the testing node and then return its
    node ID"""
    event = asyncio.Event()
    heartbeat_subscriber = test_conductor_node.make_subscriber(uavcan.node.Heartbeat_1_0)
    target_node_id = None

    def handle_heartbeats(message_class: MessageClass, transfer_from: pyuavcan.transport._transfer.TransferFrom):
        nonlocal target_node_id
        if transfer_from.source_node_id != test_conductor_node.id:
            target_node_id = transfer_from.source_node_id
            event.set()

    heartbeat_subscriber.receive_in_background(handle_heartbeats)
    # stops here and waits for the handler to declare that it has received a fitting node_id
    # if the timeout sets the event first then None is returned
    # heartbeat_subscriber.close() This should be cleaned somewhere
    await event.wait()
    return target_node_id


async def get_target_node_id_by_hw_id(test_conductor_node: Node, target_hw_id: hw_id_type) -> int:
    """Catch any node that is sending a heartbeat, make sure that it isn't the testing node and then return its
    node ID"""
    event = asyncio.Event()
    heartbeat_subscriber = test_conductor_node.make_subscriber(uavcan.node.Heartbeat_1_0)
    target_node_id = None

    def handle_heartbeats(message_class: MessageClass, transfer_from: pyuavcan.transport._transfer.TransferFrom):
        print("handler called")
        nonlocal target_node_id
        if transfer_from.source_node_id != test_conductor_node.id:
            get_info_client = test_conductor_node.make_client(uavcan.node.GetInfo_1_0, transfer_from.source_node_id)
            get_info_request = uavcan.node.GetInfo_1_0.Request()
            get_info_response: uavcan.node.GetInfo_1_0.Response = wrap_await(
                asyncio.wait_for(get_info_client.call(get_info_request)), 1)
            if get_info_response.unique_id == target_hw_id:
                target_node_id = transfer_from.source_node_id
                event.set()

    heartbeat_subscriber.receive_in_background(handle_heartbeats)

    await event.wait()

    return target_node_id


async def is_waiting_pnp() -> bool:
    pass


def configure_note_register():
    print(reg.drone.physics.acoustics.Note_0_1)


def test_esc_spin_2_seconds():
    pass


def allocate_one_node_id():
    with OneTimeAllocator(node_under_testing_hw_id) as allocator:
        wrap_await(asyncio.wait_for(allocator.one_node_allocated_event.wait(), 3))


def test_allows_allocation_of_node_id():
    try:
        allocate_one_node_id()
        assert True
    except TimeoutError:
        assert False


def test_restart_node():
    registry01 = make_registry(3)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.debugger"), registry01) as node:
        target_node_id = wrap_await(asyncio.wait_for(get_target_node_id_by_hw_id(node, node_under_testing_hw_id), 2))
        assert target_node_id is not None
        service_client = node.make_client(uavcan.node.ExecuteCommand_1_1, target_node_id)
        msg = uavcan.node.ExecuteCommand_1_1.Request()
        msg.command = msg.COMMAND_RESTART
        response = wrap_await(service_client.call(msg))
        node.close()
        assert response is not None


def test_has_heartbeat():
    allocate_one_node_id()
    try:
        registry01 = make_registry(3)
        with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
            this_awaitable = asyncio.wait_for(get_target_node_id_by_hw_id(node, node_under_testing_hw_id), 6)
            result = wrap_await(this_awaitable)
            assert result is not None
    except TimeoutError:
        assert False


if __name__ == "__main__":
    configure_note_register()
