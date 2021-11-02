#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#

import asyncio
import json
import pathlib
import sys
import re
from asyncio import Event
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

from pyuavcan.application import make_node, NodeInfo, Node, register
from pyuavcan.application.node_tracker import NodeTracker
from pyuavcan.application.plug_and_play import CentralizedAllocator, Allocator
from pyuavcan.transport import _tracer, Trace, Tracer
from pyuavcan.application.node_tracker import Entry
from pyuavcan.util import import_submodules, iter_descendants


def make_handler_for_getinfo_update(allocator: Allocator, event: asyncio.Event):
    def handle_getinfo_handler_format(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
        async def handle_inner_function():
            if node_id and next_entry and next_entry.info is not None:
                print("Allocating one node")
                allocator.register_node(node_id, bytes(next_entry.info.unique_id))
                event.set()

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
                    pass
                    # print(e.args[-1])
                # print(deserialize_trace(transfer_trace, ids, subject_id))
                log_file.write(format_trace_view_nicely(transfer_trace, ids) + "\n")

    return capture_handler


import os


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


def get_ids():
    import_submodules(uavcan)
    return fill_ids()


get_info_handler_type = typing.Callable[[int, Optional[Entry], Optional[Entry]], None]
capture_handler_type = typing.Callable[[_tracer.Capture], None]


async def make_complex_node(node_id: str,
                            get_info_handler_wrapper:
                            typing.Callable[[Allocator, Event], get_info_handler_type],
                            capture_handler_wrapper:
                            typing.Callable[[Tracer, typing.Dict[int, FixedPortObject]], capture_handler_type],
                            with_debugging=False,
                            interface: str = "socketcan:slcan0", mtu: str = "MTU") -> Node:
    allocator_node_name = "com.zubax.sapog.tests.allocator"
    registry01: register.Registry = register.Register()
    registry01["UAVCAN__CAN__IFACE"] = interface
    registry01["UAVCAN__CAN__MTU"] = mtu
    registry01["UAVCAN__NODE__ID"] = node_id
    node = make_node(NodeInfo(name=allocator_node_name), f"databases/{allocator_node_name}.db", registry01)
    if with_debugging:
        tracer = node.presentation.transport.make_tracer()
        if capture_handler:
            node.presentation.transport.begin_capture(capture_handler)
    node_tracker = NodeTracker(node)
    centralized_allocator = CentralizedAllocator(node)
    if get_info_handler:
        node_tracker.add_update_handler(get_info_handler())

    print("Running")
    return node, centralized_allocator, node_tracker


async def run_allocator(with_debugging=False):
    if with_debugging:
        pass
    node, allocator, tracker = await make_my_allocator_node()
    while True:
        await asyncio.sleep(1)
    node.close()


async def run_allocator2(time_out: Optional[int] = None):
    check_and_make_defaults()
    make_handler_for_getinfo_update(centralized_allocator)
    make_capture_handler(tracer, ids)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), "databases/node1.db") as node:
        import_submodules(uavcan)
        ids = fill_ids()
        tracer = node.presentation.transport.make_tracer()
        node.presentation.transport.begin_capture(make_capture_handler(tracer, ids))
        t = NodeTracker(node)
        centralized_allocator = CentralizedAllocator(node)
        event = asyncio.Event()
        t.add_update_handler(make_handler_for_getinfo_update(centralized_allocator, event))
        if time_out:
            async def time_out_coroutine(time_out_time):
                nonlocal event
                await asyncio.sleep(time_out_time)
                event.set()

            asyncio.get_event_loop().create_task(time_out_coroutine(time_out))
        while not event.is_set():
            await asyncio.sleep(0.04)
        return True


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run_allocator2())
    except KeyboardInterrupt:
        pass
