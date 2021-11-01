#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#

import asyncio
import dataclasses
import pathlib
import sys

import pyuavcan
from pyuavcan.application import Node
from pyuavcan.presentation._presentation import MessageClass

from allocator import make_my_allocator_node

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path.absolute())

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array


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

async def get_target_node_id(test_conductor_node: Node) -> int:
    """Catch any node that is sending a heartbeat, make sure that it isn't the testing node and then return its
    node ID"""
    test_conductor_node.add_lifetime_hooks(lambda: print("Started node"), lambda: print("Destroyed node"))
    event = asyncio.Event()
    heartbeat_subscriber = test_conductor_node.make_subscriber(uavcan.node.Heartbeat_1_0)
    target_node_id = None

    async def handle_heartbeats(message_class: MessageClass, transfer_from: pyuavcan.transport._transfer.TransferFrom):
        nonlocal target_node_id
        if transfer_from.source_node_id != test_conductor_node.id:
            target_node_id = transfer_from.source_node_id
            # event.set()

    async def time_out():
        nonlocal event
        await asyncio.sleep(1)
        event.set()

    asyncio.get_event_loop().create_task(time_out())
    heartbeat_subscriber.receive_in_background(handle_heartbeats)
    # def capture_handler(capture: _tracer.Capture):
    #     print("Yeah")
    #     tracer = test_conductor_node.presentation.transport.make_tracer()
    #     if (transfer_trace := tracer.update(capture)) is not None:
    #         event.set()

    await event.wait()
    heartbeat_subscriber.close()
    return target_node_id


# The tests themselves should not be run asynchronously, I just find it convenient to type await instead of asyncio.get_event_loop().run_until_complete()
def test_allows_pnp():
    pass


def wrap_await(async_def):
    return asyncio.get_event_loop().run_until_complete(async_def)


def test_restart_node():
    node, _, tracker = wrap_await(make_my_allocator_node())
    service_client = node.make_client(uavcan.node.ExecuteCommand_1_1, wrap_await(get_target_node_id(node)))
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_RESTART
    response = wrap_await(service_client.call(msg))
    node.close()
    assert response is not None


def test_has_heartbeat():
    node, _, node_tracker = wrap_await(make_my_allocator_node())
    assert wrap_await(get_target_node_id(node)) is not None
