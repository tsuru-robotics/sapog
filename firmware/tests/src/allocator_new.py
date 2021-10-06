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
from pyuavcan.application.node_tracker import Entry
from pyuavcan.util import import_submodules, iter_descendants

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

import_submodules(uavcan)
ids = {}
filtered_types = ["ABCMeta"]
chained_descendants = chain(iter_descendants(pyuavcan.dsdl.FixedPortCompositeObject), iter_descendants(pyuavcan.dsdl.FixedPortServiceObject))
filtered_generator = (type_ for type_ in chained_descendants if type_ not in filtered_types)
for t in filtered_generator:
    ids[pyuavcan.dsdl.get_fixed_port_id(t)] = t

source_path = pathlib.Path(__file__).parent
dependency_path = source_path.parent / "deps"
namespace_path = dependency_path / "namespaces"
sys.path.insert(0, namespace_path)

from pyuavcan.application import make_node, NodeInfo, Node
from pyuavcan.application.node_tracker import NodeTracker
from pyuavcan.application.plug_and_play import CentralizedAllocator
from pyuavcan.transport import _tracer


async def main() -> None:
    os.environ["UAVCAN__CAN__IFACE"] = "socketcan:slcan0"
    os.environ["UAVCAN__CAN__MTU"] = "8"
    os.environ["UAVCAN__NODE__ID"] = "42"
    with make_node(NodeInfo(name="com.zubax.sapog.tests.allocator"), "databases/node1.db") as node:
        tracer = node.presentation.transport.make_tracer()

        def capture_handler(capture: _tracer.Capture):
            with open("rx_frm.txt", "a") as log_file:
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
                    print(json.dumps(pyuavcan.dsdl.to_builtin(obj)))
                    deserialized = re.sub(r"fragmented_payload=\[[^\[\]]+?\]", "\nPAYLOAD\n" + final_result,
                                          deserialized)
                    deserialized = deserialized.replace(
                        "AlienTransfer(AlienTransferMetadata(AlienSessionSpecifier(", "transfer(")[:-2]
                    for key, value in ids.items():
                        deserialized = deserialized.replace("subject_id=" + str(key),
                                                            "subject_id=" + value.__name__  + f"({str(key)})")
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
