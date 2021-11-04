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

import pyuavcan
from pyuavcan.application import Node
from pyuavcan.presentation._presentation import MessageClass

from _await_wrap import wrap_await
from allocator import make_complex_node, ComplexNodeUtilities, OneTimeAllocator

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path.absolute())

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
import reg.drone.physics.acoustics.Note_0_1

from allocator import make_complex_node


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
            event.set()

    heartbeat_subscriber.receive_in_background(handle_heartbeats)
    # stops here and waits for the handler to declare that it has received a fitting node_id
    # if the timeout sets the event first then None is returned
    # heartbeat_subscriber.close() This should be cleaned somewhere
    event.wait()
    return target_node_id


async def is_waiting_pnp() -> bool:
    complex_node_utils = make_complex_node("1")


def configure_note_register():
    print(reg.drone.physics.acoustics.Note_0_1)


def test_esc_spin_2_seconds():
    pass


def test_allows_allocation_of_node_id():
    with OneTimeAllocator("1") as allocator:
        event = allocator.allocate_one_node([49, 255, 213, 5, 77, 84, 49, 52, 81, 71, 5, 67, 144, 228, 1, 8])
        wrap_await(asyncio.wait_for(event.wait(), 3))


def test_restart_node():
    complex_node_utils = wrap_await(make_complex_node("1"))
    target_node_id = wrap_await(asyncio.wait_for(get_target_node_id(complex_node_utils.node), 2))
    assert target_node_id is not None
    service_client = complex_node_utils.node.make_client(uavcan.node.ExecuteCommand_1_1, target_node_id)
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_RESTART
    response = wrap_await(service_client.call(msg))
    complex_node_utils.node.close()
    assert response is not None


def test_has_heartbeat():
    node, _, node_tracker = wrap_await(make_complex_node("1"))
    assert wrap_await(get_target_node_id(node)) is not None


if __name__ == "__main__":
    configure_note_register()
