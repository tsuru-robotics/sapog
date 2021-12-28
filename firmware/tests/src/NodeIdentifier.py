from dataclasses import dataclass
from typing import Optional, List


@dataclass
class NodeIdentifier:
    node_id: Optional[int]
    hw_id: str
    interfaces: List[str]

    def __init__(self, hw_id, interfaces):
        self.hw_id = hw_id
        self.interfaces = interfaces
        self.node_id = 0xFFFF
