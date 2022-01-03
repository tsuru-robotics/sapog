import typing
from dataclasses import dataclass
from typing import Optional, List

from pyuavcan.application._node import MessageClass
from pyuavcan.dsdl import CompositeObject
from pyuavcan.presentation import Subscriber

from RegisterPair import RegisterPair


@dataclass
class NodeInfo:
    """Is not node_id but a combination of node_id, hw_id, interfaces."""
    node_id: Optional[int]
    hw_id: str
    interfaces: List[str]
    motor_index: Optional[int]
    registers: List[RegisterPair]
    subscription_store: typing.Mapping[typing.Tuple[int, str], Subscriber[MessageClass]]
    target_rpm: float = 200

    def __init__(self, hw_id, interfaces, node_id=0xFFFF):
        self.hw_id = hw_id
        self.interfaces = interfaces
        self.node_id = node_id
        self.motor_index = None
        self.registers = []

    def store_subscription(self, sub: Subscriber[MessageClass], subject_id: int, name: str,
                           data_type: typing.Type[CompositeObject]):
        self.subscription_store[(data_type, name, subject_id)] = sub

    def get_subscription(self, what_to_look_for_in_key):
        return next(filter(lambda x: what_to_look_for_in_key in x,
                           self.subscription_store.keys()), None)
