/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "heartbeat.hpp"
#include <node/units.hpp>
#include <node/time.h>
#include <node/stop_gap.hpp>

UAVCAN_L6_NUNAVUT_C_MESSAGE(uavcan_node_Heartbeat, 1, 0);
namespace node::essential
{
void publish_heartbeat(CanardInstance &canard, node::state::State &state)
{
    (void) canard;
    uavcan_node_Heartbeat_1_0 heartbeat{};
    heartbeat.uptime = (uint32_t) ((get_monotonic_microseconds() - state.timing.started_at) / MEGA);
    heartbeat.mode.value = uavcan_node_Mode_1_0_OPERATIONAL;
    heartbeat.health.value = uavcan_node_Health_1_0_NOMINAL;
    uavcan_l6::DSDL<uavcan_node_Heartbeat_1_0>::Serializer serializer{};
    auto serialized_size = serializer.serialize(heartbeat);
    assert(serialized_size.has_value());
    if (serialized_size.has_value())
    {
        CanardTransferMetadata rtm{};  // Response transfers are similar to their requests.
        rtm.transfer_kind = CanardTransferKindMessage;
        rtm.port_id = uavcan_node_Heartbeat_1_0_FIXED_PORT_ID_;
        rtm.transfer_id = (CanardTransferID) (state.transfer_ids.uavcan_node_heartbeat++);
        rtm.remote_node_id = CANARD_NODE_ID_UNSET;
        rtm.priority = CanardPriorityNominal;
        for (int i = 0; i < AMOUNT_OF_QUEUES; ++i)
        {
            int32_t number_of_frames_enqueued = canardTxPush(&state.queues[i],
                                                             const_cast<CanardInstance *>(&state.canard),
                                                             get_monotonic_microseconds() +
                                                             ONE_SECOND_DEADLINE_usec,
                                                             &rtm,
                                                             serialized_size.value(),
                                                             serializer.getBuffer());

            (void) number_of_frames_enqueued;
            assert(number_of_frames_enqueued > 0);
        }
    }
}
}

