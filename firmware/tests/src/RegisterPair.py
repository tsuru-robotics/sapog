#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import typing
from typing import Optional
import uavcan.register
from pyuavcan.dsdl import CompositeObject


class RegisterPair:
    def __init__(self, _tester_reg_name: Optional[str], _embedded_device_reg_name: Optional[str],
                 _value: uavcan.register.Value_1_0, _tester_counter: Optional[int],
                 type_communicated: Optional[typing.Type[CompositeObject]],
                 is_subscription: bool = False):
        self.tester_reg_name = _tester_reg_name
        self.embedded_device_reg_name = _embedded_device_reg_name
        self.value = _value
        self.tester_side_counter_number = _tester_counter
        self.communication_type = type_communicated
        self.is_subscription = False
        self.actual_subscription = None


class OnlyEmbeddedDeviceRegister(RegisterPair):
    def __init__(self, name: str, value: uavcan.register.Value_1_0):
        super().__init__(None, name, value, None, None)
