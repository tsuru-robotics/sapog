#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import asyncio
import json
import typing

import math
import pytest
import pycyphal
import time

import reg.udral.physics.dynamics.rotation.PlanarTs_0_1
import reg.udral.physics.electricity.PowerTs_0_1
import reg.udral.service.actuator.common.Feedback_0_1
import reg.udral.service.actuator.common.Status_0_1
import reg.udral.service.actuator.common.sp.Scalar_0_1
import reg.udral.service.common.Readiness_0_1
import uavcan.primitive.array.Bit_1_0
import uavcan.primitive.array.Integer64_1_0
import uavcan.register.Value_1_0
from numpy import clip, ndarray
from my_simple_test_allocator import make_simple_node_allocator
from RegisterPair import RegisterPair, OnlyEmbeddedDeviceRegister
from utils import rpm_to_radians_per_second, restart_node, \
    command_save, configure_embedded_registers, configure_tester_side_registers, make_access_request

from node_fixtures.drnf import prepared_double_redundant_node

import yaml


def get_any_value_out_of_value(value: uavcan.register.Value_1_0):
    return_value = None
    if value.empty is not None:
        return_value = None
    elif value.string is not None:
        return_value = ''.join(chr(i) for i in value.string.value)
    elif value.unstructured is not None:
        return_value = value.unstructured
    elif value.bit is not None:
        return_value = value.bit.value
    elif value.integer64 is not None:
        return_value = value.integer64.value
    elif value.integer32 is not None:
        return_value = value.integer32.value
    elif value.integer16 is not None:
        return_value = value.integer16.value
    elif value.integer8 is not None:
        return_value = value.integer8.value
    elif value.natural64 is not None:
        return_value = value.natural64.value
    elif value.natural32 is not None:
        return_value = value.natural32.value
    elif value.natural16 is not None:
        return_value = value.natural16.value
    elif value.natural8 is not None:
        return_value = value.natural8.value
    elif value.real64 is not None:
        return_value = value.real64.value
    elif value.real32 is not None:
        return_value = value.real32.value
    elif value.real16 is not None:
        return_value = value.real16.value

    if type(return_value) == ndarray:
        if len(return_value) == 1:
            return str(return_value[0])
        else:
            return return_value.tolist()
    else:
        return return_value


class TestRegisterValues:
    @staticmethod
    @pytest.mark.asyncio
    async def test_port_list_full(prepared_double_redundant_node):
        our_allocator = make_simple_node_allocator()
        tester_node = prepared_double_redundant_node
        node_info_list = await our_allocator(2, node_to_use=tester_node)
        for index, node_info in enumerate(node_info_list):
            node_info.motor_index = index
            service_client = tester_node.make_client(uavcan.register.List_1_0, node_info.node_id)
            service_client.response_timeout = 2
            counter = 0
            available_register_names = []
            register = {}
            while True:
                msg = uavcan.register.List_1_0.Request(counter)
                result: uavcan.register.List_1_0.Response = (await service_client.call(msg))[0]
                if (register_name := ''.join(chr(i) for i in result.name.name)) != "" and len(register_name) > 1:
                    available_register_names.append(register_name)
                    counter += 1
                    asyncio.sleep(0.01)
                else:
                    break
            for register_name in available_register_names:
                response = await make_access_request(register_name,
                                                     uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                                     node_info,
                                                     tester_node)
                if response and response[0]:
                    register[register_name] = get_any_value_out_of_value(response[0].value)
            print(yaml.dump(register, default_flow_style=False, allow_unicode=True))
