import asyncio
import os
import time

from asyncio import exceptions

import pytest

from my_simple_test_allocator import allocate_nr_of_nodes
from utils import make_access_request

is_running_on_my_laptop = os.path.exists("/home/silver")

from imports import add_deps

add_deps()

import uavcan.pnp.NodeIDAllocationData_1_0
import uavcan.node.ID_1_0
import uavcan.register.Access_1_0
import uavcan.primitive.array

import pyuavcan
from pyuavcan.application import Node, make_node, NodeInfo, register
from pyuavcan.presentation._presentation import MessageClass

from _await_wrap import wrap_await


def is_device_with_node_id_running(node_id):
    """This creates a new node with node_id 3 that will look for heart beats from node_id."""
    registry01 = make_registry(3)
    with make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01) as node:
        subscriber = node.make_subscriber(uavcan.node.Heartbeat_1_0)
        event = asyncio.Event()

        def hb_handler(message_class: MessageClass,
                       transfer_from: pyuavcan.transport._transfer.TransferFrom):
            if transfer_from.source_node_id == node_id:
                event.set()

        subscriber.receive_in_background(hb_handler)
        try:
            wrap_await(asyncio.wait_for(event.wait(), 1.7))
        except exceptions.TimeoutError as e:
            return False
        return True


@pytest.fixture(scope="class")
def prepared_node():
    registry01 = make_registry(7)
    return make_node(NodeInfo(name="com.zubax.sapog.tests.tester"), registry01)


@pytest.fixture(scope="class")
def prepared_sapogs():
    if is_device_with_node_id_running(21) and is_running_on_my_laptop:
        print("Device with node id 21 is already running so I will use that.")
        return {21: "idk"}
    else:
        return allocate_nr_of_nodes(1)  # This will allocate id 21 too


@pytest.fixture()
def restarted_sapogs():
    global is_running_on_my_laptop
    return allocate_nr_of_nodes(1)


def make_registry(node_id: int):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    registry01["uavcan.can.iface"] = "socketcan:slcan0"
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = node_id
    return registry01


class TestRegisters:
    def test_write_unsupported_sapog_register(self, prepared_node, prepared_sapogs):
        """Checks if the response is empty when writing to a register that doesn't exit on Sapog.
        uavcan.node.description is a register that would exist on other nodes but on this node, only storage of floats
        is implemented and string storage is not supported."""
        time.sleep(0.2)
        assert len(prepared_sapogs.keys()) > 0
        for node_id in prepared_sapogs.keys():  # resource.keys():
            response = make_access_request("uavcan.node.description",
                                           uavcan.register.Value_1_0(string=uavcan.primitive.String_1_0("named")),
                                           node_id,
                                           prepared_node)
            is_result_good = response is not None and response[0].value.empty is not None
            assert is_result_good
            if not is_result_good:
                return

    def test_write_supported_sapog_register_int(self, prepared_node, prepared_sapogs):
        """Writes a non-default value and checks if it was successfully saved. Then writes back the default value and
        checks if that was saved."""
        assert len(prepared_sapogs.keys()) > 0
        for node_id in prepared_sapogs.keys():  # resource.keys():
            response = make_access_request("mot_pwm_hz",
                                           uavcan.register.Value_1_0(
                                               integer64=uavcan.primitive.array.Integer64_1_0(60001)),
                                           node_id,
                                           prepared_node)
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
            response = make_access_request("mot_pwm_hz",
                                           uavcan.register.Value_1_0(
                                               integer64=uavcan.primitive.array.Integer64_1_0(60000)),
                                           node_id,
                                           prepared_node)
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

    def test_write_supported_sapog_register_bit(self, prepared_node, prepared_sapogs):
        """Writes to a register and checks the value to match what was written, then writes the opposite value and
        checks again to see if it was saved correctly."""
        assert len(prepared_sapogs.keys()) > 0
        for node_id in prepared_sapogs.keys():  # resource.keys():
            response = make_access_request("pwm_enable",
                                           uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(1)),
                                           node_id,
                                           prepared_node)
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
            response = make_access_request("pwm_enable",
                                           uavcan.register.Value_1_0(bit=uavcan.primitive.array.Bit_1_0(0)),
                                           node_id,
                                           prepared_node)
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

    def test_read_existing_register_float(self, prepared_node, prepared_sapogs):
        """The read test doesn't check if the value matches anything, just if it is the correct datatype and that
        there is one of it."""
        assert len(prepared_sapogs.keys()) > 0
        for node_id in prepared_sapogs.keys():  # resource.keys():
            response = make_access_request("rpmctl_p", uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                           node_id,
                                           prepared_node)
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

    def test_read_existing_register_bool(self, prepared_node, prepared_sapogs):
        """The read test doesn't check if the value matches anything, just if it is the correct datatype and that
        there is one of it."""
        assert len(prepared_sapogs.keys()) > 0
        for node_id in prepared_sapogs.keys():  # resource.keys():
            response = make_access_request("pwm_enable", uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                           node_id,
                                           prepared_node)
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

    def test_read_existing_register_int(self, prepared_node, prepared_sapogs):
        """The read test doesn't check if the value matches anything, just if it is the correct datatype and that
        there is one of it."""
        assert len(prepared_sapogs.keys()) > 0
        for node_id in prepared_sapogs.keys():
            response = make_access_request("mot_tim_adv_min",
                                           uavcan.register.Value_1_0(empty=uavcan.primitive.Empty_1_0()),
                                           node_id,
                                           prepared_node)
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
