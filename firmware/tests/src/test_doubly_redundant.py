import asyncio
import time
import typing

from _await_wrap import wrap_await
from utils import make_access_request, configure_a_port_on_sapog, rpm_to_radians_per_second, prepared_node, \
    prepared_sapogs, restarted_sapogs, restart_node, configure_registers, command_save
from imports import add_deps

add_deps()
import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1
import reg.udral.service.actuator.common.sp.Scalar_0_1
import uavcan.primitive.array.Bit_1_0
import uavcan.register.Value_1_0

from register_pair_class import RegisterPair, OnlyEmbeddedDeviceRegister
import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo, register
from pyuavcan.presentation._presentation import MessageClass
import subprocess
from utils import is_running_on_my_laptop, prepared_double_redundant_node


def set_interface_online(interface_name: str, online: bool):
    if online:
        online_string = "up"
    else:
        online_string = "down"
    if is_running_on_my_laptop:
        subprocess.run(["xterm", "-e", "bash", "-c", f"sudo ifconfig {interface_name} {online_string}; read line"])
    else:
        subprocess.run(["sudo", "ifconfig", interface_name, online_string])


def test_double_redundancy(prepared_double_redundant_node, prepared_sapogs):
    assert len(prepared_sapogs.keys()) > 0
    for node_id in prepared_sapogs.keys():
        subscriber = prepared_double_redundant_node.make_subscriber(uavcan.node.Heartbeat_1_0)
        event = asyncio.Event()

        def hb_handler(message_class: MessageClass,
                       transfer_from: pyuavcan.transport._transfer.TransferFrom):
            if transfer_from.source_node_id == node_id:
                event.set()

        set_interface_online("slcan0", True)
        set_interface_online("slcan1", True)
        try:
            subscriber.receive_in_background(hb_handler)
            wrap_await(asyncio.wait_for(event.wait(), 1.7))
        except TimeoutError:
            assert False
            return
        set_interface_online("slcan0", False)
        set_interface_online("slcan1", True)
        try:
            subscriber.receive_in_background(hb_handler)
            wrap_await(asyncio.wait_for(event.wait(), 1.7))
        except TimeoutError:
            assert False
            return
        set_interface_online("slcan0", True)
        set_interface_online("slcan1", False)
        try:
            subscriber.receive_in_background(hb_handler)
            wrap_await(asyncio.wait_for(event.wait(), 1.7))
        except TimeoutError:
            assert False
            return
        # This is supposed to timeout for a successful test
        set_interface_online("slcan0", False)
        set_interface_online("slcan1", False)
        try:
            subscriber.receive_in_background(hb_handler)
            wrap_await(asyncio.wait_for(event.wait(), 1.1))
        except TimeoutError:
            assert True
            return
