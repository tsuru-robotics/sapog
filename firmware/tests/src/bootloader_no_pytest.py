import logging

import sys

import asyncio
import os
from pathlib import Path
import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

import pycyphal
from pycyphal.application import Node, make_node, NodeInfo
import pycyphal.application.file_server

from node_fixtures.drnf import get_prepared_double_redundant_node
from my_simple_test_allocator import make_simple_node_allocator
from utils import get_prepared_sapogs, restart_node


def get_valid_firmware_path():
    return str(next((Path.cwd().parent.parent / "build").glob("io.px4.sapog*.application.bin"), None).absolute())


def create_invalid_firmware():
    broken_fw_path = (Path.cwd() / "invalid_image_for_bootloader_test.bin").absolute()
    with open(broken_fw_path, "wb") as broken_fw:
        broken_fw.write(open("/dev/random", "rb").read(2000))
    assert os.path.exists(Path.cwd() / "invalid_image_for_bootloader_test.bin"), "Creating invalid image failed."
    return str(broken_fw_path)


_logger = logging.getLogger(__name__)
_logger.setLevel(logging.NOTSET)


async def assert_does_bootloader_have_warning_heartbeat(tracker, node_info):
    # Warning status needs to appear due to the overwriting with an incorrect image
    # if the read response is not received then this heartbeat cannot have the right value
    print("assert_does_bootloader_have_warning_heartbeat() beginning")
    deadline = asyncio.get_running_loop().time() + 4.0
    count_key_not_found = 0
    was_heartbeat_found = False
    did_not_reach_software_update = False
    while True:
        await asyncio.sleep(1.0)
        current_time = asyncio.get_running_loop().time()
        try:
            if current_time > deadline:
                if did_not_reach_software_update:
                    _logger.error("Did not get into the software update mode.")
                if was_heartbeat_found:
                    _logger.error("Heartbeat mode value was wrong, mode is supposed to be WARNING).")
                    break
                else:
                    _logger.error("Didn't find bootloader's heartbeat in time.")
                    break

            _logger.info(node_info.node_id)
            entry = tracker.registry.get(node_info.node_id, None)
            if entry:
                was_heartbeat_found = True
                if entry.heartbeat.health.value == uavcan.node.Health_1.WARNING:
                    _logger.info(
                        "Bootloader reported critical error, this means that it finished "
                        "installing the firmware and discovered that it is invalid"
                    )
                    break
                if entry.heartbeat.mode.value != uavcan.node.Mode_1.SOFTWARE_UPDATE:
                    did_not_reach_software_update = True
                    _logger.info("Software update mode was expected but not set.")
                print(tracker.registry)
                print(f"Bootloader has a health state of {entry.heartbeat.mode.value}")
            else:
                continue
        except KeyError:
            count_key_not_found += 1
            if count_key_not_found % 20 == 0:
                _logger.error(f"Bootloader's heartbeat was not found for {count_key_not_found} consecutive tries.")
            elif count_key_not_found > 100:
                continue
            else:
                continue
    _logger.info("Invalid firmware installation finished")
    await asyncio.sleep(3.0)
    entry = tracker.registry.get(node_info.node_id, None)
    assert entry
    _logger.info("Current state (should be in the bootloader and WARNING): %r", entry)
    assert entry.heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE
    assert entry.heartbeat.health.value == uavcan.node.Health_1.WARNING
    assert entry.info.name.tobytes().decode() == "com.zubax.sapog"


async def assert_does_bootloader_have_healthy_heartbeat(tracker, node_info):
    deadline = asyncio.get_running_loop().time() + 120.0  # This may take some time
    while node_info.node_id not in tracker.registry:
        await asyncio.sleep(0.1)
    while tracker.registry[node_info.node_id].heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE:
        await asyncio.sleep(1.0)
        assert deadline > asyncio.get_running_loop().time()
        if node_info.node_id not in tracker.registry:
            break
    _logger.info("Bootloader execution finished")
    await asyncio.sleep(10.0)
    entry = tracker.registry.get(node_info.node_id, None)
    assert entry
    _logger.info("Current state (the application should be running normally): %r", entry)
    assert entry.heartbeat.mode.value == uavcan.node.Mode_1.OPERATIONAL
    assert entry.info.name.tobytes().decode() == "com.zubax.sapog"


async def assert_send_empty_parameter_install_request(tester_node, node_info, command_client):
    _logger.info("Sending an invalid firmware update command with empty parameter")
    while True:
        result_response = await command_client.call(
            uavcan.node.ExecuteCommand_1_1.Request(
                command=uavcan.node.ExecuteCommand_1_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE)
        )
        if result_response:
            break
    assert result_response, "Got no response"
    resp, _ = result_response
    assert isinstance(resp, uavcan.node.ExecuteCommand_1_1.Response)
    assert resp.status == resp.STATUS_BAD_PARAMETER, "Status should have been STATUS_BAD_PARAMETER"


async def assert_installing_invalid_firmware_doesnt_brick_device(tester_node, node_info, command_client, tracker):
    broken_fw_path = create_invalid_firmware()
    req = uavcan.node.ExecuteCommand_1.Request(
        command=uavcan.node.ExecuteCommand_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE,
        parameter=broken_fw_path,
    )
    # INSTALL INVALID FIRMWARE AND ENSURE THE DEVICE IS NOT BRICKED.

    await asyncio.sleep(3.0)
    _logger.info("Requesting the device to install an invalid firmware image: %s", req)

    while True:
        restart_response = await restart_node(tester_node, node_info.node_id)
        if restart_response:
            break
    assert restart_response, "The device did not restart"
    await asyncio.sleep(5)
    while True:
        _logger.info("Sending a request to update to broken firmware")
        response = await command_client.call(req)
        if response:
            break
    assert response, "The device did not respond to the Execute command request."
    response = response[0]
    assert isinstance(response, uavcan.node.ExecuteCommand_1.Response)
    assert response.status == response.STATUS_SUCCESS, "Execute command response was not a success"
    print("Device restarted, good; waiting for the bootloader to finish...")
    await assert_does_bootloader_have_warning_heartbeat(tracker, node_info)


async def assert_repair_device_firmware(command_client):
    valid_firmware_path = get_valid_firmware_path()
    assert valid_firmware_path, "Valid firmware doesn't exist in the folder, maybe it is not built yet."
    # REPAIR THE DEVICE BY REPLACING THE FIRMWARE WITH A VALID ONE.
    req = uavcan.node.ExecuteCommand_1.Request(
        command=uavcan.node.ExecuteCommand_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE,
        parameter=valid_firmware_path,
    )
    print("Asking the bootloader to reinstall the valid firmware: %s", req)
    while True:
        response = await command_client.call(req)
        if response:
            break
    response = response[0]
    assert isinstance(response, uavcan.node.ExecuteCommand_1.Response)
    assert response.status == response.STATUS_SUCCESS


async def bootloader_test():
    _logger.info("Bootloader test started")
    tester_node = get_prepared_double_redundant_node()
    tracker: pycyphal.application.node_tracker = pycyphal.application.node_tracker.NodeTracker(tester_node)
    tracker.get_info_timeout = 1.0
    # Gathering heartbeats from any online nodes
    await asyncio.sleep(1)
    prepared_sapogs = await get_prepared_sapogs(tester_node)
    # Removing the debugger node
    # If no heartbeats were detected then the allocator is run

    if len(prepared_sapogs) == 0:
        our_allocator = make_simple_node_allocator()
        node_info_list = await our_allocator(node_to_use=tester_node, continuous=True,
                                             time_budget_seconds=2)
    else:
        node_info_list = prepared_sapogs
    if len(node_info_list) == 0:
        assert False, "There are no nodes to test"
    for index, node_info in enumerate(node_info_list):
        command_client = tester_node.make_client(uavcan.node.ExecuteCommand_1_1, node_info.node_id)
        command_client.response_timeout = 1.0
        if node_info.node_id == 2:
            continue
        await assert_send_empty_parameter_install_request(tester_node, node_info, command_client)
        file_server_root_path = "/"  # Path.cwd()
        # Launch the file server.
        file_server = pycyphal.application.file_server.FileServer(tester_node, [file_server_root_path], logger=_logger)
        _logger.debug("File server started")

        await assert_installing_invalid_firmware_doesnt_brick_device(tester_node, node_info, command_client, tracker)

        await assert_repair_device_firmware(command_client)

        await assert_does_bootloader_have_healthy_heartbeat(tracker, node_info)


if __name__ == "__main__":
    asyncio.run(bootloader_test())
