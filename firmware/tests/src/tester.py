#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import time
import typing

import pathlib
import sys

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
print(f"Namespace path: {namespace_path.absolute()}")
sys.path.insert(0, namespace_path.absolute())

import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo, register
from pyuavcan.presentation._presentation import MessageClass

from _await_wrap import wrap_await
from allocator import OneTimeAllocator

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
import reg.drone.physics.acoustics.Note_0_1


def make_registry(node_id: int):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = "socketcan:slcan0"
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = node_id
    return registry01


import pytest

sapog_name = "io.px4.sapog"


def node_name():
    return sapog_name


@pytest.fixture(scope='session')
def get_nodes():
    registry01 = make_registry(8)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.preparer"), registry01) as node:
        node.make_subscriber()


hw_id_type = typing.Union[typing.List[int], bytes, bytearray]


def configure_note_register():
    print(reg.drone.physics.acoustics.Note_0_1)


def allocate_one_node_id(node_name):
    with OneTimeAllocator(node_name) as allocator:
        wrap_await(asyncio.wait_for(allocator.one_node_allocated_event.wait(), 3))
        return allocator.allocated_node_id, allocator.allocated_node_name


import subprocess


def unplug_power_automatic():
    subprocess.run(["/usr/bin/env", "-S", "groom_power.py", "outputoff"])


def plug_in_power_automatic():
    subprocess.run(["/usr/bin/env", "-S", "groom_power.py", "-v", "15"])


def unplug_power():
    unplug_power_automatic()


def plug_in_power():
    plug_in_power_automatic()


def unplug_power_manual():
    subprocess.run(["xterm", "-e", "bash", "-c", "echo Unplug power to boards and press enter when done; read line"])


def plug_in_power_manual():
    subprocess.run(["xterm", "-e", "bash", "-c", "echo Plug in power for boards and press enter when done; read line"])


@pytest.fixture()
def resource():
    print("setup")
    unplug_power()
    plug_in_power()
    yield allocate_nr_of_nodes(2)
    print("teardown")
    unplug_power()


@pytest.fixture()
def empty_resource():
    print("setup")
    unplug_power()
    plug_in_power()
    yield None
    print("teardown")
    unplug_power()


from my_simple_test_allocator import allocate_nr_of_nodes


class TestSapog:
    # def test_write_register(self):
    #     return
    #     target_node_id, target_node_name = allocate_one_node_id(node_name)
    #     registry01 = make_registry(3)
    #     with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
    #         service_client = node.make_client(uavcan.register.Access_1_0, target_node_id)
    #         msg = uavcan.register.Access_1_0.Request()
    #         my_array = uavcan.primitive.array.Integer64_1_0()
    #         my_array.value = [1]
    #         msg.name.name = "uavcan_node_id"
    #         msg.value.integer64 = my_array
    #         response = wrap_await(asyncio.wait_for(service_client.call(msg), 0.5))
    #         assert response is not None

    # def test_esc_spin_2_seconds(self):
    #     pass

    @staticmethod
    def test_allows_allocation_of_node_id(empty_resource):
        try:
            required_amount = 2
            result = allocate_nr_of_nodes(required_amount)
            assert len(result.keys()) == required_amount
        except TimeoutError:
            assert False

    @staticmethod
    def test_restart_node(resource):
        for node_id in resource.keys():
            registry01 = make_registry(3)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                service_client = node.make_client(uavcan.node.ExecuteCommand_1_1, node_id)
                msg = uavcan.node.ExecuteCommand_1_1.Request()
                msg.command = msg.COMMAND_RESTART
                response = wrap_await(service_client.call(msg))
                node.close()
                assert response is not None

    @staticmethod
    def test_has_heartbeat(resource):
        for node_id in resource.keys():
            try:
                registry01 = make_registry(3)
                with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                    subscriber = node.make_subscriber(uavcan.node.Heartbeat_1_0)
                    event = asyncio.Event()

                    def hb_handler(message_class: MessageClass,
                                   transfer_from: pyuavcan.transport._transfer.TransferFrom):
                        if transfer_from.source_node_id == node_id:
                            event.set()

                    subscriber.receive_in_background(hb_handler)
                    wrap_await(asyncio.wait_for(event.wait(), 1.7))
                    assert True
            except TimeoutError:
                assert False


if __name__ == "__main__":
    configure_note_register()
