import time

from _await_wrap import wrap_await
from utils import make_access_request, configure_a_port_on_sapog, rpm_to_radians_per_second, \
    make_configurable_id_publisher, prepared_node, prepared_sapogs, restarted_sapogs, restart_node
from imports import add_deps

add_deps()
import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1

from register_pair_class import RegisterPair, EmbeddedDeviceRegPair


class TestESC:
    @staticmethod
    def test_rpm_run_2_sec(prepared_node, prepared_sapogs):
        for node_id in prepared_sapogs.keys():
            if restart_node(node_id):
                time.sleep(4)
            else:
                assert False
                return
        registers_array: list[RegisterPair] = [
            RegisterPair("uavcan.pub.radians_in_second_velocity.id", "uavcan.sub.radians_in_second_velocity.id",
                         uavcan.register.Value_1_0(integer64=uavcan.primitive.array.Integer64_1_0(136))),
            RegisterPair("uavcan.cln.readiness.id", "uavcan.srv.readiness.id",
                         uavcan.register.Value_1_0(integer64=uavcan.primitive.array.Integer64_1_0(137))),
            EmbeddedDeviceRegPair("id_in_esc_group",
                                  uavcan.register.Value_1_0(integer64=uavcan.primitive.array.Integer64_1_0(0)))
        ]
        # prepared_node.registry[f"uavcan.pub.radians_in_second_velocity.id"] = 136
        for node_id in prepared_sapogs.keys():
            readiness_message = reg.udral.service.common.Readiness_0_1(3)
        client = prepared_node.make_client(reg.udral.service.common.Readiness_0_1, node_id, "readiness")
        wrap_await(client.call(readiness_message))

        rpm_message = uavcan.si.unit.angular_velocity.Scalar_1_0(rpm_to_radians_per_second(2000))
        pub = make_configurable_id_publisher(uavcan.si.unit.angular_velocity.Scalar_1_0,
                                             "radians_in_second_velocity",
                                             subject_id=136, prepared_node=prepared_node)
        for i in range(20):
            wrap_await(pub.publish(rpm_message))
        time.sleep(0.3)
