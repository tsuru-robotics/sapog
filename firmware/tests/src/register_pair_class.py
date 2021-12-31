import typing
from typing import Optional
import uavcan.register
from pyuavcan.dsdl import CompositeObject


class RegisterPair():
    def __init__(self, _tester_reg_name: Optional[str], _embedded_device_reg_name: Optional[str],
                 _value: uavcan.register.Value_1_0, _tester_counter: int,
                 type_communicated: typing.Type[CompositeObject]):
        self.tester_reg_name = _tester_reg_name
        self.embedded_device_reg_name = _embedded_device_reg_name
        self.value = _value
        self.tester_side_counter_number = _tester_counter
        self.communication_type = type_communicated


class OnlyEmbeddedDeviceRegister(RegisterPair):
    def __init__(self, name: str, value: uavcan.register.Value_1_0):
        super().__init__(None, name, value)
