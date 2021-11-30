import asyncio
import os
import re
import subprocess
import time
import typing

from asyncio import exceptions

import pytest

from allocator import OneTimeAllocator
from my_simple_test_allocator import allocate_nr_of_nodes
from register_pair_class import RegisterPair

is_running_on_my_laptop = os.path.exists("/home/silver")

from imports import add_deps

add_deps()

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo, register
from pyuavcan.presentation._presentation import MessageClass

from _await_wrap import wrap_await


def is_device_with_node_id_running(node_id):
    """This creates a new node with node_id 3 that will look for heart beats from node_id."""
    registry01 = make_registry(3)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
        subscriber = node.make_subscriber(uavcan.node.Heartbeat_1_0)
        event = asyncio.Event()

        def hb_handler(message_class: MessageClass,
                       transfer_from: pyuavcan.transport._transfer.TransferFrom):
            if transfer_from.source_node_id == node_id:
                event.set()

        subscriber.receive_in_background(hb_handler)
        try:
            wrap_await(asyncio.wait_for(event.wait(), 1.7))
        except exceptions.TimeoutError as e:
            return False
        return True


@pytest.fixture(scope="class")
def prepared_node():
    registry01 = make_registry(7)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


@pytest.fixture(scope="class")
def prepared_double_redundant_node():
    registry01 = make_registry(7, redundant=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


@pytest.fixture(scope="class")
def prepared_sapogs():
    if is_device_with_node_id_running(21) and is_running_on_my_laptop:
        print("Device with node id 21 is already running so I will use that.")
        return {21: "idk"}
    else:
        return allocate_nr_of_nodes(1)  # This will allocate id 21 too


@pytest.fixture()
def restarted_sapogs():
    global is_running_on_my_laptop
    return allocate_nr_of_nodes(1)


def make_registry(node_id: int, redundant=False):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    if redundant:
        added_string = " socketcan:slcan1"
    else:
        added_string = ""
    registry01["uavcan.can.iface"] = "socketcan:slcan0" + added_string
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = node_id
    return registry01


def restart_node(prepared_node, node_id_to_restart):
    service_client = prepared_node.make_client(uavcan.node.ExecuteCommand_1_1, node_id_to_restart)
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_RESTART
    response = wrap_await(service_client.call(msg))
    return response


def rpm_to_radians_per_second(rpm: int):
    rps = rpm / 60
    radians_per_second = rps * 3.14 * 2
    return radians_per_second


def make_access_request(reg_name, reg_value, target_node_id, prepared_node):
    service_client = prepared_node.make_client(uavcan.register.Access_1_0, target_node_id)
    service_client.response_timeout = 1
    msg = uavcan.register.Access_1_0.Request()
    msg.name.name = reg_name
    msg.value = reg_value
    return wrap_await(service_client.call(msg))


def configure_registers(regs: typing.List[RegisterPair], prepared_node, prepared_sapogs):
    for pair in regs:
        assert isinstance(pair, RegisterPair)
        if pair.tester_reg_name:
            prepared_node.registry[pair.tester_reg_name] = pair.value
        if pair.embedded_device_reg_name:
            for node_id in prepared_sapogs:
                make_access_request(pair.embedded_device_reg_name, pair.value,
                                    node_id, prepared_node)


def allocate_one_node_id(node_name):
    with OneTimeAllocator(node_name) as allocator:
        wrap_await(asyncio.wait_for(allocator.one_node_allocated_event.wait(), 3))
        return allocator.allocated_node_id, allocator.allocated_node_name


def unplug_power():
    global is_running_on_my_laptop
    if is_running_on_my_laptop:
        unplug_power_manual()
    else:
        unplug_power_automatic()


def unplug_power_manual():
    """Yields with a \"dialog\" open for the user to close with enter when the requested action is done."""
    subprocess.run(["xterm", "-e", "bash", "-c", "echo Unplug power to boards and press enter when done; read line"])


def plug_in_power_manual():
    """Yields with a \"dialog\" open for the user to close with enter when the requested action is done."""
    subprocess.run(["xterm", "-e", "bash", "-c", "echo Plug in power for boards and press enter when done; read line"])


def unplug_power_automatic():
    subprocess.run(["/usr/bin/env", "-S", "groom_power.py", "outputoff"])


def plug_in_power_automatic():
    subprocess.run(["/usr/bin/env", "-S", "groom_power.py", "-v", "15"])


def plug_in_power():
    global is_running_on_my_laptop
    if is_running_on_my_laptop:
        plug_in_power_manual()
    else:
        plug_in_power_automatic()


def command_save(prepared_node, node_id):
    command_client = prepared_node.make_client(uavcan.node.ExecuteCommand_1_1, node_id)
    command_client.response_timeout = 1
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_STORE_PERSISTENT_STATES
    wrap_await(command_client.call(msg))


def configure_a_port_on_sapog(name, subject_id, prepared_sapogs, prepared_node):
    for node_id in prepared_sapogs.keys():
        if restart_node(node_id):
            time.sleep(4)
        else:
            assert False
            return
    result = allocate_nr_of_nodes(len(prepared_sapogs.keys()))
    time.sleep(1)
    assert len(result.keys()) == len(prepared_sapogs.keys())
    prepared_node.registry[f"uavcan.pub.{name}.id"] = subject_id
    assert len(prepared_sapogs.keys()) > 0
    for node_id in prepared_sapogs.keys():
        make_access_request(f"uavcan.sub.{name}.id",
                            uavcan.register.Value_1_0(integer64=uavcan.primitive.array.Integer64_1_0(subject_id)),
                            node_id,
                            prepared_node)
        command_save(prepared_node, node_id)
        if restart_node(21):
            time.sleep(3)
            result = allocate_nr_of_nodes(len(prepared_sapogs.keys()))
        else:
            assert False
            return
