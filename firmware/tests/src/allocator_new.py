#
# Copyright (c) 2021 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import json
import os
import pathlib
import sys
import re
from typing import Optional
from itertools import chain
import pyuavcan.dsdl
import typing

source_path = pathlib.Path(__file__).parent.absolute()
print(source_path.absolute())
dependency_path = source_path.parent / "deps"
print(dependency_path.absolute())
namespace_path = dependency_path / "namespaces"
print(namespace_path.absolute())
sys.path.insert(0, namespace_path.absolute())

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

do_update_dsdl = False
import subprocess
from pyuavcan.application import make_node, NodeInfo, Node
from pyuavcan.application.node_tracker import NodeTracker
from pyuavcan.application.plug_and_play import CentralizedAllocator
from pyuavcan.transport import _tracer
from pyuavcan.application.node_tracker import Entry
from pyuavcan.util import import_submodules, iter_descendants
import requests
import os.path

downloads_folder_name = "downloads"
assert (len(downloads_folder_name) > 4)
downloads_folder_name = downloads_folder_name.replace("*", "")
remove_zip_files_after_use = True




async def does_compiled_dsdl_directory_exist() -> bool:
    return os.path.isdir((source_path.parent / downloads_folder_name / "public_regulated_data_types-master").absolute())


async def does_sapog_directory_exist() -> bool:
    return os.path.isdir((source_path.parent / downloads_folder_name / "sapog-3").absolute())


async def get_info_about_archive_contents(archive_path: pathlib.Path) -> str:
    return subprocess.run(["unzip", "-l", archive_path], stdout=subprocess.PIPE).stdout


async def remove_previous_sapog_zip() -> None:
    subprocess.run(["rm", (source_path / "v3.zip").absolute()])


async def remove_previous_sapog_folder() -> None:
    subprocess.run(["rm", "-rf", (source_path.parent / downloads_folder_name / "sapog-3").absolute()])


async def build_sapog() -> None:
    subprocess.run(["make", "-j8"], cwd=(source_path.parent / downloads_folder_name / "sapog-3" / "firmware").absolute())


async def download_and_place_uavcan_dsdl() -> None:
    # making a request for downloading the zip file
    url = "https://github.com/UAVCAN/public_regulated_data_types/archive/refs/heads/master.zip"
    r = requests.get(url, allow_redirects=True)
    if os.path.isdir((source_path.parent / downloads_folder_name / "public_regulated_data_types-master").absolute()) and not do_update_dsdl:
        return
    if do_update_dsdl and does_compiled_dsdl_directory_exist():
        subprocess.run(["rm", "-rf", (source_path.parent / downloads_folder_name / "public_regulated_data_types-master").absolute()])

    # writing the received binary to a file
    public_regulated_data_types = open(source_path.parent / downloads_folder_name / "public_regulated_data_types.zip", "wb")
    public_regulated_data_types.write(r.content)
    public_regulated_data_types.close()
    # unzipping the zip file
    subprocess.run(["unzip", "-d", (source_path.parent / downloads_folder_name).absolute(), (source_path / "public_regulated_data_types.zip").absolute()])
    subprocess.run(
        ["mv", "-t",
         (source_path.parent / downloads_folder_name / "sapog-3" / "firmware" / "public_regulated_data_types").absolute(),
         # here
         (source_path.parent / downloads_folder_name / "public_regulated_data_types-master" / "uavcan").absolute(),  # move this
         (source_path.parent / downloads_folder_name / "public_regulated_data_types-master" / "reg").absolute()])  # and this


async def compile_dsdl():
    subprocess.run(["make", "dsdl"], cwd=(source_path.parent / downloads_folder_name / "sapog-3" / "firmware").absolute())


async def start_build_process() -> None:
    print(await get_info_about_archive_contents())

# await remove_previous_sapog_zip()
# await remove_previous_sapog_folder()
# await download_sapog_software_unpack()
# await download_and_place_uavcan_dsdl()
# await compile_dsdl()
# await build_sapog()


async def download_sapog_software_unpack() -> None:
    url = 'https://github.com/Zubax/sapog/archive/refs/heads/v3.zip'
    r = requests.get(url, allow_redirects=True)
    v3_zip_file = open(source_path.parent / "downloaded" / "v3.zip", "wb")
    v3_zip_file.write(r.content)
    v3_zip_file.close()
    subprocess.run(["unzip", "-d", (source_path.parent / "downloaded").absolute(), (source_path.parent / "downloaded" / "v3.zip").absolute()])


async def main() -> None:
    #asyncio.get_event_loop().create_task(start_build_process())
    os.environ["UAVCAN__CAN__IFACE"] = "socketcan:slcan0"
    os.environ["UAVCAN__CAN__MTU"] = "8"
    os.environ["UAVCAN__NODE__ID"] = "42"





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
