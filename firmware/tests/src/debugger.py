#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#

import asyncio
import json
import re
from typing import Optional
from itertools import chain

import pyuavcan.dsdl
import typing

from pyuavcan.dsdl import FixedPortObject
from pyuavcan.transport.can import CANErrorTrace

from conftest import add_deps

add_deps()

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

from pyuavcan.application import make_node, NodeInfo, Node, register
from pyuavcan.application.node_tracker import NodeTracker
from pyuavcan.transport import _tracer, Trace, Tracer, TransferTrace
from pyuavcan.application.node_tracker import Entry
from pyuavcan.util import import_submodules, iter_descendants

from make_registry import make_registry
from datetime import datetime


def make_handler_for_getinfo_update():
    def handle_getinfo_handler_format(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
        async def handle_inner_function():
            if node_id and next_entry and next_entry.info is not None:
                # print("Debugger sees an allocation request")
                await asyncio.sleep(2)

        asyncio.get_event_loop().create_task(handle_inner_function())

    return handle_getinfo_handler_format


def format_payload_hex_view(fragmented_payload: typing.Sequence[memoryview]) -> str:
    payload: str = ""
    count = 0
    for memory_view in fragmented_payload:
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


def format_payload_hex_view_trace(trace: Trace):
    return format_payload_hex_view(trace.transfer.fragmented_payload)


def deserialize_trace(trace: Trace, ids: typing.Dict[int, FixedPortObject], subject_id: int, debugger_id: int):
    transfer_type = "service" if "service" in str(trace.transfer).lower() else "message"
    if ids.get(subject_id) is None:
        return f"{transfer_type} CONFIGURED {subject_id}, from {trace.transfer.metadata.session_specifier.source_node_id} " \
               f"to {trace.transfer.metadata.session_specifier.destination_node_id}" \
               f"\n{str(trace.transfer)}"
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
    if trace.transfer.metadata.session_specifier.source_node_id == debugger_id:
        transfer_deserialized = transfer_deserialized.replace(f"source_node_id={debugger_id}",
                                                              f"source_node_id={debugger_id} (this)")
    if trace.transfer.metadata.session_specifier.destination_node_id == debugger_id:
        transfer_deserialized = transfer_deserialized.replace(f"destination_node_id={debugger_id}",
                                                              f"destination_node_id={debugger_id} (this)")
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
    transfer_deserialized = transfer_deserialized.replace("transfer(ServiceDataSpecifier(", "")
    transfer_deserialized = transfer_deserialized.replace("source_node_id", "src_id")
    transfer_deserialized = transfer_deserialized.replace("destination_node_id", "dest_id")
    transfer_deserialized = transfer_deserialized.replace("priority", "prio")
    transfer_deserialized = transfer_deserialized.replace(", role=<Role.REQUEST: 1>)", "")
    transfer_deserialized = transfer_deserialized.replace("role=<Role.RESPONSE: 2>)", "")
    transfer_deserialized = transfer_deserialized.replace("transfer_id", "t_id")
    transfer_deserialized = transfer_deserialized.replace("), {})", "")
    transfer_deserialized = transfer_deserialized.replace("service_id=", "")
    transfer_deserialized = transfer_type + " " + transfer_deserialized + "\n" + format_payload_hex_view_trace(trace)
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
    # 7510  # port_list
    # , 7509  # heartbeat
    # , 8166  # allocation
    # , 430  # getinfo
    # , 140
    # , 139
]


def make_capture_handler(tracer: Tracer, ids: typing.Dict[int, FixedPortObject], debugger_id_for_filtering: int,
                         log_to_file=True, log_to_print=True, ignore_traffic_by_debugger=True):
    def capture_handler(capture: _tracer.Capture):
        with open("rx_frm.txt", "a") as log_file:
            # Checking to see if a transfer has finished, then assigning the value to transfer_trace
            if (transfer_trace := tracer.update(capture)) is not None:
                if isinstance(transfer_trace, CANErrorTrace):
                    print(transfer_trace)
                elif isinstance(transfer_trace, TransferTrace):
                    is_service_request: bool = hasattr(
                        transfer_trace.transfer.metadata.session_specifier.data_specifier,
                        "service_id")
                    if ignore_traffic_by_debugger and \
                            transfer_trace.transfer.metadata.session_specifier.source_node_id == debugger_id_for_filtering \
                            and not is_service_request:
                        return
                    if is_service_request:
                        subject_id = transfer_trace.transfer.metadata.session_specifier.data_specifier.service_id
                    else:
                        subject_id = transfer_trace.transfer.metadata.session_specifier.data_specifier.subject_id
                    if subject_id in ignore_subjects:
                        return
                    deserialized_trace = deserialize_trace(transfer_trace, ids, subject_id, debugger_id_for_filtering)
                    if deserialized_trace is None:
                        return
                    if log_to_print:
                        print(datetime.now().strftime("%H:%M:%S:%f") + deserialized_trace)
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
    msg.name.name = "uavcan.node.id"
    msg.value.integer64 = my_array
    response = await service_client.call(msg)
    print(response)


async def run_debugger_node(with_debugging=False):
    debugger_node_id = 2
    registry01: register.Registry = make_registry(2, use_all_interfaces=True)
    while True:
        try:
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
        except OSError:
            await asyncio.sleep(2)
            printed_interface = registry01["uavcan.can.iface"]
            print(f"Debugger is trying to reconnect to {printed_interface}")


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run_debugger_node(True))
    except KeyboardInterrupt:
        pass
