#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import math
import os
import time
import typing

import pathlib
import sys
from asyncio import exceptions

is_running_on_my_laptop = os.path.exists("/home/silver")


def fix_imports():
    source_path = pathlib.Path(__file__).parent.absolute()
    dependency_path = source_path.parent / "deps"
    namespace_path = dependency_path / "namespaces"
    print(f"Namespace path: {namespace_path.absolute()}")
    sys.path.insert(0, str(namespace_path.absolute()))


fix_imports()
import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
import reg.udral.physics.acoustics.Note_0_1

import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo, register
from pyuavcan.presentation._presentation import MessageClass

from _await_wrap import wrap_await
from allocator import OneTimeAllocator


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
    global is_running_on_my_laptop
    if is_running_on_my_laptop:
        unplug_power_manual()
    else:
        unplug_power_automatic()


def plug_in_power():
    global is_running_on_my_laptop
    if is_running_on_my_laptop:
        plug_in_power_manual()
    else:
        plug_in_power_automatic()


def unplug_power_manual():
    subprocess.run(["xterm", "-e", "bash", "-c", "echo Unplug power to boards and press enter when done; read line"])


def plug_in_power_manual():
    subprocess.run(["xterm", "-e", "bash", "-c", "echo Plug in power for boards and press enter when done; read line"])


def is_device_with_node_id_running(node_id):
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


from debugger import format_payload_hex_view


@pytest.fixture()
def resource():
    global is_running_on_my_laptop
    print(f"is_running_on_my_laptop: {is_running_on_my_laptop}")
    fix_imports()

    if not is_running_on_my_laptop:
        unplug_power()
        plug_in_power()
        time.sleep(4)

    if is_device_with_node_id_running(21) and is_running_on_my_laptop:
        print("Device with node id 21 is already running so I will use that.")
        yield {21: "idk"}
    else:
        yield allocate_nr_of_nodes(1)


@pytest.fixture()
def empty_resource():
    global is_running_on_my_laptop
    fix_imports()
    unplug_power()
    plug_in_power()
    if not is_running_on_my_laptop:
        time.sleep(4)
    yield None
    unplug_power()


from my_simple_test_allocator import allocate_nr_of_nodes


class TestSapog:
    @staticmethod
    def test_write_supported_sapog_register_int(resource):
        time.sleep(1)
        for node_id in resource.keys():  # resource.keys():
            registry01 = make_registry(7)

            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                service_client = node.make_client(uavcan.register.Access_1_0, node_id)
                msg = uavcan.register.Access_1_0.Request()
                msg.value = uavcan.register.Value_1_0(integer64=uavcan.primitive.array.Integer64_1_0(60001))
                msg.name.name = "mot_pwm_hz"
                time.sleep(0.5)
                response = wrap_await(service_client.call(msg))
                print(f"Response fragmented payload: {format_payload_hex_view(response[1].fragmented_payload)}")
                print(response)
                if response:
                    int_value = response[0].value.integer64
                    if int_value:
                        if int_value.value.size == 1:
                            returned_value = response[0].value.integer64.value.tolist()[0]
                            print(type(returned_value))
                            assert returned_value == 60001
                        else:
                            print(f"Size should be 1 but is {int_value.value.size}")
                    else:
                        print("response[0].value.bit is None")
                else:
                    print("Response is None")
                msg = uavcan.register.Access_1_0.Request()
                msg.value = uavcan.register.Value_1_0(integer64=uavcan.primitive.array.Integer64_1_0(60000))
                msg.name.name = "mot_pwm_hz"
                time.sleep(0.5)
                response = wrap_await(service_client.call(msg))
                print(f"Response fragmented payload: {format_payload_hex_view(response[1].fragmented_payload)}")
                print(response)
                if response:
                    int_value = response[0].value.integer64
                    if int_value:
                        if int_value.value.size == 1:
                            returned_value = response[0].value.integer64.value.tolist()[0]
                            print(type(returned_value))
                            assert returned_value == 60000
                            return
                        else:
                            print(f"Size should be 1 but is {int_value.value.size}")
                    else:
                        print("response[0].value.bit is None")
                else:
                    print("Response is None")
                assert False

    @staticmethod
    def test_write_supported_sapog_register_bit(resource):
        time.sleep(1)
        for node_id in resource.keys():  # resource.keys():
            registry01 = make_registry(7)

            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                service_client = node.make_client(uavcan.register.Access_1_0, node_id)
                msg = uavcan.register.Access_1_0.Request()
                msg.value = uavcan.register.Value_1_0(integer32=uavcan.primitive.array.Integer32_1_0(0))
                msg.name.name = "pwm_enable"
                time.sleep(0.5)
                response = wrap_await(service_client.call(msg))
                print(f"Response fragmented payload: {format_payload_hex_view(response[1].fragmented_payload)}")
                print(response)
                if response:
                    bit_value = response[0].value.bit
                    if bit_value:
                        if bit_value.value.size == 1:
                            returned_value = response[0].value.bit.value.tolist()[0]
                            print(type(returned_value))
                            if returned_value:
                                assert True
                                return
                            else:
                                print(f"Returned value should be 1 but is {returned_value}")
                        else:
                            print(f"Size should be 1 but is {bit_value.value.size}")
                    else:
                        print("response[0].value.bit is None")
                else:
                    print("Response is None")
                assert False

    @staticmethod
    def test_read_existing_register_float(resource):
        time.sleep(1)
        for node_id in resource.keys():  # resource.keys():
            registry01 = make_registry(7)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                service_client = node.make_client(uavcan.register.Access_1_0, node_id)
                msg = uavcan.register.Access_1_0.Request()
                msg.value = uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0())
                msg.name.name = "rpmctl_p"
                time.sleep(0.5)
                response = wrap_await(service_client.call(msg))
                print(f"Response fragmented payload: {format_payload_hex_view(response[1].fragmented_payload)}")
                print(response)
                if response:
                    real_value = response[0].value.real64
                    if real_value:
                        if real_value.value.size == 1:
                            returned_value = response[0].value.real64.value.tolist()[0]
                            print(type(returned_value))
                            assert math.isclose(returned_value, 0.000099999, abs_tol=1e-09)
                            return
                        else:
                            print(f"Size should be 1 but is {real_value.value.size}")
                    else:
                        print("response[0].value.real is None")
                else:
                    print("Response is None")
                assert False

    @staticmethod
    def test_read_existing_register_bool(resource):
        time.sleep(1)
        for node_id in resource.keys():  # resource.keys():
            registry01 = make_registry(7)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                service_client = node.make_client(uavcan.register.Access_1_0, node_id)
                msg = uavcan.register.Access_1_0.Request()
                msg.value = uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0())
                msg.name.name = "pwm_enable"
                time.sleep(0.5)
                response = wrap_await(service_client.call(msg))
                print(f"Response fragmented payload: {format_payload_hex_view(response[1].fragmented_payload)}")
                print(response)
                if response:
                    real_value = response[0].value.real64
                    if real_value:
                        if real_value.value.size == 1:
                            returned_value = response[0].value.bit.value.tolist()[0]
                            print(type(returned_value))
                            assert math.isclose(returned_value, 0.000099999, abs_tol=1e-09)
                            return
                        else:
                            print(f"Size should be 1 but is {real_value.value.size}")
                    else:
                        print("response[0].value.real is None")
                else:
                    print("Response is None")
                assert False

    @staticmethod
    def test_read_existing_register_int(resource):
        time.sleep(1)
        for node_id in resource.keys():  # resource.keys():
            registry01 = make_registry(7)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                service_client = node.make_client(uavcan.register.Access_1_0, node_id)
                msg = uavcan.register.Access_1_0.Request()
                msg.value = uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0())
                msg.name.name = "mot_tim_adv_min"
                time.sleep(0.5)
                response = wrap_await(service_client.call(msg))
                print(f"Response fragmented payload: {format_payload_hex_view(response[1].fragmented_payload)}")
                print(response)
                if response:
                    real_value = response[0].value.integer64
                    if real_value:
                        if real_value.value.size == 1:
                            returned_value = response[0].value.integer64.value.tolist()[0]
                            print(type(returned_value))
                            assert math.isclose(returned_value, 5, abs_tol=1e-09)
                            return
                        else:
                            print(f"Size should be 1 but is {real_value.value.size}")
                    else:
                        print("response[0].value.real is None")
                else:
                    print("Response is None")
                assert False

    @staticmethod
    def test_write_unsupported_sapog_register(resource):
        time.sleep(1)
        for node_id in resource.keys():  # resource.keys():
            registry01 = make_registry(7)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                service_client = node.make_client(uavcan.register.Access_1_0, node_id)
                msg = uavcan.register.Access_1_0.Request()
                msg.value = uavcan.register.Value_1_0(string=uavcan.primitive.String_1_0("named"))
                msg.name.name = "uavcan.node.description"
                time.sleep(0.5)
                response = wrap_await(service_client.call(msg))
                print(response)
                is_result_good = response is not None and response[0].value.empty is not None
                assert is_result_good

    # def test_esc_spin_2_seconds(self):
    #     pass

    @staticmethod
    def test_allows_allocation_of_node_id(empty_resource):
        try:
            required_amount = 1
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
