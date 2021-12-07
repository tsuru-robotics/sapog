import time
import typing

from _await_wrap import wrap_await
from my_simple_test_allocator import allocate_nr_of_nodes
from utils import make_access_request, configure_a_port_on_sapog, rpm_to_radians_per_second, prepared_node, \
    prepared_sapogs, restarted_sapogs, restart_node, configure_registers, command_save, prepared_double_redundant_node
from imports import add_deps

add_deps()
import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1
import reg.udral.service.actuator.common.sp.Scalar_0_1
import uavcan.primitive.array.Bit_1_0
import uavcan.register.Value_1_0

from register_pair_class import RegisterPair, EmbeddedDeviceRegPair


class TestESC:
    @staticmethod
    def test_rpm_run_2_sec(prepared_double_redundant_node, prepared_sapogs):
        prepared_node = prepared_double_redundant_node
        for node_id in prepared_sapogs.keys():
            if restart_node(prepared_node, node_id):
                time.sleep(4)
            else:
                assert False
                return
        allocate_nr_of_nodes(len(prepared_sapogs.keys()))
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
        configure_registers(registers_array, prepared_node, prepared_sapogs)
        for node_id in prepared_sapogs.keys():
            command_save(prepared_node, node_id)
            if restart_node(prepared_node, node_id) is None:
                assert False
                return
        time.sleep(4)
        allocate_nr_of_nodes(len(prepared_sapogs.keys()))
        readiness_message = reg.udral.service.common.Readiness_0_1(3)
        readiness_pub = prepared_node.make_publisher(reg.udral.service.common.Readiness_0_1, "readiness")
        wrap_await(readiness_pub.publish(readiness_message))

        rpm_message = reg.udral.service.actuator.common.sp.Scalar_0_1(value=rpm_to_radians_per_second(2000))
        pub = prepared_node.make_publisher(reg.udral.service.actuator.common.sp.Scalar_0_1, "setpoint")
        for i in range(400):
            wrap_await(pub.publish(rpm_message))
            wrap_await(readiness_pub.publish(readiness_message))
            time.sleep(0.3)
        time.sleep(0.3)
