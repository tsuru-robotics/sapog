import logging

import sys

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
from utils import get_prepared_sapogs, restart_node, command_save

_logger = logging.getLogger(__name__)
_logger.info(f"Current file {__file__}")

current_working_directory = Path(__file__).parent
_logger.info(f"Current working directory: {current_working_directory.absolute()}")
build_directory = (current_working_directory.parent.parent / "build").resolve()
_logger.info(f"Files in build directory ({build_directory.absolute()})")
_logger.info([str(x) for x in list(build_directory.glob("*"))])
valid_path = str(Path("build") / next(
    build_directory.glob("io.px4.sapog*.app.*.bin")).name)
_logger.info(valid_path)


def get_valid_firmware_path():
    return valid_path


def create_invalid_firmware():
    """Invalid firmware is needed to make sure the bootloader remains functional
    even if an invalid application image is installed after it in the memory.
    """
    _logger.info("Creating invalid firmware")
    broken_fw_path = (build_directory / "invalid_image_for_bootloader_test.bin").absolute()
    _logger.info(f"This path was established for the broken firmware: {broken_fw_path}")
    random_bytes = open("/dev/urandom", "rb").read(2000)
    _logger.info("Got the needed random bytes")
    with open(broken_fw_path, "wb") as broken_fw:
        broken_fw.write(random_bytes)
    _logger.info(f"Created the invalid image")
    assert os.path.exists(broken_fw_path), "Creating invalid image failed."
    return str(Path("build") / broken_fw_path.name)


async def assert_does_bootloader_have_warning_heartbeat(tracker, node_info):
    """Warning status needs to appear due to the overwriting with an incorrect image
    if the read response is not received then this heartbeat cannot have the right value"""
    entry = tracker.registry[node_info.node_id]
    _logger.info("Current state (should be in the bootloader and WARNING): %r", entry)
    assert entry.heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE
    assert entry.heartbeat.health.value == uavcan.node.Health_1.WARNING
    assert entry.info.name.tobytes().decode() == "io.px4.sapog"


async def assert_does_bootloader_have_healthy_heartbeat(tracker, node_info):
    deadline = asyncio.get_running_loop().time() + 120.0  # Uploading the new firmware does take some time
    while node_info.node_id not in tracker.registry:
        await asyncio.sleep(0.1)
    while tracker.registry[node_info.node_id].heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE:
        await asyncio.sleep(1.0)
        assert deadline > asyncio.get_running_loop().time()
        if node_info.node_id not in tracker.registry:
            break
    _logger.info("Bootloader execution finished")
    await asyncio.sleep(10.0)
    entry = tracker.registry[node_info.node_id]
    _logger.info("Current state (the application should be running normally): %r", entry)
    assert entry.heartbeat.mode.value == uavcan.node.Mode_1.OPERATIONAL
    assert entry.heartbeat.health.value == uavcan.node.Health_1.NOMINAL
    assert entry.info.name.tobytes().decode() == "io.px4.sapog"


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


async def assert_started_installing_invalid_firmware(tester_node, node_info, command_client, tracker):
    _logger.info("will now create invalid firmware")
    broken_fw_path = create_invalid_firmware()
    req = uavcan.node.ExecuteCommand_1.Request(
        command=uavcan.node.ExecuteCommand_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE,
        parameter=broken_fw_path,
    )
    # INSTALL INVALID FIRMWARE AND ENSURE THE DEVICE IS NOT BRICKED.

    _logger.info("Requesting the device to install an invalid firmware image: %s", req)

    while True:
        restart_response = await restart_node(tester_node, node_info.node_id)
        if restart_response:
            break
    assert restart_response, "The device did not restart"
    while True:
        _logger.info("Sending a request to update to broken firmware")
        response = await command_client.call(req)
        if response:
            _logger.info("Got a response on restarting.")
            break
    assert response, "The device did not respond to the Execute command request."
    response = response[0]
    assert isinstance(response, uavcan.node.ExecuteCommand_1.Response)
    assert response.status == response.STATUS_SUCCESS, "Execute command response was not a success"
    _logger.info("Device restarted, good; waiting for the bootloader to finish...")


async def assert_request_repair_device_firmware(command_client):
    valid_firmare_path = get_valid_firmware_path()
    assert valid_firmare_path, "Valid firmware doesn't exist in the folder, maybe it is not built yet."
    # REPAIR THE DEVICE BY REPLACING THE FIRMWARE WITH A VALID ONE.
    req = uavcan.node.ExecuteCommand_1.Request(
        command=uavcan.node.ExecuteCommand_1.Request.COMMAND_BEGIN_SOFTWARE_UPDATE,
        parameter=valid_firmare_path,
    )
    _logger.info("Asking the bootloader to reinstall the valid firmware: %s", req)
    while True:
        response = await command_client.call(req)
        if response:
            break
    response = response[0]
    assert isinstance(response, uavcan.node.ExecuteCommand_1.Response)
    _logger.info("Response received.")
    assert response.status == response.STATUS_SUCCESS
    _logger.info("Response status was a success")


async def wait_until_installation_is_started_and_finished(tracker, node_info, max_wait_time=120):
    deadline = asyncio.get_running_loop().time() + max_wait_time
    _logger.info("Waiting for the firmware update to begin")
    while node_info.node_id not in tracker.registry or tracker.registry[
        node_info.node_id].heartbeat.mode.value != uavcan.node.Mode_1.SOFTWARE_UPDATE:
        await asyncio.sleep(0.1)
        assert deadline > asyncio.get_running_loop().time()
    _logger.info("Waiting for the firmware update to end")
    while node_info.node_id in tracker.registry and tracker.registry[
        node_info.node_id].heartbeat.mode.value == uavcan.node.Mode_1.SOFTWARE_UPDATE \
            and tracker.registry[node_info.node_id].heartbeat.health.value != uavcan.node.Health_1.WARNING:
        await asyncio.sleep(1.0)
        assert deadline > asyncio.get_running_loop().time()


@pytest.mark.asyncio
async def test_bootloader(prepared_double_redundant_node):
    _logger.info("Bootloader test started, it has 4 steps.")
    tester_node = prepared_double_redundant_node
    tester_node.start()
    tracker: pyuavcan.application.node_tracker = pyuavcan.application.node_tracker.NodeTracker(tester_node)
    tracker.get_info_timeout = 1.0
    prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
    if len(prepared_sapogs) == 0:
        our_allocator = make_simple_node_allocator()
        node_info_list = await our_allocator(node_to_use=prepared_double_redundant_node, continuous=True,
                                             time_budget_seconds=2)
        for index, node_info in enumerate(node_info_list):
            await command_save(tester_node, node_info.node_id)
    else:
        node_info_list = prepared_sapogs
    if len(node_info_list) == 0:
        assert False, "There are no nodes to test"
    for index, node_info in enumerate(node_info_list):
        command_client = tester_node.make_client(uavcan.node.ExecuteCommand_1_1, node_info.node_id)
        command_client.response_timeout = 1.0
        is_target_node_a_debugger = node_info.node_id == 2
        if is_target_node_a_debugger:
            continue
        _logger.info("Step 1, sending a command to update firmware with the parameter empty, this should fail.")
        await assert_send_empty_parameter_install_request(tester_node, node_info, command_client)
        file_server_root_path = build_directory.parent.absolute()
        _logger.info(f"Created a file server in the background, the root path is {file_server_root_path}")
        file_server = pyuavcan.application.file.FileServer(tester_node, [file_server_root_path])
        _logger.debug("File server started")
        _logger.info("Step 2, Installing invalid firmware and making sure that the device doesn't get bricked.")
        _logger.info("The device should be emitting a warning heartbeat.")
        await assert_started_installing_invalid_firmware(tester_node, node_info, command_client, tracker)
        await wait_until_installation_is_started_and_finished(tracker, node_info)
        _logger.info("Invalid firmware installation finished")
        await assert_does_bootloader_have_warning_heartbeat(tracker, node_info)
        _logger.info("Step 3, Installing correct firmware to repair the device")
        await assert_request_repair_device_firmware(command_client)
        await wait_until_installation_is_started_and_finished(tracker, node_info)
        await assert_does_bootloader_have_healthy_heartbeat(tracker, node_info)
        _logger.info("Correct firmware installation finished")
        _logger.info("Bootloader test passed")
