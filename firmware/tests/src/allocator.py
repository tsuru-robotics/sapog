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
from abc import ABC
from asyncio import Event
from typing import Optional
from itertools import chain

import pyuavcan.dsdl
import typing

from pyuavcan.application._node_factory import SimpleNode
from pyuavcan.dsdl import FixedPortObject

from _await_wrap import wrap_await

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


hw_id_type = typing.Union[typing.List[int], bytes, bytearray]


class OneTimeAllocator(Allocator, ABC):
    """This class is used for testing if allocation works on Sapog

    It creates a Node that will be used as an allocator."""

    def __init__(self, node_id: str):
        self._complex_node_utilities = wrap_await(make_complex_node(node_id))
        self.node = self.complex_node_utilities.node

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.node.close()

    async def allocate_one_node(self, target_hw_id: hw_id_type):
        """Returns and event that can be waited for."""
        one_node_allocated_event = asyncio.Event()

        def get_info_handler_wrapper(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
            async def get_info_handler():
                if node_id and next_entry and next_entry.info is not None:
                    print("Allocating one node")
                    self._complex_node_utilities.centralized_allocator.register_node(node_id,
                                                                                     bytes(next_entry.info.unique_id))
                    one_node_allocated_event.set()

            asyncio.get_event_loop().create_task(get_info_handler())


get_info_handler_type = typing.Callable[[int, Optional[Entry], Optional[Entry]], None]
get_info_handler_wrapper_type = Optional[typing.Callable[[Allocator, Event], get_info_handler_type]]
capture_handler_type = typing.Callable[[_tracer.Capture], None]
capture_handler_wrapper_type = Optional[
    typing.Callable[[Tracer, typing.Dict[int, FixedPortObject]], capture_handler_type]]


class ComplexNodeUtilities:
    """node, centralized_allocator, node_tracker and tracer to return from functions"""

    def __init__(self, node: Node, centralized_allocator: Allocator, tracker: NodeTracker, tracer: Tracer):
        self._node = node
        self._centralized_allocator = centralized_allocator
        self._tracker = tracker
        self._tracer = tracer

    @property
    def node(self):
        return self._node

    @property
    def centralized_allocator(self):
        return self._centralized_allocator

    @property
    def tracker(self):
        return self._tracker

    @property
    def tracer(self):
        return self._tracer


async def make_one_time_allocator(node_id: str, target_hw_id: hw_id_type):
    pass


async def make_allocator(node_id: str):
    complex_node_utilities = await make_complex_node(node_id)
    complex_node_utilities.tracker.add_update_handler(
        make_handler_for_getinfo_update(complex_node_utilities.tracker.centralized_allocator, None))


async def make_complex_node(node_id: str,
                            get_info_handler_wrapper: get_info_handler_wrapper_type = None,
                            capture_handler_wrapper: capture_handler_wrapper_type = None,
                            with_debugging=False,
                            interface: str = "socketcan:slcan0", mtu: str = "8", name: str = "Just a node") -> Node:
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = interface
    registry01["uavcan.can.mtu"] = int(mtu)
    registry01["uavcan.node.id"] = int(node_id)
    ids = get_ids()
    node = make_node(NodeInfo(name=name), registry01)
    tracer = node.presentation.transport.make_tracer()
    if with_debugging and capture_handler_wrapper:
        node.presentation.transport.begin_capture(capture_handler_wrapper(tracer, ids))
    node_tracker = NodeTracker(node)
    centralized_allocator = CentralizedAllocator(node)
    if get_info_handler_wrapper:
        node_tracker.add_update_handler(get_info_handler_wrapper(centralized_allocator, None))
    return ComplexNodeUtilities(node, centralized_allocator, node_tracker, tracer)


async def run_allocator2(time_out: Optional[int] = None):
    event = asyncio.Event()
    complex_node = make_complex_node("com.zubax.sapog.tests.allocator",
                                     get_info_handler_wrapper=make_handler_for_getinfo_update,
                                     capture_handler_wrapper=make_capture_handler)

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
