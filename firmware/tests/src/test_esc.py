#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import typing

import math
import pytest
import pyuavcan
import time

import reg.udral.physics.dynamics.rotation.PlanarTs_0_1
import reg.udral.physics.electricity.PowerTs_0_1
import reg.udral.service.actuator.common.Feedback_0_1
import reg.udral.service.actuator.common.Status_0_1
import reg.udral.service.actuator.common.sp.Scalar_0_1
import reg.udral.service.common.Readiness_0_1
import uavcan.primitive.array.Bit_1_0
import uavcan.primitive.array.Integer64_1_0
import uavcan.register.Value_1_0
from numpy import clip
from my_simple_test_allocator import make_simple_node_allocator
from register_pair_class import RegisterPair, OnlyEmbeddedDeviceRegister
from utils import rpm_to_radians_per_second, restart_node, \
    command_save, configure_embedded_registers, configure_tester_side_registers

from node_fixtures.drnf import prepared_double_redundant_node


def radian_s_to_rpm(radian_s: float):
    return radian_s * 60 / (math.pi * 2)


def test_radian_s_to_rpm():
    from decimal import Decimal
    from math import isclose
    assert isclose(radian_s_to_rpm(3), Decimal(28.65), abs_tol=0.01)
    assert isclose(Decimal(radian_s_to_rpm(4)), Decimal(38.2), abs_tol=0.01)


class SubjectIdGenerator:
    def __init__(self, start_value: int):
        self.counter = start_value

    def get(self):
        return self.counter

    def get_next(self):
        return_value = self.counter  # or can i just: return_value = self.counter
        self.counter += 1
        return return_value

    def set(self, value: int):
        self.counter = value

    def __call__(self, *args, **kwargs):
        return self.get_next()


class TestESC:
    @staticmethod
    @pytest.mark.asyncio
    async def test_rpm_run_2_sec(prepared_double_redundant_node):
        our_allocator = make_simple_node_allocator()
        tester_node = prepared_double_redundant_node
        node_info_list = await our_allocator(2, node_to_use=tester_node)

        sid_gen = SubjectIdGenerator(135)
        sid_gen2 = SubjectIdGenerator(135)
        common_registers = [
            RegisterPair("uavcan.pub.setpoint.id", "uavcan.sub.setpoint.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()]))),
            RegisterPair("uavcan.pub.readiness.id", "uavcan.sub.readiness.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()]))),
        ]
        sid_gen2.set(sid_gen.get())

        def make_device_specific_registry(device_index: int) -> typing.List[RegisterPair]:
            return [

                # RegisterPair("uavcan.pub.radians_in_second_velocity.id", "uavcan.sub.radians_in_second_velocity.id",
                #              uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(136))),

                OnlyEmbeddedDeviceRegister("control_mode_rpm",
                                           uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(value=[True]))),
                OnlyEmbeddedDeviceRegister("ttl_milliseconds",
                                           uavcan.register.Value_1_0(
                                               natural16=uavcan.primitive.array.Natural16_1_0([300]))),
                RegisterPair("uavcan.sub.esc_heartbeat.id", "uavcan.pub.esc_heartbeat.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             type_communicated=reg.udral.service.common.Heartbeat_0_1),
                RegisterPair("uavcan.sub.feedback.id", "uavcan.pub.feedback.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.service.actuator.common.Feedback_0_1),
                RegisterPair("uavcan.sub.power.id", "uavcan.pub.power.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.physics.electricity.PowerTs_0_1),
                RegisterPair("uavcan.sub.status.id", "uavcan.pub.status.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.service.actuator.common.Status_0_1),
                RegisterPair("uavcan.sub.dynamics.id", "uavcan.pub.dynamics.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.physics.dynamics.rotation.PlanarTs_0_1)
            ]

        time.sleep(2)

        for index, node_info in enumerate(node_info_list):
            node_info.motor_index = index
            combined_registry = make_device_specific_registry(index) + common_registers
            combined_registry.append(OnlyEmbeddedDeviceRegister("id_in_esc_group",
                                                                uavcan.register.Value_1_0(
                                                                    natural16=uavcan.primitive.array.Natural16_1_0(
                                                                        index))))
            await configure_embedded_registers(combined_registry, tester_node, node_info)
            configure_tester_side_registers(combined_registry, tester_node)
            node_info.registers = combined_registry
            for registry_item in combined_registry:
                if ".sub." in registry_item.tester_reg_name:
                    pure_name = registry_item.tester_reg_name[11:].replace(".id", "")
                    assert "." not in pure_name, "There was a problem converting the compound name to a pure name"
                    sub = tester_node.make_subscriber(registry_item.communication_type, pure_name)
                    node_info.store_subscription(sub, registry_item.value.natural16.value,
                                                 registry_item.tester_reg_name,
                                                 data_type=registry_item.communication_type)

            await command_save(tester_node, node_info.node_id)
            if await restart_node(tester_node, node_info.node_id) is None:
                assert False, f"Node {node_info.node_id} couldn't be restarted"
        time.sleep(4)
        node_info_list = await our_allocator(2, node_to_use=tester_node)
        for index, node_info in enumerate(node_info_list):
            node_info.motor_index = index
        readiness_message = reg.udral.service.common.Readiness_0_1(3)
        readiness_stop_message = reg.udral.service.common.Readiness_0_1(2)  # it is actually standby
        subscription_store = {}
        readiness_pub = tester_node.make_publisher(reg.udral.service.common.Readiness_0_1, "readiness")
        await readiness_pub.publish(readiness_message)
        pub = tester_node.make_publisher(reg.udral.service.actuator.common.sp.Vector2_0, "setpoint")
        for index, node_info in enumerate(node_info_list):
            feedback_subscription = tester_node.make_subscriber(reg.udral.service.actuator.common.Feedback_0_1,
                                                                "feedback")
        dynamics_sub = tester_node.make_subscriber(reg.udral.physics.dynamics.rotation.PlanarTs_0_1, "dynamics")
        current_speeds = [0, 0]
        assert len(node_info_list) >= 2, "Please restart" \
                                         " the nodes before continuing. This test was supposed" \
                                         "to allocate nodes and then keep the info about them. "

        def receive_dynamics(msg: reg.udral.physics.dynamics.rotation.PlanarTs_0_1,
                             tf: pyuavcan.transport._transfer.TransferFrom):
            new_filter = filter(lambda n: n.node_id == tf.source_node_id, node_info_list)
            if (node := next(new_filter, None)) is not None:
                current_speeds[node.motor_index] = msg.value.kinematics.angular_velocity.radian_per_second

        dynamics_sub.receive_in_background(receive_dynamics)
        starting_time = time.time()
        try:
            for i in range(40000):
                input_array = [rpm_to_radians_per_second(200), rpm_to_radians_per_second(200)]
                input_array.extend([0 for i in range(6)])
                if time.time() - starting_time > 4:
                    for i2, s in enumerate(current_speeds):
                        speed_difference = abs(input_array[i2] - s)
                        assert speed_difference < 100, "There is a problem with reporting RPM."
                rpm_message = reg.udral.service.actuator.common.sp.Vector2_0(value=input_array)
                await pub.publish(rpm_message)
                await readiness_pub.publish(readiness_message)
                start_time2 = time.time()
                for node_info in node_info_list:
                    feedback_subscription = node_info.get_subscription(reg.udral.service.actuator.common.Feedback_0_1)
                    feedback_result = await feedback_subscription.receive_for(0.5)
                    assert feedback_result is not None, "Feedback was not received."
                # Sleep the time that hasn't been already used of 0.2 seconds
                time.sleep(clip(.2 - time.time() - start_time2, 0, 0.2))
        except KeyboardInterrupt:
            # The ESC would stop after TTL itself, but it is important to have quicker control available when all
            # communications are still available
            await readiness_pub.publish(readiness_stop_message)
            print("\nInterrupted, sent stop message")
