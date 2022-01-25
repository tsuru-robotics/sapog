#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import os

import pytest
import time

from utils import make_access_request, get_prepared_sapogs

from node_fixtures.drnf import prepared_double_redundant_node

is_running_on_my_laptop = os.path.exists("/home/silver")

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array
import uavcan.register.List_1_0


class TestRegisters:
    @pytest.mark.asyncio
    async def test_register_list(self, prepared_double_redundant_node):
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(prepared_sapogs) > 0
        for node_info in prepared_sapogs:
            service_client = prepared_double_redundant_node.make_client(uavcan.register.List_1_0, node_info.node_id)
            service_client.response_timeout = 1
            msg = uavcan.register.List_1_0.Request(20)
            result = await service_client.call(msg)
            print(result)
            assert result is not None

    @pytest.mark.asyncio
    async def test_write_unsupported_sapog_register(self, prepared_double_redundant_node):
        """Checks if the response is empty when writing to a register that doesn't exit on Sapog.
        uavcan.node.description is a register that would exist on other nodes but on this node, only storage of floats
        is implemented and string storage is not supported."""
        time.sleep(0.2)
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(prepared_sapogs) > 0
        for node_info in prepared_sapogs:
            response = await make_access_request("uavcan.node.description",
                                                 uavcan.register.Value_1_0(string=uavcan.primitive.String_1_0("named")),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            is_result_good = response is not None and response[0].value.empty is not None
            assert is_result_good
            if not is_result_good:
                return

    @pytest.mark.asyncio
    async def test_write_supported_sapog_register_int(self, prepared_double_redundant_node):
        """Writes a non-default value and checks if it was successfully saved. Then writes back the default value and
        checks if that was saved."""
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(prepared_sapogs) > 0
        for node_info in prepared_sapogs:
            response = await make_access_request("mot_pwm_hz",
                                                 uavcan.register.Value_1_0(
                                                     integer64=uavcan.primitive.array.Integer64_1_0(60001)),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            if response:
                int_value = response[0].value.integer64
                if int_value:
                    if int_value.value.size == 1:
                        returned_value = response[0].value.integer64.value.tolist()[0]
                        print(type(returned_value))
                        assert returned_value == 60001
                    else:
                        print(f"Size should be 1 but is {int_value.value.size}")
                else:
                    print("response[0].value.bit is None")
            else:
                print("Response is None")
            response = await make_access_request("mot_pwm_hz",
                                                 uavcan.register.Value_1_0(
                                                     integer64=uavcan.primitive.array.Integer64_1_0(60000)),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            if response:
                int_value = response[0].value.integer64
                if int_value:
                    if int_value.value.size == 1:
                        returned_value = response[0].value.integer64.value.tolist()[0]
                        print(type(returned_value))
                        assert returned_value == 60000
                        return
                    else:
                        print(f"Size should be 1 but is {int_value.value.size}")
                else:
                    print("response[0].value.integer64 is None")
            else:
                print("Response is None")
            assert False

    @pytest.mark.asyncio
    async def test_write_supported_sapog_register_bit(self, prepared_double_redundant_node):
        """Writes to a register and checks the value to match what was written, then writes the opposite value and
        checks again to see if it was saved correctly."""
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(prepared_sapogs) > 0
        for node_info in prepared_sapogs:
            response = await make_access_request("pwm_enable",
                                                 uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(1)),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            if response:
                bit_value = response[0].value.bit
                if bit_value:
                    if bit_value.value.size == 1:
                        returned_value = response[0].value.bit.value.tolist()[0]
                        print(type(returned_value))
                        if returned_value == True:
                            assert True
                        else:
                            print(f"Returned value should be 0 but is {returned_value}")
                    else:
                        print(f"Size should be 1 but is {bit_value.value.size}")
                else:
                    print("response[0].value.bit is None")
            else:
                print("Response is None")
            response = await make_access_request("pwm_enable",
                                                 uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(0)),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            if response:
                bit_value = response[0].value.bit
                if bit_value:
                    if bit_value.value.size == 1:
                        returned_value = response[0].value.bit.value.tolist()[0]
                        print(type(returned_value))
                        if returned_value == False:
                            assert True
                            return
                        else:
                            print(f"Returned value should be 1 but is {returned_value}")
                    else:
                        print(f"Size should be 1 but is {bit_value.value.size}")
                else:
                    print("response[0].value.bit is None")
            else:
                print("Response is None")
            assert False

    @pytest.mark.asyncio
    async def test_read_existing_register_float(self, prepared_double_redundant_node):
        """The read test doesn't check if the value matches anything, just if it is the correct datatype and that
        there is one of it."""
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(prepared_sapogs) > 0
        for node_info in prepared_sapogs:
            response = await make_access_request("rpmctl_p",
                                                 uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            if response:
                real_value = response[0].value.real64
                if real_value:
                    if real_value.value.size == 1:
                        returned_value = response[0].value.real64.value.tolist()[0]
                        print(type(returned_value))
                        assert returned_value is not None
                        return
                    else:
                        print(f"Size should be 1 but is {real_value.value.size}")
                else:
                    print("response[0].value.real64 is None")
            else:
                print("Response is None")
            assert False

    @pytest.mark.asyncio
    async def test_read_existing_register_bool(self, prepared_double_redundant_node):
        """The read test doesn't check if the value matches anything, just if it is the correct datatype and that
        there is one of it."""
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(prepared_sapogs) > 0
        for node_info in prepared_sapogs:
            response = await make_access_request("pwm_enable",
                                                 uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            if response:
                bit_value = response[0].value.bit
                if bit_value:
                    if bit_value.value.size == 1:
                        returned_value = response[0].value.bit.value.tolist()[0]
                        assert returned_value is not None
                        return
                    else:
                        print(f"Size should be 1 but is {bit_value.value.size}")
                else:
                    print("response[0].value.bit is None")
            else:
                print("Response is None")
            assert False

    @pytest.mark.asyncio
    async def test_read_existing_register_int(self, prepared_double_redundant_node):
        """The read test doesn't check if the value matches anything, just if it is the correct datatype and that
        there is one of it."""
        prepared_sapogs = await get_prepared_sapogs(prepared_double_redundant_node)
        assert len(prepared_sapogs) > 0
        for node_info in prepared_sapogs:
            response = await make_access_request("mot_tim_adv_min",
                                                 uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                                 node_info.node_id,
                                                 prepared_double_redundant_node)
            if response:
                real_value = response[0].value.integer64
                if real_value:
                    if real_value.value.size == 1:
                        returned_value = response[0].value.integer64.value.tolist()[0]
                        print(type(returned_value))
                        assert returned_value is not None
                        return
                    else:
                        print(f"Size should be 1 but is {real_value.value.size}")
                else:
                    print("response[0].value.real is None")
            else:
                print("Response is None")
            assert False
