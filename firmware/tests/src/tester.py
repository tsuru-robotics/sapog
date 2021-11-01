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


# I refuse to use fixtures, what if someone doesn't know about them
# they would be super confused.
async def do_setup():
    node, _, node_tracker = (await make_my_allocator_node())
    target_node_id = await get_target_node_id(node)
    return SetupData(node, target_node_id)


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
    # def capture_handler(capture: _tracer.Capture):
    #     print("Yeah")
    #     tracer = test_conductor_node.presentation.transport.make_tracer()
    #     if (transfer_trace := tracer.update(capture)) is not None:
    #         event.set()

    await event.wait()
    heartbeat_subscriber.close()
    return target_node_id


async def dotest_restart_node():
    setup = await do_setup()
    service_client = setup.node.make_client(uavcan.node.ExecuteCommand_1_1, setup.target_node_id)
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_RESTART
    response = await service_client.call(msg)
    print(response)
    setup.node.close()


asyncio.get_event_loop().run_until_complete(dotest_restart_node())
