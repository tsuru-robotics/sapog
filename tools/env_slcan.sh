export UAVCAN__CAN__IFACE='socketcan:slcan0'
export UAVCAN__CAN__MTU=8
export UAVCAN__NODE__ID=$(yakut accommodate)

echo "Auto-selected node-ID for this session: $UAVCAN__NODE__ID"
