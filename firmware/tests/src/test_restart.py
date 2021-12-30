import pytest

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

from node_fixtures.drnf import prepared_node
from utils import prepared_sapogs


@pytest.mark.asyncio
async def test_restart_node(prepared_node, prepared_sapogs):
    for node_id in prepared_sapogs.keys():
        service_client = prepared_node.make_client(uavcan.node.ExecuteCommand_1_1, node_id)
        msg = uavcan.node.ExecuteCommand_1_1.Request()
        msg.command = msg.COMMAND_RESTART
        response = await service_client.call(msg)
        assert response is not None
