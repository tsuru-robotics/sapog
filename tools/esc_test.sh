#!/usr/bin/bash
set -ex
y compile https://github.com/UAVCAN/public_regulated_data_types/zipball/master
export uavcan__pub__setpoint__id=135
export uavcan__pub__readiness__id=136
export uavcan__sub__esc_heartbeat__id=137
export uavcan__sub__feedback__id=138
export uavcan__sub__power__id=139
export uavcan__sub__status__id=140
export uavcan__sub__dynamics__id=141
export UAVCAN__CAN__IFACE="socketcan:slcan0 socketcan:slcan1"
export UAVCAN__NODE__ID=0
# Allocate node_ids
yakut pub -N 1 uavcan.pnp.NodeIDAllocationData.1.0 "{unique_id_hash: 75720222859564, allocated_node_id: {21}}"
yakut pub -N 1 uavcan.pnp.NodeIDAllocationData.1.0 "{unique_id_hash: 205537128692115, allocated_node_id: {22}}"
yakut call 21 uavcan.node.ExecuteCommand.1.1 "command: 65535" # Restart node
sleep 3
# Allocate node_ids
yakut pub -N 1 uavcan.pnp.NodeIDAllocationData.1.0 "{unique_id_hash: 75720222859564, allocated_node_id: {21}}"
yakut pub -N 1 uavcan.pnp.NodeIDAllocationData.1.0 "{unique_id_hash: 205537128692115, allocated_node_id: {22}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.sub.setpoint.id},  value: {natural16: {value: 135}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.sub.readiness.id}, value: {natural16: {value: 136}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.esc_heartbeat.id},    value: {natural16: {value: 137}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.feedback.id},    value: {natural16: {value: 138}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.power.id},     value: {natural16: {value: 139}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.status.id},    value: {natural16: {value: 140}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.dynamics.id},  value: {natural16: {value: 141}}}"

yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.sub.setpoint.id},  value: {natural16: {value: 142}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.sub.readiness.id}, value: {natural16: {value: 143}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.esc_heartbeat.id},    value: {natural16: {value: 144}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.feedback.id},    value: {natural16: {value: 145}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.power.id},     value: {natural16: {value: 146}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.status.id},    value: {natural16: {value: 147}}}"
yakut call 21 uavcan.register.Access.1.0 "{name: {name: uavcan.pub.dynamics.id},  value: {natural16: {value: 148}}}"

yakut call 21 uavcan.node.ExecuteCommand.1.1 "command: 65530" # Save persistent states
yakut call 21 uavcan.node.ExecuteCommand.1.1 "command: 65535" # Restart node
# Allocate node_ids
yakut pub -N 1 uavcan.pnp.NodeIDAllocationData.1.0 "{unique_id_hash: 75720222859564, allocated_node_id: {21}}"
yakut pub -N 1 uavcan.pnp.NodeIDAllocationData.1.0 "{unique_id_hash: 205537128692115, allocated_node_id: {22}}"

