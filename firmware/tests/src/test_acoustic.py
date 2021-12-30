#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import os

import pytest
import time
import typing

from utils import configure_a_port_on_sapog, prepared_sapogs, prepared_node, restarted_sapogs

is_running_on_my_laptop = os.path.exists("/home/silver")

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
import reg.udral.physics.acoustics.Note_0_1
import reg.udral.service.common.Readiness_0_1

import pyuavcan
from pyuavcan.application import Node, register

from _await_wrap import wrap_await

sapog_name = "io.px4.sapog"


def node_name():
    return sapog_name


hw_id_type = typing.Union[typing.List[int], bytes, bytearray]


def configure_note_register():
    print(reg.drone.physics.acoustics.Note_0_1)


import subprocess


async def play_note(frequency, duration, prepared_node):
    note_message = reg.udral.physics.acoustics.Note_0_1(
        frequency=uavcan.si.unit.frequency.Scalar_1_0(frequency),
        acoustic_power=uavcan.si.unit.power.Scalar_1_0(1),
        duration=uavcan.si.unit.duration.Scalar_1_0(duration))
    publisher = prepared_node.make_publisher(reg.udral.physics.acoustics.Note_0_1, "note_response")
    await publisher.publish(note_message)


class TestFun:
    @staticmethod
    @pytest.mark.asyncio
    async def test_assign_port_for_note_acoustics(prepared_node, prepared_sapogs):
        # During this test, we need to save the configuration
        # But we don't want to save any other configuration
        # that could have been left on the device during tests,
        # we only care about saving the configuration for
        # the uavcan.pub.note_response.id configurable port.
        # Restarting to lose any other configuration.
        configure_a_port_on_sapog("note_response", 135, prepared_sapogs, prepared_node)
        arps = [[(196.00, 0.05), (246.94, 0.05), (293.66, 0.2)]]
        for arp in arps:
            for i in range(1):
                for frequency, duration in arp:
                    play_note(frequency, duration, prepared_node)
                    time.sleep(duration)


import uavcan.si.unit.angular_velocity.Scalar_1_0
