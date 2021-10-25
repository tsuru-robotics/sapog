import dataclasses
import pathlib
import sys

from pyuavcan.application import Node

from special_tracker import make_my_allocator_node, get_target_node_id

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
def do_setup():
    node = make_my_allocator_node()
    target_node_id = get_target_node_id()
    return SetupData(node, target_node_id)


def do_cleanup(data: SetupData):
    data.node.close()


def test_access_register():
    setup = do_setup()
    pass


# make_my_allocator_node is a fixture from special_tracker
def test_write_register():
    setup = do_setup()
    sending_node = make_my_allocator_node
    print(f"Resetting node_id of {setup.target_node_id}")
    global already_ran
    if already_ran:
        return
    already_ran = True
    service_client = sending_node.make_client(uavcan.register.Access_1_0, setup.target_node_id)
    msg = uavcan.register.Access_1_0.Request()
    my_array = uavcan.primitive.array.Integer64_1_0()
    my_array.value = [1]
    msg.name.name = "uavcan_node_id"
    msg.value.integer64 = my_array
    response = await service_client.call(msg)
    print(response)
    sending_node.close()
