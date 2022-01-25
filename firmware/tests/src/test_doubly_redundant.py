import asyncio

import pytest

from my_simple_test_allocator import make_simple_node_allocator

import uavcan.primitive.array.Integer64_1_0
import uavcan.primitive.array.Bit_1_0
import uavcan.register.Value_1_0
from util.get_available_interfaces import get_available_slcan_interfaces

import pyuavcan
from pyuavcan.presentation._presentation import MessageClass
import subprocess
from utils import is_running_on_my_laptop
from node_fixtures.drnf import prepared_double_redundant_node, prepared_node


def set_interface_online(interface_name: str, online: bool):
    if online:
        online_string = "up"
    else:
        online_string = "down"
    if is_running_on_my_laptop:
        subprocess.run(["xterm", "-e", "bash", "-c", f"sudo ifconfig {interface_name} {online_string}; read line"])
    else:
        subprocess.run(["sudo", "ifconfig", interface_name, online_string])


@pytest.mark.asyncio
async def test_double_redundancy(prepared_double_redundant_node):
    # We shouldn't expect double redundancy to work when only one interface is available
    if len(get_available_slcan_interfaces()) == 1:
        assert True
        return
    node = prepared_double_redundant_node
    our_allocator = make_simple_node_allocator()
    node_info_list = await our_allocator(2, node_to_use=node)
    for node_info in node_info_list:
        subscriber = node.make_subscriber(uavcan.node.Heartbeat_1_0)
        event = asyncio.Event()

        async def hb_handler(message_class: MessageClass,
                             transfer_from: pyuavcan.transport._transfer.TransferFrom):
            if transfer_from.source_node_id == node_info.node_id:
                event.set()

        set_interface_online("slcan0", True)
        set_interface_online("slcan1", True)
        try:
            subscriber.receive_in_background(hb_handler)
            await asyncio.wait_for(event.wait(), 1.7)
        except TimeoutError:
            assert False
            return
        set_interface_online("slcan0", False)
        set_interface_online("slcan1", True)
        try:
            subscriber.receive_in_background(hb_handler)
            await asyncio.wait_for(event.wait(), 1.7)
        except TimeoutError:
            assert False
            return
        set_interface_online("slcan0", True)
        set_interface_online("slcan1", False)
        try:
            subscriber.receive_in_background(hb_handler)
            await asyncio.wait_for(event.wait(), 1.7)
        except TimeoutError:
            assert False
            return
        # This is supposed to timeout for a successful test
        set_interface_online("slcan0", False)
        set_interface_online("slcan1", False)
        try:
            subscriber.receive_in_background(hb_handler)
            await asyncio.wait_for(event.wait(), 1.1)
        except TimeoutError:
            assert True
            return
