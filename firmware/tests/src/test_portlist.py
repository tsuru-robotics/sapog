#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
"""This port.List test is in its own file because it is really slow to execute, port list is supposed to be published
every 5 seconds on Sapog so that's the maximum amount of time that has to be waited to verify if it works."""
import pytest

import asyncio
from utils import restarted_sapogs
from make_registry import make_registry

import pycyphal
from pycyphal.presentation._presentation import MessageClass
from pycyphal.application import Node, make_node, NodeInfo, register
import uavcan.node.ID_1_0
import uavcan.node.port


@pytest.mark.asyncio
async def test_port_list(restarted_sapogs):
    """It is possible to create a new node for this test run because the sapogs that it tests are restarted."""
    for node_id in restarted_sapogs.keys():
        try:
            registry01 = make_registry(3)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                subscriber = node.make_subscriber(uavcan.node.port.List_0_1)
                event = asyncio.Event()

                def handler(message_class: MessageClass,
                            transfer_from: pycyphal.transport._transfer.TransferFrom):
                    if transfer_from.source_node_id == node_id:
                        event.set()

                subscriber.receive_in_background(handler)
                await asyncio.wait_for(event.wait(), 5.1)
                assert True
        except TimeoutError:
            assert False
