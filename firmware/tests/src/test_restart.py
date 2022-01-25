import pytest

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

from node_fixtures.drnf import prepared_double_redundant_node
from utils import get_prepared_sapogs


@pytest.mark.asyncio
async def test_restart_node(prepared_double_redundant_node):
    prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
    for node_info in prepared_sapogs:
        service_client = prepared_double_redundant_node.make_client(uavcan.node.ExecuteCommand_1_1, node_info.node_id)
        msg = uavcan.node.ExecuteCommand_1_1.Request()
        msg.command = msg.COMMAND_RESTART
        response = await service_client.call(msg)
        assert response is not None, "Node did not acknowledge restarting."
