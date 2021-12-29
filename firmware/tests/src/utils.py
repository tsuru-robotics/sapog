import asyncio
import os
import subprocess
import time
import typing

from asyncio import exceptions

import pytest

import Nodes
from allocator import OneTimeAllocator
from my_simple_test_allocator import make_simple_node_allocator

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


def get_available_slcan_interfaces():
    result = subprocess.run(["netstat -i | tail -n +3 |cut -d\" \" -f1"], shell=True, stdout=subprocess.PIPE)
    list_of_interfaces = result.stdout.decode("utf-8").strip().split("\n")
    result_interfaces = []
    for interface_name in list_of_interfaces:
        if "slcan" in interface_name:
            result_interfaces.append("socketcan:" + interface_name)
    return result_interfaces


@pytest.fixture(scope="class")
def prepared_node():
    registry01 = make_registry(7)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


@pytest.fixture(scope="class")
def prepared_double_redundant_node():
    registry01 = make_registry(7)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


def get_interfaces_by_hw_id(do_get_allocated_nodes: bool = False, do_get_unallocated_nodes: bool = True,
                            do_allocate: bool = False) -> \
        typing.List[Nodes.NodeInfo]:
    """
    Makes a list of .

    This helps to automatically find out which devices are using which interfaces and then communicate to every device
    in a for loop to test these.
    """
    available_interfaces = get_available_slcan_interfaces()
    node_identifier_list: typing.List[Nodes.NodeInfo] = []

    def add_to_dictionary_list(hw_id, interface, node_id: typing.Optional[int]):
        """Used twice below, tested in duplicated code below"""
        filtered_list = filter(lambda node_identifier: node_identifier.hw_id == hw_id, node_identifier_list)
        if (next_item := next(filtered_list, None)) is not None:
            next_item.node_id = node_id
            next_item.interfaces.append(interface)
        else:
            next_item.node_id = node_id
            node_identifier_list.append(Nodes.NodeInfo(hw_id=hw_id, interfaces=[interface]))

    for index, interface in enumerate(available_interfaces):
        registry = make_registry(index, interfaces=[interface])
        node = make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry)
        done = False
        if do_allocate:
            make_simple_node_allocator(interface, node_to_use=node)(1)
        if do_get_unallocated_nodes:
            # Key is going to be a string
            sub = node.make_subscriber(uavcan.pnp.NodeIDAllocationData_1_0)
            received_tuple: uavcan.pnp.NodeIDAllocationData_1_0 = wrap_await(sub.receive_for(1.3))
            if not received_tuple:
                print(f"Interface {interface} did not receive the allocation request.")
                continue
            allocation_request, transfer_from = received_tuple
            add_to_dictionary_list(str(allocation_request.unique_id_hash), interface, transfer_from.source_node_id)
        if not done and do_get_allocated_nodes:
            # Key is going to be an int
            sub = node.make_subscriber(uavcan.node.Heartbeat_1_0)
            received_tuple: typing.Tuple[uavcan.node.Heartbeat_1_0, pyuavcan.transport.TransferFrom] = wrap_await(
                sub.receive_for(1.3))
            if not received_tuple:
                print(f"Interface {interface} did not receive a heartbeat.")
                continue
            heartbeat, transfer_from = received_tuple
            add_to_dictionary_list(transfer_from.source_node_id, interface, transfer_from.source_node_id)
    return node_identifier_list


def test_add_to_dictionary_list():
    interfaces_list = [Nodes.NodeInfo('75720222859564', ['socketcan:slcan0', 'socketcan:slcan1']),
                       Nodes.NodeInfo('205537128692115', ['socketcan:slcan2'])]

    def add_to_dictionary_list(key, value):
        """Used twice below"""
        filtered_list = filter(lambda node_identifier: node_identifier.hw_id == key, interfaces_list)
        if (next_item := next(filtered_list)) is not None:
            next_item.interfaces.append(value)
        else:
            assert False

    add_to_dictionary_list('75720222859564', "socks")
    assert interfaces_list == [Nodes.NodeInfo('75720222859564', ['socketcan:slcan0', 'socketcan:slcan1', "socks"]),
                               Nodes.NodeInfo('205537128692115', ['socketcan:slcan2'])]


def test_get_interfaces_by_hw_id():
    print(get_interfaces_by_hw_id())
    assert True


def prepared_all_devices(should_be_allocated: bool = False):
    from my_simple_test_allocator import make_simple_node_allocator
    interfaces_by_hw_id: typing.Dict[str, typing.List[str]] = get_interfaces_by_hw_id()
    if should_be_allocated:
        allocated_nodes = make_simple_node_allocator()(len(interfaces_by_hw_id.keys()))
    for key, interfaces_list in interfaces_by_hw_id.items():
        is_key_node_id = type(key) is int
        is_key_hw_id = type(key) is str
        if is_key_hw_id:
            pass
        elif is_key_node_id and should_be_allocated:
            registry = make_registry(0, interfaces=interfaces_list)
            node = make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry)
            service_client = node.make_client(uavcan.node.ExecuteCommand_1_1, key)
            msg = uavcan.node.ExecuteCommand_1_1.Request()
            msg.command = msg.COMMAND_RESTART
            response = wrap_await(service_client.call(msg))
            node.close()
            assert response is not None
    # Replace every hw_id with node_id if it is allocated because a node_id is more useful
    for hw_id in interfaces_by_hw_id.keys():
        for key, value in list(allocated_nodes.items()):
            if value == hw_id:
                interfaces_by_hw_id[key] = interfaces_by_hw_id[hw_id]
                interfaces_by_hw_id.pop(hw_id)
    return interfaces_by_hw_id


@pytest.fixture(scope="class")
def prepared_sapogs():
    from my_simple_test_allocator import make_simple_node_allocator
    if is_running_on_my_laptop and is_device_with_node_id_running(21):
        print("Device with node id 21 is already running so I will use that.")
        return {21: "idk"}
    else:
        print("Allocating one node")
        return make_simple_node_allocator()(1)  # This will allocate id 21 too


@pytest.fixture()
def restarted_sapogs():
    from my_simple_test_allocator import make_simple_node_allocator
    global is_running_on_my_laptop
    return make_simple_node_allocator()(1)


def make_registry(node_id: int, interfaces: typing.List[str], use_all_interfaces: bool = False):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    if use_all_interfaces:
        registry01["uavcan.can.iface"] = " ".join(get_available_slcan_interfaces())
    else:
        registry01["uavcan.can.iface"] = " ".join(interfaces)
    print("Using these interfaces: " + str(registry01["uavcan.can.iface"]))
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


def make_access_request(reg_name, reg_value, node_identifier: Nodes.NodeInfo, prepared_node):
    if node_identifier.node_id == 0xFFFF:
        print(f"Device {node_identifier.hw_id} cannot be configured, it is missing a node_id, please allocate it first")
        assert False
    service_client = prepared_node.make_client(uavcan.register.Access_1_0, node_identifier.node_id)
    service_client.response_timeout = 1
    msg = uavcan.register.Access_1_0.Request()
    msg.name.name = reg_name
    msg.value = reg_value
    return wrap_await(service_client.call(msg))


def configure_registers(regs: typing.List[RegisterPair], prepared_node, node_id):
    for pair in regs:
        assert isinstance(pair, RegisterPair)
        if pair.tester_reg_name:
            prepared_node.registry[pair.tester_reg_name] = pair.value
        if pair.embedded_device_reg_name:
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
    from my_simple_test_allocator import make_simple_node_allocator
    for node_id in prepared_sapogs.keys():
        if restart_node(prepared_node, node_id):
            time.sleep(4)
        else:
            assert False
            return
    result = make_simple_node_allocator()(len(prepared_sapogs.keys()))
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
        if restart_node(prepared_node, node_id):
            time.sleep(3)
            result = make_simple_node_allocator()(len(prepared_sapogs.keys()))
        else:
            assert False
            return


def test_interfaces_by_hardware_id():
    print(get_interfaces_by_hw_id())
    assert True
