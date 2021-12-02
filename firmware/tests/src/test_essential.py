import asyncio
import os
import time

from my_simple_test_allocator import allocate_nr_of_nodes
from utils import is_device_with_node_id_running, restart_node, make_registry
from utils import prepared_sapogs, prepared_node, prepared_double_redundant_node

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


class TestEssential:
    @staticmethod
    def test_allows_allocation_of_node_id(prepared_double_redundant_node):
        if restart_node(prepared_double_redundant_node, 21):
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
                registry01 = make_registry(3, True)
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
