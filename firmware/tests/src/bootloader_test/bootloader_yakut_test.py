import asyncio
import logging
import os
import subprocess
from pathlib import Path

import pytest
import pyuavcan
import pyuavcan.application.node_tracker
import sys

import uavcan
from my_simple_test_allocator import make_simple_node_allocator
from node_fixtures.drnf import prepared_double_redundant_node
from utils import get_prepared_sapogs

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


async def run_yakut_file_server():
    my_env = os.environ.copy()
    # my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
    my_env["UAVCAN__CAN__MTU"] = "8"
    my_env["UAVCAN__NODE__ID"] = "126"
    my_env["UAVCAN__CAN__IFACE"] = "socketcan:slcan0"
    yakut_path = "/home/silver/.local/bin/yakut"
    namespaces_path = Path.cwd().parent.parent / 'deps' / 'namespaces'
    my_env["PYTHONPATH"] = f"{namespaces_path}:{my_env['PYTHONPATH']}"
    _logger.info("Starting yakut fileserver")
    process = subprocess.Popen(
        ["pwd"],
        # [f"{yakut_path}", "--path", namespaces_path, "file-server", "+U", f"{Path.cwd().parent.absolute()}"],
        env=my_env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):  # replace '' with b'' for Python 3
        sys.stdout.write(line)


@pytest.mark.asyncio
async def test_bootloader(prepared_double_redundant_node):
    prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
    if len(prepared_sapogs) == 0:
        our_allocator = make_simple_node_allocator()
        node_info_list = await our_allocator(node_to_use=prepared_double_redundant_node,
                                             continuous=True,
                                             time_budget_seconds=2)
    else:
        node_info_list = prepared_sapogs
    tester_node = prepared_double_redundant_node
    tracker: pyuavcan.application.node_tracker = pyuavcan.application.node_tracker.NodeTracker(tester_node)
    loop = asyncio.get_event_loop()
    task = loop.create_task(run_yakut_file_server())
    for index, node_info in enumerate(node_info_list):
        await assert_does_bootloader_have_warning_heartbeat(tracker, node_info)
    task.cancel()
