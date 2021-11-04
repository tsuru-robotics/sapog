from pyuavcan.application import Node

import uavcan


def configure_note_on_sapog(sending_node: Node, current_target_node_id: int):
    service_client = sending_node.make_client(uavcan.register.Access_1_0, current_target_node_id)
