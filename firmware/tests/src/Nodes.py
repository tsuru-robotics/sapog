from dataclasses import dataclass
from typing import Optional, List


@dataclass
class NodeInfo:
    """Is not node_id but a combination of node_id, hw_id, interfaces."""
    node_id: Optional[int]
    hw_id: str
    interfaces: List[str]

    def __init__(self, hw_id, interfaces):
        self.hw_id = hw_id
        self.interfaces = interfaces
        self.node_id = 0xFFFF
