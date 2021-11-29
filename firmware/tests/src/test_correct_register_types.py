import time

from _await_wrap import wrap_await
from utils import make_access_request, configure_a_port_on_sapog, rpm_to_radians_per_second, prepared_node, \
    prepared_sapogs, restarted_sapogs, restart_node, configure_registers
from imports import add_deps

add_deps()
import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1

from register_pair_class import RegisterPair, EmbeddedDeviceRegPair


def test_correct_id_types():
    pass
