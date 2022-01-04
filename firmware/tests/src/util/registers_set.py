import sys
from pyuavcan.application import make_node, NodeInfo

from conftest import add_deps
from make_registry import make_registry

add_deps()
import asyncio

import uavcan.primitive.array.Bit_1_0
import uavcan.primitive.array.Integer64_1_0
import uavcan.register.Value_1_0
from numpy import ndarray
from my_simple_test_allocator import make_simple_node_allocator
from utils import make_access_request

import yaml


def prepared_double_redundant_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


async def main():
    with open("node_demo.yaml", "r") as f:
        node_id = sys.argv[1]
        register = yaml.load(f)
        tester_node = prepared_double_redundant_node()
        for key, value in register.items():
            get_type_response = await make_access_request(key,
                                                          uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                                          int(node_id),
                                                          tester_node)
            response = await make_access_request(key,
                                                 uavcan.register.Value_1_0(value),
                                                 int(node_id),
                                                 tester_node)


if __name__ == "__main__":
    asyncio.run(main())
