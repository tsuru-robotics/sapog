import asyncio
import json
import pathlib
import sys
import re
from typing import Optional
from itertools import chain

import pyuavcan.dsdl
import typing

from pyuavcan.dsdl import FixedPortObject

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path.absolute())

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

do_update_dsdl = False

from pyuavcan.application import make_node, NodeInfo, Node
from pyuavcan.application.node_tracker import NodeTracker
from pyuavcan.application.plug_and_play import CentralizedAllocator, Allocator
from pyuavcan.transport import _tracer, Trace, Tracer
from pyuavcan.application.node_tracker import Entry
from pyuavcan.util import import_submodules, iter_descendants


def make_handler_for_getinfo_update(allocator: Allocator):
    def handle_getinfo_handler_format(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
        async def handle_inner_function():
            if node_id and next_entry and next_entry.info is not None:
                print("Allocating one node")
                allocator.register_node(node_id, bytes(next_entry.info.unique_id))
                await asyncio.sleep(2)
                # await reset_node_id(node, node_id)

        asyncio.get_event_loop().create_task(handle_inner_function())

    return handle_getinfo_handler_format


def format_trace_view_nicely(trace: Trace, ids: typing.Dict[int, FixedPortObject]):
    payload: str = ""
    count = 0
    deserialized = str(trace.transfer)
    for memory_view in trace.transfer.fragmented_payload:
        my_list = memory_view.tolist()
        for byte in bytes(my_list):
            payload += '{:02X} '.format(byte)
        else:
            payload = payload[:len(payload) - 1]
        count += 1
        if count >= 4:
            payload += "\n"
            count = 0
        else:
            payload += " | "
    else:
        payload = payload[:len(payload) - len(" |")]
    deserialized = re.sub(r"fragmented_payload=\[[^\[\]]+?\]", "\nPAYLOAD\n" + payload, deserialized)
    deserialized = deserialized.replace("AlienTransfer(AlienTransferMetadata(AlienSessionSpecifier(", "transfer(")[:-2]
    for key, value in ids.items():
        deserialized = deserialized.replace("subject_id=" + str(key), "subject_id=" + value.__name__ + f"({str(key)})")
        deserialized = deserialized.replace("service_id=" + str(key), "service_id=" + value.__name__ + f"({str(key)})")
    return deserialized


def deserialize_trace(trace: Trace, ids: typing.Dict[int, FixedPortObject], subject_id: int):
    obj = pyuavcan.dsdl.deserialize(ids[subject_id], trace.transfer.fragmented_payload)
    return json.dumps(pyuavcan.dsdl.to_builtin(obj))


def fill_ids():
    ids = {}
    filtered_types = ["ABCMeta"]
    chained_descendants = chain(iter_descendants(pyuavcan.dsdl.FixedPortCompositeObject),
                                iter_descendants(pyuavcan.dsdl.FixedPortServiceObject))
    filtered_generator = (type_ for type_ in chained_descendants if type_ not in filtered_types)
    for t in filtered_generator:
        ids[pyuavcan.dsdl.get_fixed_port_id(t)] = t
    return ids


def make_capture_handler(tracer: Tracer, ids: typing.Dict[int, FixedPortObject]):
    def capture_handler(capture: _tracer.Capture):
        with open("rx_frm.txt", "a") as log_file:
            # Checking to see if a transfer has finished, then assigning the value to transfer_trace
            if (transfer_trace := tracer.update(capture)) is not None:
                subject_id = None
                try:
                    subject_id = transfer_trace.transfer.metadata.session_specifier.data_specifier.subject_id
                except Exception as e:
                    print(e.args[-1])
                print(deserialize_trace(transfer_trace, ids, subject_id))
                log_file.write(format_trace_view_nicely(transfer_trace, ids) + "\n")

    return capture_handler


import os


# TODO: Need to implement this method to be able to test anything.
async def get_target_node_id(test_conductor_node: Node) -> int:
    """Catch any node that is sending a heartbeat, make sure that it isn't the testing node and then return its
    node ID"""
    t = NodeTracker(test_conductor_node)
    event = asyncio.Event(loop=asyncio.get_event_loop())

    def capture_handler(capture: _tracer.Capture):
        tracer = test_conductor_node.presentation.transport.make_tracer()
        if (transfer_trace := tracer.update(capture)) is not None:
            print("Yeah")

    t.add_update_handler(capture_handler)
    return 1


async def reset_node_id(sending_node: Node, current_target_node_id: int) -> bool:
    print(f"Resetting node_id of {current_target_node_id}")
    global already_ran
    if already_ran:
        return
    already_ran = True
    service_client = sending_node.make_client(uavcan.register.Access_1_0, current_target_node_id)
    msg = uavcan.register.Access_1_0.Request()
    my_array = uavcan.primitive.array.Integer64_1_0()
    my_array.value = [1]
    msg.name.name = "uavcan_node_id"
    msg.value.integer64 = my_array
    response = await service_client.call(msg)
    print(response)


def configure_note_on_sapog(sending_node: Node, current_target_node_id: int):
    service_client = sending_node.make_client(uavcan.register.Access_1_0, current_target_node_id)


def check_and_make_defaults():
    env_default = {
        "UAVCAN__CAN__IFACE": "socketcan:slcan0",
        "UAVCAN__CAN__MTU": "8",
        "UAVCAN__NODE__ID": "42"
    }
    for key, value in env_default.items():
        if os.environ.get(key) is not None:
            print(
                f"Warning, environment variable {key} has already been set, your defaults are overridden by value \"{value}\".")
        os.environ.setdefault(key, value)


async def make_my_allocator_node(with_debugging=False) -> Node:
    check_and_make_defaults()
    node = make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), "databases/node1.db")
    if with_debugging:
        import_submodules(uavcan)
        ids = fill_ids()
        tracer = node.presentation.transport.make_tracer()
        node.presentation.transport.begin_capture(make_capture_handler(tracer, ids))
    t = NodeTracker(node)
    centralized_allocator = CentralizedAllocator(node)
    t.add_update_handler(make_handler_for_getinfo_update(centralized_allocator))
    print("Running")
    return node, centralized_allocator, t


async def run_allocator(with_debugging=False):
    if with_debugging:
        pass
    node, allocator, tracker = await make_my_allocator_node()
    while True:
        await asyncio.sleep(1)
    node.close()


async def run_allocator2(with_debugging=False):
    check_and_make_defaults()
    with make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), "databases/node1.db") as node:
        import_submodules(uavcan)
        ids = fill_ids()
        tracer = node.presentation.transport.make_tracer()
        node.presentation.transport.begin_capture(make_capture_handler(tracer, ids))
        t = NodeTracker(node)
        centralized_allocator = CentralizedAllocator(node)
        t.add_update_handler(make_handler_for_getinfo_update(centralized_allocator))
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run_allocator2())
    except KeyboardInterrupt:
        pass
