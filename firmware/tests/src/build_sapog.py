#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import os
import pathlib
import sys
import tempfile
import typing

source_path = pathlib.Path(__file__).parent.absolute()
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path.absolute())

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
from multiprocessing import cpu_count

do_update_dsdl = False
import subprocess
from pyuavcan.application import make_node, NodeInfo, Node

import requests
import os.path

downloads_folder_name = "downloads"
tracking_branch_name = "v3"
discard_local_changes = False
assert (len(downloads_folder_name) > 4)
downloads_folder_name = downloads_folder_name.replace("*", "")
remove_zip_files_after_use = True
sapog_root = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
firmware_directory = sapog_root / "firmware"
tests_directory = firmware_directory / "tests"


def get_port():
    from glob import glob
    output = subprocess.check_output(["realpath", "-LPz", glob("/dev/serial/by-id/usb-*Black_Magic_Probe*-if00")[0]]).decode("utf-8")[:-1]
    return output


def move_directories(destination: pathlib.Path, *source_dirs: pathlib.Path):
    subprocess.run(["mv", "-t", destination, *source_dirs])


async def upload_compound():
    temp_file = f"""tar ext {get_port()}
mon swdp_scan
attach 1
set mem inaccessible-by-default off
load
quit"""
    arguments = []
    for line in temp_file.split("\n"):
        arguments.append("-ex")
        arguments.append(f"{line.rstrip()}")  # https://manned.org/arm-none-eabi-gdb/7308522e
    subprocess.run(["arm-none-eabi-gdb", firmware_directory / "build" / "compound.elf", *arguments, "--batch"])


async def build_sapog() -> None:
    public_regulated_data_types_directory = (firmware_directory / "public_regulated_data_types").absolute()
    subprocess.run(["make", "clean"], cwd=firmware_directory)
    subprocess.run(["mkdir", firmware_directory / downloads_folder_name])
    if discard_local_changes:
        subprocess.run(["git", "checkout", "--force", tracking_branch_name])
    import zipfile
    # making a request for downloading the zip file
    url = "https://github.com/UAVCAN/public_regulated_data_types/archive/refs/heads/master.zip"
    r = requests.get(url, allow_redirects=True)
    if os.path.isdir((source_path.parent / downloads_folder_name / "public_regulated_data_types-master").absolute()) and not do_update_dsdl:
        return
    # writing the received binary to a file
    zip_path = firmware_directory / downloads_folder_name / "public_regulated_data_types.zip"
    public_regulated_data_types = open(zip_path, "wb")
    public_regulated_data_types.write(r.content)
    public_regulated_data_types.close()
    zip_file = zipfile.ZipFile(zip_path)
    name_list = zip_file.namelist()
    extra_parent_directory = name_list[0]
    zip_file.extractall(firmware_directory / downloads_folder_name)
    print(extra_parent_directory)
    zip_file.close()
    subprocess.run(["mkdir", public_regulated_data_types_directory])
    move_directories(public_regulated_data_types_directory,
                     (firmware_directory / downloads_folder_name / extra_parent_directory / "uavcan").absolute(),
                     (firmware_directory / downloads_folder_name / extra_parent_directory / "reg").absolute())
    subprocess.run(["make", "dsdl"], cwd=firmware_directory)
    subprocess.run(["make", f"-j{cpu_count()}"], cwd=firmware_directory)


async def compile_dsdl():
    subprocess.run(["make", "dsdl"], cwd=(source_path.parent / downloads_folder_name / "sapog-3" / "firmware").absolute())


async def start_build_process() -> None:
    await build_sapog()


async def main() -> None:
    await build_sapog()
    await upload_compound()
    # while True:
    #     await asyncio.sleep(1)


already_ran = False


async def reset_node_id(sending_node: Node, current_target_node_id: int) -> bool:
    print(f"Resetting node_id of {current_target_node_id}")
    global already_ran
    if already_ran:
        return
    already_ran = True
    service_client = sending_node.make_client(uavcan.register.Access_1_0, current_target_node_id)
    msg = uavcan.register.Access_1_0.Request()
    my_array = uavcan.primitive.array.Integer64_1_0()
    my_array.value = [1]
    msg.name.name = "uavcan_node_id"
    msg.value.integer64 = my_array
    response = await service_client.call(msg)
    print(response)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
