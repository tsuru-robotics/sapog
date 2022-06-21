#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import os
import subprocess

import time
import typing

from asyncio import exceptions

import pytest

import my_nodes
from allocator import OneTimeAllocator
from make_registry import make_registry

from RegisterPair import RegisterPair

is_running_on_my_laptop = os.path.exists("/home/silver")

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

import pycyphal
from pycyphal.application import Node, make_node, NodeInfo, register


async def is_device_with_node_id_running(node_id):
    """This creates a new node with node_id 3 that will look for heart beats from node_id."""
    registry01 = make_registry(3)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
        subscriber = node.make_subscriber(uavcan.node.Heartbeat_1_0)
        event = asyncio.Event()

        async def hb_handler(message_class,
                             transfer_from: pycyphal.transport._transfer.TransferFrom):
            if transfer_from.source_node_id == node_id:
                event.set()

        subscriber.receive_in_background(hb_handler)
        try:
            await asyncio.wait_for(event.wait(), 1.7)
        except exceptions.TimeoutError as e:
            return False
        return True


def test_add_to_dictionary_list():
    interfaces_list = [my_nodes.NodeInfo('75720222859564', ['socketcan:slcan0', 'socketcan:slcan1']),
                       my_nodes.NodeInfo('205537128692115', ['socketcan:slcan2'])]

    def add_to_dictionary_list(key, value):
        """Used twice below"""
        filtered_list = filter(lambda node_identifier: node_identifier.hw_id == key, interfaces_list)
        if (next_item := next(filtered_list)) is not None:
            next_item.interfaces.append(value)
        else:
            assert False

    add_to_dictionary_list('75720222859564', "socks")
    assert interfaces_list == [my_nodes.NodeInfo('75720222859564', ['socketcan:slcan0', 'socketcan:slcan1', "socks"]),
                               my_nodes.NodeInfo('205537128692115', ['socketcan:slcan2'])]


async def get_prepared_sapogs(prepared_node) -> typing.List[my_nodes.NodeInfo]:
    hb_sub = prepared_node.make_subscriber(uavcan.node.Heartbeat_1_0)
    allowed_listen_time = 1.5
    listen_start_time = time.time()
    recorded_node_ids = {}
    node_info_list: typing.List[my_nodes.NodeInfo] = []
    from pycyphal.transport import TransferFrom

    async def receive_heartbeat(heartbeat: uavcan.node.Heartbeat_1_0, sending_node: TransferFrom):
        if time.time() - listen_start_time <= allowed_listen_time and not recorded_node_ids.get(
                sending_node.source_node_id):
            recorded_node_ids[sending_node.source_node_id] = True
            node_info_list.append(my_nodes.NodeInfo(None, None, sending_node.source_node_id))

    hb_sub.receive_in_background(receive_heartbeat)
    await asyncio.sleep(allowed_listen_time + 1)
    return node_info_list


@pytest.fixture()
def restarted_sapogs():
    from my_simple_test_allocator import make_simple_node_allocator
    global is_running_on_my_laptop
    return make_simple_node_allocator()(1)


async def restart_node(node, node_id_to_restart):
    service_client = node.make_client(uavcan.node.ExecuteCommand_1_1, node_id_to_restart)
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_RESTART
    response = await service_client.call(msg)
    return response


def rpm_to_radians_per_second(rpm: int):
    rps = rpm / 60
    radians_per_second = rps * 3.14 * 2
    return radians_per_second


async def make_access_request(reg_name, reg_value, node_id: int,
                              node: pycyphal.application.Node):
    if not node_id or node_id == 0xFFFF:
        assert False, f"Device cannot be configured, it is missing a node_id, please allocate it first"
    service_client = node.make_client(uavcan.register.Access_1_0, node_id)
    service_client.response_timeout = 0.5
    msg = uavcan.register.Access_1_0.Request()
    msg.name.name = reg_name
    msg.value = reg_value
    return await service_client.call(msg)


def configure_tester_side_registers(regs: typing.List[RegisterPair], node: pycyphal.application.Node,
                                    append_counter: bool = True):
    for pair in regs:
        assert isinstance(pair, RegisterPair)
        if pair.tester_reg_name:
            if ".id" not in pair.tester_reg_name:
                if append_counter:
                    node.registry[f"{pair.tester_reg_name}_{pair.tester_side_counter_number}"] = pair.value
                    pair.tester_reg_name = f"{pair.tester_reg_name}_{pair.tester_side_counter_number}"
                else:
                    node.registry[f"{pair.tester_reg_name}"] = pair.value
                    pair.tester_reg_name = f"{pair.tester_reg_name}"
            else:
                node.registry[pair.tester_reg_name] = pair.value


async def configure_embedded_registers(regs: typing.List[RegisterPair], node: pycyphal.application.Node,
                                       node_id: int):
    for pair in regs:
        assert isinstance(pair, RegisterPair)
        if pair.embedded_device_reg_name:
            await make_access_request(pair.embedded_device_reg_name, pair.value, node_id, node)


async def allocate_one_node_id(node_name):
    with OneTimeAllocator(node_name) as allocator:
        await asyncio.wait_for(allocator.one_node_allocated_event.wait(), 3)
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


async def command_save(prepared_node, node_id):
    command_client = prepared_node.make_client(uavcan.node.ExecuteCommand_1_1, node_id)
    command_client.response_timeout = 1
    msg = uavcan.node.ExecuteCommand_1_1.Request()
    msg.command = msg.COMMAND_STORE_PERSISTENT_STATES
    await command_client.call(msg)
