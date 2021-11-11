/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "heartbeat.hpp"
#include <node/units.hpp>
#include <node/time.h>

namespace node::essential
{
void publish_heartbeat(CanardInstance &canard, node::state::State &state)
{
    uavcan_node_Heartbeat_1_0 heartbeat{};
    heartbeat.uptime = (uint32_t) ((get_monotonic_microseconds() - state.timing.started_at) / MEGA);
    heartbeat.mode.value = uavcan_node_Mode_1_0_OPERATIONAL;
    heartbeat.health.value = uavcan_node_Health_1_0_NOMINAL;
    uint8_t serialized[uavcan_node_Heartbeat_1_0_SERIALIZATION_BUFFER_SIZE_BYTES_]{};
    size_t serialized_size = sizeof(serialized);
    const int8_t err = uavcan_node_Heartbeat_1_0_serialize_(&heartbeat, &serialized[0], &serialized_size);
    assert(err >= 0);
    if (err >= 0)
    {
        const CanardTransfer transfer = {
            .timestamp_usec = get_monotonic_microseconds() +
                              ONE_SECOND_DEADLINE_usec, // transmission deadline 1 second, optimal for heartbeat
            .priority       = CanardPriorityNominal,
            .transfer_kind  = CanardTransferKindMessage,
            .port_id        = uavcan_node_Heartbeat_1_0_FIXED_PORT_ID_,
            .remote_node_id = CANARD_NODE_ID_UNSET,
            .transfer_id    = (CanardTransferID) (state.transfer_ids.uavcan_node_heartbeat++),
            .payload_size   = serialized_size,
            .payload        = &serialized[0],
        };
        int32_t number_of_frames_enqueued = canardTxPush(&canard, &transfer);
        (void) number_of_frames_enqueued;
        assert(number_of_frames_enqueued > 0);
    }
}
}

