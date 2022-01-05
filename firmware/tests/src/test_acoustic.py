#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import os

import pytest
import typing

from RegisterPair import RegisterPair
from my_simple_test_allocator import make_simple_node_allocator
from utils import configure_a_port_on_sapog, prepared_sapogs, restarted_sapogs, configure_tester_side_registers, \
    configure_embedded_registers, command_save, restart_node

from node_fixtures.drnf import prepared_double_redundant_node

is_running_on_my_laptop = os.path.exists("/home/silver")

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
import reg.udral.physics.acoustics.Note_0_1
import reg.udral.service.common.Readiness_0_1

sapog_name = "io.px4.sapog"


def node_name():
    return sapog_name


hw_id_type = typing.Union[typing.List[int], bytes, bytearray]


def configure_note_register():
    print(reg.drone.physics.acoustics.Note_0_1)


async def play_note(frequency, duration, tester_node):
    note_message = reg.udral.physics.acoustics.Note_0_1(
        frequency=uavcan.si.unit.frequency.Scalar_1_0(frequency),
        acoustic_power=uavcan.si.unit.power.Scalar_1_0(1),
        duration=uavcan.si.unit.duration.Scalar_1_0(duration))
    publisher = tester_node.make_publisher(reg.udral.physics.acoustics.Note_0_1, "note_response")
    await publisher.publish(note_message)


class TestAcoustics:
    @staticmethod
    @pytest.mark.asyncio
    async def test_play_acoustic_note(prepared_double_redundant_node):
        tester_node = prepared_double_redundant_node
        common_registers = [
            RegisterPair("uavcan.pub.note_response.id", "uavcan.sub.note_response.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([180])), None,
                         None),
        ]
        our_allocator = make_simple_node_allocator()
        node_info_list = await our_allocator(2, node_to_use=tester_node)
        configure_tester_side_registers(common_registers, tester_node, append_counter=False)
        await configure_embedded_registers(common_registers, tester_node, 21)
        await configure_embedded_registers(common_registers, tester_node, 22)
        arps = [[(196.00, 0.05), (246.94, 0.05), (293.66, 0.2)]]
        await command_save(tester_node, 21)
        await command_save(tester_node, 22)
        if await restart_node(tester_node, 21) is None:
            assert False, f"Node {21} couldn't be restarted"
        if await restart_node(tester_node, 22) is None:
            assert False, f"Node {21} couldn't be restarted"
        await asyncio.sleep(1)
        our_allocator = make_simple_node_allocator()
        node_info_list = await our_allocator(2, node_to_use=tester_node)
        await asyncio.sleep(2)
        for arp in arps:
            for i in range(2):
                for frequency, duration in arp:
                    await play_note(frequency, duration, tester_node)
                    await asyncio.sleep(duration)
