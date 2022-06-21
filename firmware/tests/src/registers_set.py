import sys
from pycyphal.application import make_node, NodeInfo

from conftest import add_deps
from make_registry import make_registry

add_deps()
import asyncio

import uavcan.primitive.array.Bit_1_0
import uavcan.primitive.array.Integer64_1_0
import uavcan.register.Value_1_0
from utils import make_access_request

import yaml


def prepared_double_redundant_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


async def main():
    node_id = sys.argv[1]
    register = yaml.load(sys.stdin)
    tester_node = prepared_double_redundant_node()
    for key, value in register.items():
        if ".type" in key:
            continue
        if isinstance(value, int):
            value_to_be_sent = uavcan.register.Value_1_0(integer64=uavcan.primitive.array.Integer64_1_0([value]))
        elif isinstance(value, str):
            value_to_be_sent = uavcan.register.Value_1_0(string=uavcan.primitive.String_1_0(value))
        elif isinstance(value, bool):
            value_to_be_sent = uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0([value]))
        response = await make_access_request(key, value_to_be_sent, int(node_id), tester_node)


if __name__ == "__main__":
    asyncio.run(main())
