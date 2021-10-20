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

import_submodules(uavcan)
ids = {}
filtered_types = ["ABCMeta"]
chained_descendants = chain(iter_descendants(pyuavcan.dsdl.FixedPortCompositeObject),
                            iter_descendants(pyuavcan.dsdl.FixedPortServiceObject))
filtered_generator = (type_ for type_ in chained_descendants if type_ not in filtered_types)
for t in filtered_generator:
    ids[pyuavcan.dsdl.get_fixed_port_id(t)] = t


async def does_sapog_directory_exist() -> bool:
    return os.path.isdir((source_path.parent / "downloaded" / "sapog-3").absolute())


async def remove_previous_sapog_zip() -> None:
    subprocess.run(["rm", (source_path / "v3.zip").absolute()])


async def remove_previous_sapog_folder() -> None:
    subprocess.run(["rm", "-rf", (source_path.parent / "downloaded").absolute()])


async def build_sapog() -> None:
    subprocess.run(["make", "-j8"], cwd=(source_path.parent / "downloaded" / "sapog-3" / "firmware").absolute())


async def download_and_place_uavcan_dsdl() -> None:
    url = "https://github.com/UAVCAN/public_regulated_data_types/archive/refs/heads/master.zip"
    r = requests.get(url, allow_redirects=True)
    if os.path.isdir((source_path.parent / "downloaded" / "public_regulated_data_types-master")
                             .absolute()) and not do_update_dsdl:
        return
    if do_update_dsdl:
        subprocess.run(
            ["rm", "-rf", (source_path.parent / "downloaded" / "public_regulated_data_types-master").absolute()])
    public_regulated_data_types = open("public_regulated_data_types.zip", "wb")
    public_regulated_data_types.write(r.content)
    public_regulated_data_types.close()
    subprocess.run(["unzip", "-d", (source_path.parent / "downloaded").absolute(),
                    (source_path / "public_regulated_data_types.zip").absolute()])
    subprocess.run(
        ["mv", "-t",
         (source_path.parent / "downloaded" / "sapog-3" / "firmware" / "public_regulated_data_types").absolute(),
         # here
         (source_path.parent / "downloaded" / "public_regulated_data_types-master" / "uavcan").absolute(),  # move this
         (source_path.parent / "downloaded" / "public_regulated_data_types-master" / "reg").absolute()])  # and this


async def compile_dsdl():
    subprocess.run(["make", "dsdl"], cwd=(source_path.parent / "downloaded" / "sapog-3" / "firmware").absolute())


async def start_build_process() -> None:
    await remove_previous_sapog_zip()
    await remove_previous_sapog_folder()
    await download_sapog_software_unpack()
    await download_and_place_uavcan_dsdl()
    await compile_dsdl()
    await build_sapog()


async def download_sapog_software_unpack() -> None:
    url = 'https://github.com/Zubax/sapog/archive/refs/heads/v3.zip'
    r = requests.get(url, allow_redirects=True)
    v3_zip_file = open("v3.zip", "wb")
    v3_zip_file.write(r.content)
    v3_zip_file.close()
    subprocess.run(["unzip", "-d", (source_path.parent / "downloaded").absolute(), (source_path / "v3.zip").absolute()])


async def main() -> None:
    asyncio.get_event_loop().create_task(start_build_process())
    # with open("testfile.txt", "wb") as f:
    #    print(type(f))
    os.environ["UAVCAN__CAN__IFACE"] = "socketcan:slcan0"
    os.environ["UAVCAN__CAN__MTU"] = "8"
    os.environ["UAVCAN__NODE__ID"] = "42"
    with make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), "databases/node1.db") as node:
        tracer = node.presentation.transport.make_tracer()

        def capture_handler(capture: _tracer.Capture):
            with open("rx_frm.txt", "w") as log_file:
                if (transfer_trace := tracer.update(capture)) is not None:
                    subject_id = None
                    try:
                        subject_id = transfer_trace.transfer.metadata.session_specifier.data_specifier.subject_id
                    except Exception as e:
                        print(e.args[-1])
                    final_result = ""
                    count = 0
                    for memory_view in transfer_trace.transfer.fragmented_payload:
                        my_list = memory_view.tolist()
                        for byte in bytes(my_list):
                            final_result += '{:02X} '.format(byte)
                        else:
                            final_result = final_result[:len(final_result) - 1]
                        count += 1
                        if count >= 4:
                            final_result += "\n"
                            count = 0
                        else:
                            final_result += " | "
                    else:
                        final_result = final_result[:len(final_result) - len(" |")]
                    deserialized = str(transfer_trace.transfer)
                    obj = pyuavcan.dsdl.deserialize(ids[subject_id], transfer_trace.transfer.fragmented_payload)
                    print(obj)
                    print(json.dumps(pyuavcan.dsdl.to_builtin(obj)))
                    deserialized = re.sub(r"fragmented_payload=\[[^\[\]]+?\]", "\nPAYLOAD\n" + final_result,
                                          deserialized)
                    deserialized = deserialized.replace(
                        "AlienTransfer(AlienTransferMetadata(AlienSessionSpecifier(", "transfer(")[:-2]
                    for key, value in ids.items():
                        deserialized = deserialized.replace("subject_id=" + str(key),
                                                            "subject_id=" + value.__name__ + f"({str(key)})")
                        deserialized = deserialized.replace("service_id=" + str(key),
                                                            "service_id=" + value.__name__ + f"({str(key)})")
                    log_file.write(deserialized + "\n")

        node.presentation.transport.begin_capture(capture_handler)
        t = NodeTracker(node)
        a = CentralizedAllocator(node)

        def handle_getinfo_update(node_id: int, previous_entry: Optional[Entry], next_entry: Optional[Entry]):
            async def handle_inner_function():
                if node_id and next_entry and next_entry.info is not None:
                    print(next_entry.info)
                    a.register_node(node_id, bytes(next_entry.info.unique_id))
                    await asyncio.sleep(2)
                    # await reset_node_id(node, node_id)

            asyncio.get_event_loop().create_task(handle_inner_function())

        t.add_update_handler(handle_getinfo_update)
        print("Running")
        while True:
            await asyncio.sleep(1)


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
