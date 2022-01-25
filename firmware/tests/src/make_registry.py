#
# Copyright (c) 2022 Zubax, zubax.com
# Distributed under the MIT License, available in the file LICENSE.
# Author: Silver Valdvee <silver.valdvee@zubax.com>
#
import typing

import pyuavcan

from uavcan import register
from util.get_available_interfaces import get_available_slcan_interfaces


def make_registry(node_id: int, interfaces: typing.List[str] = [], use_all_interfaces: bool = False):
    registry01: register.Registry = pyuavcan.application.make_registry(environment_variables={})
    if use_all_interfaces:
        registry01["uavcan.can.iface"] = " ".join(get_available_slcan_interfaces())
    else:
        registry01["uavcan.can.iface"] = " ".join(interfaces)
    registry01["uavcan.can.mtu"] = 8
    registry01["uavcan.node.id"] = node_id
    return registry01
