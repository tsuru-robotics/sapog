import asyncio
import os
import time

from asyncio import exceptions

import pytest

from my_simple_test_allocator import allocate_nr_of_nodes

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


def make_registry(node_id: int):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = "socketcan:slcan0"
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = node_id
    return registry01


def restart_node(node_id_to_restart):
    registry01 = make_registry(3)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
        service_client = node.make_client(uavcan.node.ExecuteCommand_1_1, node_id_to_restart)
        msg = uavcan.node.ExecuteCommand_1_1.Request()
        msg.command = msg.COMMAND_RESTART
        response = wrap_await(service_client.call(msg))
        node.close()
        return response


class TestEssential:
    @staticmethod
    def test_allows_allocation_of_node_id():
        if restart_node(21):
            time.sleep(2)
        try:
            required_amount = 1
            result = allocate_nr_of_nodes(required_amount)
            assert len(result.keys()) == required_amount
        except TimeoutError:
            assert False

    @staticmethod
    def test_has_heartbeat(prepared_sapogs):
        assert len(prepared_sapogs.keys()) > 0
        for node_id in prepared_sapogs.keys():
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
