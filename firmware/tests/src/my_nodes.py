import typing
from dataclasses import dataclass
from typing import Optional, List

from pyuavcan.application._node import MessageClass
from pyuavcan.presentation import Subscriber

from register_pair_class import RegisterPair


@dataclass
class NodeInfo:
    """Is not node_id but a combination of node_id, hw_id, interfaces."""
    node_id: Optional[int]
    hw_id: str
    interfaces: List[str]
    motor_index: Optional[int]
    registers: List[RegisterPair]
    subscription_store: typing.Mapping[Subscriber[MessageClass]]
    target_rpm: float = 200

    def __init__(self, hw_id, interfaces, node_id=0xFFFF):
        self.hw_id = hw_id
        self.interfaces = interfaces
        self.node_id = node_id
        self.motor_index = None
