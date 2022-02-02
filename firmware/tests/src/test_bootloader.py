import pytest
import asyncio
import os
from pathlib import Path
import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo
import pyuavcan.application.file

from node_fixtures.drnf import prepared_node, prepared_double_redundant_node
from my_simple_test_allocator import make_simple_node_allocator
from utils import get_prepared_sapogs, restart_node


@pytest.mark.asyncio
async def test_bootloader(prepared_double_redundant_node):
    tester_node = prepared_double_redundant_node
    tracker: pyuavcan.application.node_tracker = pyuavcan.application.node_tracker.NodeTracker(tester_node)
    tracker.get_info_timeout = 1.0
    # Gathering heartbeats from any online nodes
    prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
    # Removing the debugger node
    # If no heartbeats were detected then the allocator is run
    if len(prepared_sapogs) == 0:
        our_allocator = make_simple_node_allocator()
        node_info_list = await our_allocator(node_to_use=prepared_double_redundant_node, continuous=True,
                                             time_budget_seconds=2)
    else:
        node_info_list = prepared_sapogs
    for index, node_info in enumerate(node_info_list):
        if node_info.node_id == 2:
            continue
        command_client = tester_node.make_client(uavcan.node.ExecuteCommand_1, node_info.node_id)
        command_client.response_timeout = 10.0
        print("Sending an invalid firmware update command with empty parameter")
        result_response = await command_client.call(
            uavcan.node.ExecuteCommand_1.Request(
                command=uavcan.node.ExecuteCommand_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE)
        )
        assert result_response, "Got no response"
        resp, _ = result_response
        assert isinstance(resp, uavcan.node.ExecuteCommand_1.Response)
        assert resp.status == resp.STATUS_BAD_PARAMETER, "Status should have been STATUS_BAD_PARAMETER"

        # Launch the file server.
        # TODO: currently, pyuavcan.application service objects cannot be stopped once started; fix that in PyUAVCAN.
        file_server = pyuavcan.application.file.FileServer(tester_node, [Path.cwd()])
        broken_fw_path = ""
        # INSTALL INVALID FIRMWARE AND ENSURE THE DEVICE IS NOT BRICKED.
        with open("invalid_image_for_bootloader_test.bin", "wb") as broken_fw:
            broken_fw.write(open("/dev/random", "rb").read(2000))
            broken_fw_path = str(Path.cwd() / "invalid_image_for_bootloader_test.bin")
        req = uavcan.node.ExecuteCommand_1.Request(
            command=uavcan.node.ExecuteCommand_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE,
            parameter=broken_fw_path,
        )
        assert os.path.exists(Path.cwd() / "invalid_image_for_bootloader_test.bin"), "Creating invalid image failed."
        await asyncio.sleep(3.0)
        print("Requesting the device to install an invalid firmware image: %s", req)
        restart_response = await restart_node(tester_node, node_info.node_id)
        assert restart_response, "The device did not restart"
        await asyncio.sleep(10)
        response = await command_client.call(req)
        assert response, "The device did not respond to the restart request."
        resp, _ = response
        assert isinstance(resp, uavcan.node.ExecuteCommand_1.Response)
        assert resp.status == resp.STATUS_SUCCESS, "Execute command response was not a success"
        print("Device restarted, good; waiting for the bootloader to finish...")
        deadline = asyncio.get_running_loop().time() + 10.0
        count_key_not_found = 0
        while True:
            try:
                assert deadline > asyncio.get_running_loop().time(), "Didn't find bootloader's heartbeat in time."
                await asyncio.sleep(1.0)
                entry = tracker.registry[node_info.node_id]
                assert entry.heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE, "Bootloader is not running"
                if entry.heartbeat.health.value == uavcan.node.Health_1.WARNING:
                    print(
                        "Bootloader reported critical error, this means that it finished "
                        "installing the firmware and discovered that it is invalid"
                    )
                    break
            except KeyError:
                count_key_not_found += 1
                if count_key_not_found > 20:
                    raise Exception("Key was not found for too many times")
                else:
                    continue
        print("Invalid firmware installation finished")
        await asyncio.sleep(3.0)
        entry = tracker.registry[node_info.node_id]
        print("Current state (should be in the bootloader and WARNING): %r", entry)
        assert entry.heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE
        assert entry.heartbeat.health.value == uavcan.node.Health_1.WARNING
        assert entry.info.name.tobytes().decode() == "com.zubax.sapog"

        # REPAIR THE DEVICE BY REPLACING THE FIRMWARE WITH A VALID ONE.
        req = uavcan.node.ExecuteCommand_1.Request(
            command=uavcan.node.ExecuteCommand_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE,
            parameter=broken_fw_path,
        )
        print("Asking the bootloader to reinstall the valid firmware: %s", req)
        resp, _ = await command_client.call(req)
        assert isinstance(resp, uavcan.node.ExecuteCommand_1.Response)
        assert resp.status == resp.STATUS_SUCCESS
        deadline = asyncio.get_running_loop().time() + 120.0  # This may take some time
        while tracker.registry[node_info.node_id].heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE:
            await asyncio.sleep(1.0)
            assert deadline > asyncio.get_running_loop().time()
            if node_info.node_id not in tracker.registry:
                break
        print("Bootloader execution finished")
        await asyncio.sleep(10.0)
        entry = tracker.registry[node_info.node_id]
        print("Current state (the application should be running normally): %r", entry)
        assert entry.heartbeat.mode.value == uavcan.node.Mode_1.OPERATIONAL
        assert entry.info.name.tobytes().decode() == "com.zubax.sapog"
