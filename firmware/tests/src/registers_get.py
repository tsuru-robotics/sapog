import pathlib
import sys


def add_deps():
    """This is necessary to extend the python path with the compiled DSDL."""
    source_path = pathlib.Path(__file__).parent.absolute()
    dependency_path = source_path.parent / "deps"
    namespace_path = dependency_path / "namespaces"
    sys.path.insert(0, str(namespace_path.absolute()))


add_deps()
from pyuavcan.application import make_node, NodeInfo
from make_registry import make_registry
import asyncio

import uavcan.primitive.array.Bit_1_0
import uavcan.primitive.array.Integer64_1_0
import uavcan.register.Value_1_0
from numpy import ndarray
from my_simple_test_allocator import make_simple_node_allocator
from utils import make_access_request, get_prepared_sapogs

import yaml


def prepared_double_redundant_node():
    registry01 = make_registry(7, use_all_interfaces=True)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


def get_any_value_out_of_value(value: uavcan.register.Value_1_0):
    return_value = None
    is_float = False
    is_int = False
    is_bool = False
    is_str = False
    is_unstructured = False
    if value.empty is not None:
        return_value = None
    elif value.string is not None:
        return_value = ''.join(chr(i) for i in value.string.value)
        is_str = True
    elif value.unstructured is not None:
        return_value = value.unstructured
        is_unstructured = True
    elif value.bit is not None:
        return_value = value.bit.value
        is_bool = True
    elif value.integer64 is not None:
        return_value = value.integer64.value
        is_int = True
    elif value.integer32 is not None:
        return_value = value.integer32.value
        is_int = True
    elif value.integer16 is not None:
        return_value = value.integer16.value
        is_int = True
    elif value.integer8 is not None:
        return_value = value.integer8.value
        is_int = True
    elif value.natural64 is not None:
        return_value = value.natural64.value
        is_int = True
    elif value.natural32 is not None:
        return_value = value.natural32.value
        is_int = True
    elif value.natural16 is not None:
        return_value = value.natural16.value
        is_int = True
    elif value.natural8 is not None:
        return_value = value.natural8.value
        is_int = True
    elif value.real64 is not None:
        return_value = value.real64.value
        is_float = True
    elif value.real32 is not None:
        return_value = value.real32.value
        is_float = True
    elif value.real16 is not None:
        return_value = value.real16.value
        is_float = True

    if type(return_value) == ndarray:
        # if len(return_value) == 1:
        #     if is_int:
        #         return int(str(return_value[0]))
        #     elif is_float:
        #         return float(str(return_value[0]))
        #     elif is_bool:
        #         return bool(str(return_value[0]))
        #     else:
        #         return str(return_value[0])
        # else:
        return return_value.tolist()
    else:
        return return_value


async def main():
    tester_node = prepared_double_redundant_node()
    prepared_sapogs = await get_prepared_sapogs(tester_node)
    if len(prepared_sapogs) == 0:
        our_allocator = make_simple_node_allocator()
        node_info_list = await our_allocator(2, node_to_use=tester_node)
    else:
        node_info_list = prepared_sapogs
    for index, node_info in enumerate(node_info_list[:1]):
        service_client = tester_node.make_client(uavcan.register.List_1_0, node_info.node_id)
        service_client.response_timeout = 2
        counter = 0
        available_register_names = []
        register = {}
        while True:
            msg = uavcan.register.List_1_0.Request(counter)
            result = await service_client.call(msg)
            if result is None:
                service_client.close()
                assert False, "There was a problem getting a response from one of the nodes"
            message, transfer_info = result
            if (register_name := ''.join(chr(i) for i in message.name.name)) != "" and len(register_name) > 1:
                available_register_names.append(register_name)
                counter += 1
                await asyncio.sleep(0.01)
            else:
                service_client.close()
                break
        for register_name in available_register_names:
            response = await make_access_request(register_name,
                                                 uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                                 node_info.node_id,
                                                 tester_node)
            if response and response[0]:
                register[register_name] = get_any_value_out_of_value(response[0].value)
        print(yaml.dump(register, default_flow_style=False, allow_unicode=True))


if __name__ == "__main__":
    asyncio.run(main())
