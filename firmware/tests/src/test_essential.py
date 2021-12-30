import asyncio
import os
import typing

import pytest
import time

import my_simple_test_allocator
from my_simple_test_allocator import make_simple_node_allocator
from utils import is_device_with_node_id_running, restart_node, get_interfaces_by_hw_id, \
    get_available_slcan_interfaces
from utils import prepared_sapogs

from node_fixtures.drnf import prepared_node, prepared_double_redundant_node
from make_registry import make_registry

is_running_on_my_laptop = os.path.exists("/home/silver")

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo
from pyuavcan.presentation._presentation import MessageClass

from _await_wrap import wrap_await


class TestEssential:
    @staticmethod
    @pytest.mark.asyncio
    async def test_allows_allocation_of_node_id():
        asyncio.set_event_loop(asyncio.new_event_loop())
        nodes_info_list = get_interfaces_by_hw_id(do_get_unallocated_nodes=True, do_get_allocated_nodes=True,
                                                  do_allocate=False)
        our_allocator = make_simple_node_allocator()
        for index, node_info in enumerate(nodes_info_list):
            registry = make_registry(index, interfaces=node_info.interfaces)
            tester = make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry)
            if node_info.node_id and restart_node(tester, node_info.node_id):
                time.sleep(2)
            try:
                required_amount = 1
                result = await our_allocator(required_amount, node_to_use=tester)
                assert len(result) == required_amount
            except TimeoutError:
                assert False, f"Didn't allocate {required_amount} nodes in the time allotted"
            except Exception:
                assert False
            finally:
                tester.close()

    @staticmethod
    @pytest.mark.asyncio
    async def test_has_heartbeat():
        """This heartbeat test implies that node_id allocation works."""
        list_of_nodes_info = await make_simple_node_allocator()(1, )
        node_id_received_heartbeat = {}
        try:
            registry01 = make_registry(0)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                subscriber = node.make_subscriber(uavcan.node.Heartbeat_1_0)
                event = asyncio.Event()

                def hb_handler(message_class: MessageClass,
                               transfer_from: pyuavcan.transport._transfer.TransferFrom):
                    node_id_received_heartbeat[transfer_from.source_node_id] = True
                    if len(list(filter(node_id_received_heartbeat.values()))) == len(
                            list_of_nodes_info):
                        event.set()

                subscriber.receive_in_background(hb_handler)
                await asyncio.wait_for(event.wait(), 1.7)
        except TimeoutError:
            missing_heartbeats = len(list_of_nodes_info) - len(list(filter(node_id_received_heartbeat.values())))
            assert False, f"{missing_heartbeats} nodes do not have a heartbeat."

    @staticmethod
    def test_responds_to_get_info(prepared_double_redundant_node: pyuavcan.application.Node,
                                  prepared_sapogs: typing.Dict[int, str]):
        pdrn = prepared_double_redundant_node
        for node_id in prepared_sapogs.keys():
            try:
                get_info_client = pdrn.make_client(uavcan.node.GetInfo_1_0, node_id)
                gi_request = uavcan.node.GetInfo_1_0.Request()
                assert wrap_await(get_info_client.call(gi_request)) is not None
            except TimeoutError:
                assert False
