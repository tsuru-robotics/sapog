/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "heartbeat.hpp"
#include "libcanard/canard.h"
#include <node/units.hpp>
#include "uavcan/_register/List_1_0.h"
#include <node/time.h>
#include <node/stop_gap.hpp>

std::string_view all_register_names[] = {
    "uavcan.sub.note_response.id\0", "uavcan.sub.note_response.type\0",
    "uavcan.sub.setpoint.id\0", "uavcan.sub.setpoint.type\0",
    "id_in_esc_group\0",
    "uavcan.sub.readiness.id\0", "uavcan.sub.readiness.type\0",
    "ttl_milliseconds\0",
    "uavcan.pub.esc_heartbeat.id\0", "uavcan.pub.esc_heartbeat.type\0",
    "uavcan.pub.esc_feedback.id\0", "uavcan.pub.esc_feedback.type\0",
    "uavcan.pub.esc_power.id\0", "uavcan.pub.esc_power.type\0",
    "uavcan.pub.esc_dynamics.id\0", "uavcan.pub.esc_dynamics.type\0",
    "control_mode_rpm\0"
};

UAVCAN_L6_NUNAVUT_C_SERVICE(uavcan_register_List, 1, 0);
namespace node::essential
{
struct : IHandler
{
    void operator()(node::state::State &state, CanardRxTransfer *transfer)
    {
        auto request =
            uavcan_l6::DSDL<uavcan_register_List_Request_1_0>
            ::deserialize(transfer->payload_size,
                          static_cast<const uint8_t *>(transfer->payload));
        auto serializer = uavcan_l6::DSDL<uavcan_register_List_Response_1_0>::Serializer();
        auto response_value = uavcan_register_List_Response_1_0{};
        if (sizeof(all_register_names) / sizeof(all_register_names[0]))
        {
            std::copy(std::begin(all_register_names[request->index]),
                      std::end(all_register_names[request->index]),
                      std::begin(response_value.name.name.elements));
            response_value.name.name.count =
                sizeof(all_register_names[request->index]) / sizeof(all_register_names[request->index][0]);
        } else
        {
            response_value.name.name.elements[0] = '\0';
            response_value.name.name.count = 1;
        }
        auto res = serializer.serialize(response_value);
        CanardTransferMetadata rtm = transfer->metadata;  // Response transfers are similar to their requests.
        rtm.transfer_kind = CanardTransferKindResponse;
        for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
        {
            int32_t number_of_frames_enqueued = canardTxPush(&state.queues[i],
                                                             const_cast<CanardInstance *>(&state.canard),
                                                             get_monotonic_microseconds() +
                                                             ONE_SECOND_DEADLINE_usec,
                                                             &rtm,
                                                             res.value(),
                                                             serializer.getBuffer());

            (void) number_of_frames_enqueued;
            assert(number_of_frames_enqueued > 0);
        }
        return;
    }
} uavcan_register_List_1_0_handler;
}

