#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
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
from RegisterPair import RegisterPair, OnlyEmbeddedDeviceRegister
from utils import rpm_to_radians_per_second, restart_node, \
    command_save, configure_embedded_registers, configure_tester_side_registers, get_prepared_sapogs

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


def modify_tester_registry_name_with_number(registry_item: RegisterPair, number: int):
    registry_item.tester_reg_name = f"{registry_item.tester_reg_name}_{number}"


class SpeedController:
    def __init__(self, node_amount: int, starting_speed=0, allowed_acceleration_time: float = 3.0):
        self.speed_array = [starting_speed for x in range(node_amount)]
        self.current_speeds = [0 for x in range(node_amount)]
        self.allowed_acceleration_time = allowed_acceleration_time

    def change_speed(self, node_index: int, new_speed: float):
        assert len(
            self.speed_array) > node_index, \
            f"Cannot access index {node_index} in array of {len(self.speed_array)} elements"
        self.speed_array[node_index] = new_speed
        task = asyncio.create_task(self.check_speed_correctness())

    async def check_speed_correctness(self):
        # Allowing time for the motors to reach their desired speeds
        await asyncio.sleep(self.allowed_acceleration_time)
        for i2, s in enumerate(self.current_speeds):
            speed_difference = abs(self.speed_array[i2] - s)
            assert speed_difference < 100, "There is a problem with reporting RPM."


class TestEscRpm:
    @staticmethod
    @pytest.mark.asyncio
    async def test_rpm_esc_control(prepared_double_redundant_node):
        tester_node = prepared_double_redundant_node
        prepared_sapogs = await get_prepared_sapogs(tester_node)
        our_allocator = None
        if len(prepared_sapogs) == 0:
            our_allocator = make_simple_node_allocator()
            node_info_list = await our_allocator(2, node_to_use=tester_node)
        else:
            node_info_list = prepared_sapogs
        sid_gen = SubjectIdGenerator(135)
        sid_gen2 = SubjectIdGenerator(135)
        common_registers = [
            RegisterPair("uavcan.pub.setpoint.id", "uavcan.sub.setpoint.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])), None,
                         None),
            # not planning to use this either
            RegisterPair("uavcan.pub.readiness.id", "uavcan.sub.readiness.id",
                         uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])), None,
                         None),
        ]
        sid_gen2.set(sid_gen.get())

        def make_device_specific_registry() -> typing.List[RegisterPair]:
            return [
                OnlyEmbeddedDeviceRegister("control_mode_rpm",
                                           uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(value=[True]))),
                OnlyEmbeddedDeviceRegister("ttl_milliseconds",
                                           uavcan.register.Value_1_0(
                                               natural16=uavcan.primitive.array.Natural16_1_0([300]))),
                RegisterPair("feedback", "uavcan.pub.feedback.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.service.actuator.common.Feedback_0_1,
                             is_subscription=True),
                RegisterPair("power", "uavcan.pub.power.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.physics.electricity.PowerTs_0_1,
                             is_subscription=True),
                RegisterPair("status", "uavcan.pub.status.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.service.actuator.common.Status_0_1,
                             is_subscription=True),
                RegisterPair("dynamics", "uavcan.pub.dynamics.id",
                             uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0([sid_gen()])),
                             sid_gen2(),
                             reg.udral.physics.dynamics.rotation.PlanarTs_0_1,
                             is_subscription=True)
            ]

        time.sleep(2)
        assert (len(node_info_list) > 0)
        for index, node_info in enumerate(node_info_list):
            node_info.motor_index = index
            combined_registry = make_device_specific_registry() + common_registers
            combined_registry.append(OnlyEmbeddedDeviceRegister("id_in_esc_group",
                                                                uavcan.register.Value_1_0(
                                                                    natural16=uavcan.primitive.array.Natural16_1_0(
                                                                        [index]))))
            await configure_embedded_registers(combined_registry, tester_node, node_info.node_id)
            configure_tester_side_registers(combined_registry, tester_node)
            node_info.registers = combined_registry
            await command_save(tester_node, node_info.node_id)
            if await restart_node(tester_node, node_info.node_id) is None:
                assert False, f"Node {node_info.node_id} couldn't be restarted"
        time.sleep(4)
        if our_allocator:
            node_info_list = await our_allocator(2, node_to_use=tester_node)
        for index, node_info in enumerate(node_info_list):
            node_info.motor_index = index
            for register in node_info.registers:
                if register.is_subscription:
                    register.actual_subscription = tester_node.make_subscriber(register.communication_type,
                                                                               register.tester_reg_name)

        readiness_message = reg.udral.service.common.Readiness_0_1(3)
        readiness_stop_message = reg.udral.service.common.Readiness_0_1(2)  # it is actually standby
        readiness_pub = tester_node.make_publisher(reg.udral.service.common.Readiness_0_1, "readiness")
        await readiness_pub.publish(readiness_message)
        pub = tester_node.make_publisher(reg.udral.service.actuator.common.sp.Vector2_0, "setpoint")
        # dynamics_sub = tester_node.make_subscriber(reg.udral.physics.dynamics.rotation.PlanarTs_0_1, "dynamics")
        speed_controller = SpeedController(2)
        assert len(node_info_list) >= 1, "Please restart" \
                                         " the nodes before continuing. This test was supposed" \
                                         "to allocate nodes and then keep the info about them. "

        async def receive_dynamics(msg: reg.udral.physics.dynamics.rotation.PlanarTs_0_1,
                                   tf: pyuavcan.transport._transfer.TransferFrom):
            new_filter = filter(lambda n: n.node_id == tf.source_node_id, node_info_list)
            if (node := next(new_filter, None)) is not None:
                speed_controller.current_speeds[
                    node.motor_index] = msg.value.kinematics.angular_velocity.radian_per_second

        for index, node_info in enumerate(node_info_list):
            node_info.motor_index = index
            for register in node_info.registers:
                if register.is_subscription and register.actual_subscription is not None:
                    if "dynamics" in register.tester_reg_name:
                        register.actual_subscription.receive_in_background(receive_dynamics)

        async def run_first_motor():
            speed_controller.change_speed(0, rpm_to_radians_per_second(1400))

        async def run_second_motor():
            await asyncio.sleep(5)
            speed_controller.change_speed(1, rpm_to_radians_per_second(1400))

        asyncio.create_task(run_first_motor())
        asyncio.create_task(run_second_motor())
        try:
            for i in range(4000):

                rpm_message = reg.udral.service.actuator.common.sp.Vector2_0(value=speed_controller.speed_array)
                await pub.publish(rpm_message)
                await readiness_pub.publish(readiness_message)
                # start_time2 = time.time()

                for node_info in node_info_list:
                    for register in node_info.registers:
                        if register.is_subscription and register.actual_subscription is not None:
                            if "feedback" in register.tester_reg_name:
                                feedback_result = register.actual_subscription.receive_for(0.2)
                                assert feedback_result is not None, "Feedback was not received."
                # Sleep the time that hasn't been already used of 0.2 seconds
                time.sleep(0.1)
                # time.sleep(clip(.2 - time.time() - start_time2, 0, 0.2))
        except KeyboardInterrupt:
            # The ESC would stop after TTL itself, but it is important to have quicker control available when all
            # communications are still available
            await readiness_pub.publish(readiness_stop_message)
            print("\nInterrupted, sent stop message")
