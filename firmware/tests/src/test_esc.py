import asyncio

import pyuavcan
import time
import typing

from pyuavcan.application import make_node, NodeInfo

import Nodes
from _await_wrap import wrap_await
from my_simple_test_allocator import make_simple_node_allocator
from utils import rpm_to_radians_per_second, restart_node, configure_registers, \
    command_save, make_registry, get_interfaces_by_hw_id
from imports import add_deps

add_deps()
import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1
import reg.udral.service.actuator.common.sp.Scalar_0_1
import reg.udral.service.actuator.common.Feedback_0_1
import reg.udral.service.actuator.common.Status_0_1
import reg.udral.physics.electricity.PowerTs_0_1
import reg.udral.physics.dynamics.rotation.PlanarTs_0_1
import uavcan.primitive.array.Bit_1_0
import uavcan.register.Value_1_0

import threading

from register_pair_class import RegisterPair, EmbeddedDeviceRegPair


def _restart_node(interfaces, node_id):
    pass


def _allocate_node(interfaces) -> int:
    """Returns a node_id"""
    pass


def _motor_test_esc_controllers(nodes: typing.List[Nodes.NodeInfo]):
    """What should this do? Should it loop over all the available devices and create a tester node for each?"""
    coroutines = []
    for node_info in enumerate(nodes):
        registry = make_registry(0, interfaces=node_info.interfaces)
        tester_node = make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry)
        threading.Thread(target=lambda: _run_esc_test_on_board(node_info, tester_node)).start()


def _run_esc_test_on_board(node_info: Nodes.NodeInfo, tester_node: pyuavcan.application.Node) -> None:
    registry = make_registry(0, interfaces=node_info.interfaces)

    # radian per second
    registers_array: typing.List[RegisterPair] = [
        RegisterPair("uavcan.pub.setpoint.id", "uavcan.sub.setpoint.id",
                     uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(136))),
        # RegisterPair("uavcan.pub.radians_in_second_velocity.id", "uavcan.sub.radians_in_second_velocity.id",
        #              uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(136))),
        RegisterPair("uavcan.pub.readiness.id", "uavcan.sub.readiness.id",
                     uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(137))),
        EmbeddedDeviceRegPair("id_in_esc_group",
                              uavcan.register.Value_1_0(natural16=uavcan.primitive.array.Natural16_1_0(0))),
        EmbeddedDeviceRegPair("control_mode_rpm",
                              uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(value=[True]))),
        EmbeddedDeviceRegPair("ttl_milliseconds",
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
    configure_registers(registers_array, tester_node, node_info.node_id)
    command_save(tester_node, node_info.node_id)
    if restart_node(tester_node, node_info.node_id) is None:
        assert False
        return
    time.sleep(4)
    _allocate_node(node_info.interfaces)
    readiness_message = reg.udral.service.common.Readiness_0_1(3)
    readiness_stop_message = reg.udral.service.common.Readiness_0_1(2)  # it is actually standby
    readiness_pub = tester_node.make_publisher(reg.udral.service.common.Readiness_0_1, "readiness")
    wrap_await(readiness_pub.publish(readiness_message))
    rpm_message = reg.udral.service.actuator.common.sp.Scalar_0_1(value=rpm_to_radians_per_second(200))
    pub = tester_node.make_publisher(reg.udral.service.actuator.common.sp.Scalar_0_1, "setpoint")
    feedback_subscription = tester_node.make_subscriber(reg.udral.service.actuator.common.Feedback_0_1,
                                                        "feedback")
    try:
        for i in range(40000):
            wrap_await(pub.publish(rpm_message))
            wrap_await(readiness_pub.publish(readiness_message))
            feedback_result = wrap_await(feedback_subscription.receive_for(0.3))
            if feedback_result is None:
                assert False
                return
            time.sleep(0.06)
    except KeyboardInterrupt:
        # The ESC would stop after TTL itself, but it is important to have quicker control available when all
        # communications are still available
        wrap_await(readiness_pub.publish(readiness_stop_message))
        print("\nInterrupted, sent stop message")


class TestESC:
    @staticmethod
    def test_rpm_run_2_sec(prepared_double_redundant_node, prepared_sapogs):
        # prepared_node = prepared_double_redundant_node
        # for node_id in prepared_sapogs.keys():
        #     if restart_node(prepared_node, node_id):
        #         time.sleep(4)
        #     else:
        #         assert False
        #         return
        # make_simple_node_allocator()(len(prepared_sapogs.keys()))
        nodes_info_list = get_interfaces_by_hw_id(do_get_allocated_nodes=True, do_allocate=True)
        _motor_test_esc_controllers(nodes_info_list)
