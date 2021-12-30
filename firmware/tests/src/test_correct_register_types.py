import pytest
import time

from _await_wrap import wrap_await
from utils import make_access_request, prepared_sapogs, restarted_sapogs, restart_node

from node_fixtures.drnf import prepared_node, prepared_double_redundant_node

from conftest import add_deps

add_deps()
import uavcan.primitive.array.Integer64_1_0
import reg.udral.service.common.Readiness_0_1

from register_pair_class import RegisterPair, OnlyEmbeddedDeviceRegister


@pytest.mark.asyncio
async def test_correct_id_types():
    pass
