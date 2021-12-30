from typing import Optional

import uavcan.register
from imports import add_deps

add_deps()


class RegisterPair():
    def __init__(self, _tester_reg_name: Optional[str], _embedded_device_reg_name: Optional[str],
                 _value: uavcan.register.Value_1_0):
        self.tester_reg_name = _tester_reg_name
        self.embedded_device_reg_name = _embedded_device_reg_name
        self.value = _value


class OnlyEmbeddedDeviceRegister(RegisterPair):
    def __init__(self, name: str, value: uavcan.register.Value_1_0):
        super().__init__(None, name, value)
