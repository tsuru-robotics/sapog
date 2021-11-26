import time

from _await_wrap import wrap_await
from utils import make_access_request, configure_a_port_on_sapog, rpm_to_radians_per_second, \
    make_configurable_id_publisher
from imports import add_deps

add_deps()
import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1


class TestESC:
    @staticmethod
    def test_rpm_run_2_sec(prepared_node, prepared_sapogs):
        for node_id in prepared_sapogs.keys():
            make_access_request("id_in_esc_group", uavcan.primitive.array.Integer64_1_0(0), node_id, prepared_node)
        configure_a_port_on_sapog("radians_in_second_velocity", 136, prepared_sapogs, prepared_node)
        configure_a_port_on_sapog("readiness", 137, prepared_sapogs, prepared_node)
        # prepared_node.registry[f"uavcan.pub.radians_in_second_velocity.id"] = 136
        for node_id in prepared_sapogs.keys():
            readiness_message = reg.udral.service.common.Readiness_0_1(3)
            client = prepared_node.make_client(reg.udral.service.common.Readiness_0_1, node_id, "readiness.id")
            wrap_await(client.call(readiness_message))

            rpm_message = uavcan.si.unit.angular_velocity.Scalar_1_0(rpm_to_radians_per_second(2000))
            pub = make_configurable_id_publisher(uavcan.si.unit.angular_velocity.Scalar_1_0,
                                                 "radians_in_second_velocity",
                                                 subject_id=136, prepared_node=prepared_node)
            for i in range(20):
                wrap_await(pub.publish(rpm_message))
                time.sleep(0.3)
