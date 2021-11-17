"""This port.List test is in its own file because it is really slow to execute, port list is supposed to be published
every 5 seconds on Sapog so that's the maximum amount of time that has to be waited to verify if it works."""
from _await_wrap import wrap_await
import asyncio
from test import restarted_sapogs
from test import fix_imports
from test import make_registry

fix_imports()
import pyuavcan
from pyuavcan.presentation._presentation import MessageClass
from pyuavcan.application import Node, make_node, NodeInfo, register
import uavcan.node.ID_1_0
import uavcan.node.port


def test_port_list(restarted_sapogs):
    """It is possible to create a new node for this test run because the sapogs that it tests are restarted."""
    for node_id in restarted_sapogs.keys():
        try:
            registry01 = make_registry(3)
            with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
                subscriber = node.make_subscriber(uavcan.node.port.List_0_1)
                event = asyncio.Event()

                def handler(message_class: MessageClass,
                            transfer_from: pyuavcan.transport._transfer.TransferFrom):
                    if transfer_from.source_node_id == node_id:
                        event.set()

                subscriber.receive_in_background(handler)
                wrap_await(asyncio.wait_for(event.wait(), 5.1))
                assert True
        except TimeoutError:
            assert False
