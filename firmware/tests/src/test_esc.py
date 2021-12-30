import asyncio

import pytest
import pyuavcan
import time
import typing

from pyuavcan.application import make_node, NodeInfo

import my_nodes
import my_simple_test_allocator
from _await_wrap import wrap_await
from my_simple_test_allocator import make_simple_node_allocator
from utils import rpm_to_radians_per_second, restart_node, configure_registers, \
    command_save, make_registry, get_interfaces_by_hw_id

import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1
import reg.udral.service.actuator.common.sp.Scalar_0_1
import reg.udral.service.actuator.common.Feedback_0_1
import reg.udral.service.actuator.common.Status_0_1
import reg.udral.physics.electricity.PowerTs_0_1
import reg.udral.physics.dynamics.rotation.PlanarTs_0_1
import uavcan.primitive.array.Bit_1_0
import uavcan.register.Value_1_0

import time

from register_pair_class import RegisterPair, OnlyEmbeddedDeviceRegister


class TestESC:
    @staticmethod
    @pytest.mark.asyncio
    async def test_rpm_run_2_sec(prepared_double_redundant_node):
        our_allocator = make_simple_node_allocator()
        tester_node = prepared_double_redundant_node
        node_info_list = our_allocator(2, node_to_use=tester_node)
        registers_array: typing.List[RegisterPair] = [
            RegisterPair("uavcan.pub.setpoint.id", "uavcan.sub.setpoint.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(136))),
            # RegisterPair("uavcan.pub.radians_in_second_velocity.id", "uavcan.sub.radians_in_second_velocity.id",
            #              uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(136))),
            RegisterPair("uavcan.pub.readiness.id", "uavcan.sub.readiness.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(137))),
            OnlyEmbeddedDeviceRegister("control_mode_rpm",
                                       uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(value=[True]))),
            OnlyEmbeddedDeviceRegister("ttl_milliseconds",
                                       uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(300))),
            RegisterPair("uavcan.sub.esc_heartbeat.id", "uavcan.pub.esc_heartbeat.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(138))),
            RegisterPair("uavcan.sub.feedback.id", "uavcan.pub.feedback.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(139))),
            RegisterPair("uavcan.sub.power.id", "uavcan.pub.power.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(140))),
            RegisterPair("uavcan.sub.status.id", "uavcan.pub.status.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(141))),
            RegisterPair("uavcan.sub.dynamics.id", "uavcan.pub.dynamics.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(142)))
        ]
        time.sleep(2)
        for index, node_info in enumerate(node_info_list):
            node_info.motor_index = OnlyEmbeddedDeviceRegister("id_in_esc_group",
                                                               uavcan.register.Value_1_0(
                                                                   natural16=uavcan.primitive.array.Natural16_1_0(0)))
            configure_registers(registers_array, tester_node, node_info)
            command_save(tester_node, node_info.node_id)
            if restart_node(tester_node, node_info.node_id) is None:
                assert False
                return
        time.sleep(4)
        our_allocator(2, node_to_use=tester_node)
        readiness_message = reg.udral.service.common.Readiness_0_1(3)
        readiness_stop_message = reg.udral.service.common.Readiness_0_1(2)  # it is actually standby
        readiness_pub = tester_node.make_publisher(reg.udral.service.common.Readiness_0_1, "readiness")
        await readiness_pub.publish(readiness_message)
        pub = tester_node.make_publisher(reg.udral.service.actuator.common.sp.Scalar_0_1, "setpoint")
        feedback_subscription = tester_node.make_subscriber(reg.udral.service.actuator.common.Feedback_0_1,
                                                            "feedback")
        try:
            for i in range(40000):
                for node_info in node_info_list:
                    rpm_message = reg.udral.service.actuator.common.sp.Scalar_0_1(value=rpm_to_radians_per_second(200))
                    await pub.publish(rpm_message)
                    await readiness_pub.publish(readiness_message)
                    feedback_result = await feedback_subscription.receive_for(0.3)
                    if feedback_result is None:
                        assert False
                        return
                time.sleep(0.06)
        except KeyboardInterrupt:
            # The ESC would stop after TTL itself, but it is important to have quicker control available when all
            # communications are still available
            await readiness_pub.publish(readiness_stop_message)
            print("\nInterrupted, sent stop message")
