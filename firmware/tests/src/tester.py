import asyncio
import dataclasses
import pathlib
import sys

from pyuavcan.application import Node

from allocator import make_my_allocator_node, get_target_node_id

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
    node = (await make_my_allocator_node())[0]
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


async def dotest_restart_node():
    setup = await do_setup()
    service_client = setup.node.make_client(uavcan.node.ExecuteCommand_1_1, setup.target_node_id)
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_RESTART
    response = await service_client.call(msg)
    print(response)
    setup.node.close()


asyncio.get_event_loop().run_until_complete(dotest_restart_node())
