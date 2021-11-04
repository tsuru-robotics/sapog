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

from pyuavcan.application import make_node, NodeInfo, Node, register
from pyuavcan.application.node_tracker import NodeTracker
from pyuavcan.application.plug_and_play import CentralizedAllocator, Allocator
from pyuavcan.transport import _tracer, Trace, Tracer
from pyuavcan.application.node_tracker import Entry
from pyuavcan.util import import_submodules, iter_descendants


def make_handler_for_getinfo_update():
    def handle_getinfo_handler_format(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
        async def handle_inner_function():
            if node_id and next_entry and next_entry.info is not None:
                # print("Debugger sees an allocation request")
                await asyncio.sleep(2)

        asyncio.get_event_loop().create_task(handle_inner_function())

    return handle_getinfo_handler_format


def format_payload_hex_view(trace: Trace):
    payload: str = ""
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
    return payload


def deserialize_trace(trace: Trace, ids: typing.Dict[int, FixedPortObject], subject_id: int):
    if ids.get(subject_id) is None:
        return f"missing id {subject_id}"
    try:
        obj = pyuavcan.dsdl.deserialize(ids[subject_id], trace.transfer.fragmented_payload)
        built_in_representation = pyuavcan.dsdl.to_builtin(obj)
    except TypeError:
        built_in_representation = {}
    if "clients" in built_in_representation.keys():
        built_in_representation["clients"] = None
    if "servers" in built_in_representation.keys():
        built_in_representation["servers"] = None
    transfer_deserialized = str(trace.transfer)
    transfer_deserialized = transfer_deserialized.replace(
        "AlienTransfer(AlienTransferMetadata(AlienSessionSpecifier(",
        "transfer(")
    for key, value in ids.items():
        transfer_deserialized = transfer_deserialized.replace("subject_id=" + str(key),
                                                              "subject_id=" + value.__name__ + f"({str(key)})")
        transfer_deserialized = transfer_deserialized.replace("service_id=" + str(key),
                                                              "service_id=" + value.__name__ + f"({str(key)})")
    transfer_deserialized = re.sub(r"fragmented_payload=\[[^\[\]]+?\]", json.dumps(built_in_representation),
                                   transfer_deserialized)
    return transfer_deserialized


def fill_ids():
    ids = {}
    filtered_types = ["ABCMeta"]
    chained_descendants = chain(iter_descendants(pyuavcan.dsdl.FixedPortCompositeObject),
                                iter_descendants(pyuavcan.dsdl.FixedPortServiceObject))
    filtered_generator = (type_ for type_ in chained_descendants if type_ not in filtered_types)
    for t in filtered_generator:
        ids[pyuavcan.dsdl.get_fixed_port_id(t)] = t
    return ids


ignore_subjects = [
    7510,  # port_list
    7509  # heartbeat
]


def make_capture_handler(tracer: Tracer, ids: typing.Dict[int, FixedPortObject], debugger_id_for_filtering: int,
                         log_to_file=True, log_to_print=True, ignore_traffic_by_debugger=True):
    def capture_handler(capture: _tracer.Capture):
        with open("rx_frm.txt", "a") as log_file:
            # Checking to see if a transfer has finished, then assigning the value to transfer_trace
            if (transfer_trace := tracer.update(capture)) is not None:
                if ignore_traffic_by_debugger and \
                        transfer_trace.transfer.metadata.session_specifier.source_node_id == debugger_id_for_filtering:
                    return
                subject_id = None
                try:
                    subject_id = transfer_trace.transfer.metadata.session_specifier.data_specifier.subject_id
                except Exception as e:
                    subject_id = transfer_trace.transfer.metadata.session_specifier.data_specifier.service_id
                    print(e.args[-1])
                if subject_id in ignore_subjects:
                    return
                deserialized_trace = deserialize_trace(transfer_trace, ids, subject_id)
                if deserialized_trace is None:
                    return
                if log_to_print:
                    print(deserialized_trace)
                if log_to_file:
                    log_file.write(deserialized_trace + "\n")

    return capture_handler


import os


def get_target_node_id(allocator_node: Node) -> int:
    pass


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


async def run_debugger_node(with_debugging=False):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = "socketcan:slcan0"
    registry01["uavcan.can.mtu"] = 8
    debugger_node_id = 2
    registry01["uavcan.node.id"] = debugger_node_id

    with make_node(NodeInfo(name="com.zubax.sapog.tests.debugger"), registry01) as node:
        import_submodules(uavcan)
        ids = fill_ids()
        tracer = node.presentation.transport.make_tracer()
        node.presentation.transport.begin_capture(
            make_capture_handler(tracer, ids, log_to_file=with_debugging, log_to_print=with_debugging,
                                 debugger_id_for_filtering=debugger_node_id))
        t = NodeTracker(node)
        t.add_update_handler(make_handler_for_getinfo_update())
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run_debugger_node(True))
    except KeyboardInterrupt:
        pass
