import asyncio
import os
import typing

import pytest
import time

import my_simple_test_allocator
from my_simple_test_allocator import make_simple_node_allocator
from utils import is_device_with_node_id_running, restart_node, get_prepared_sapogs

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
    async def test_allows_allocation_of_node_id(prepared_double_redundant_node):
        tester_node = prepared_double_redundant_node
        asyncio.set_event_loop(asyncio.new_event_loop())
        our_allocator = make_simple_node_allocator()
        registry = make_registry(0, use_all_interfaces=True)
        tester = make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry)
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
    async def test_has_heartbeat(prepared_double_redundant_node):
        """This heartbeat test implies that node_id allocation works."""
        our_allocator = make_simple_node_allocator()
        result = await our_allocator(node_to_use=prepared_double_redundant_node, continuous=True, time_budget_seconds=2)
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(result) == len(prepared_sapogs), "Not all nodes are emitting heartbeats"

    @staticmethod
    @pytest.mark.asyncio
    async def test_responds_to_get_info(prepared_double_redundant_node: pyuavcan.application.Node,
                                        prepared_sapogs: typing.Dict[int, str]):
        pdrn = prepared_double_redundant_node
        for node_id in prepared_sapogs.keys():
            try:
                get_info_client = pdrn.make_client(uavcan.node.GetInfo_1_0, node_id)
                gi_request = uavcan.node.GetInfo_1_0.Request()
                assert await get_info_client.call(gi_request) is not None
            except TimeoutError:
                assert False
