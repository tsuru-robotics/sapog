/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <uavcan/node/ExecuteCommand_1_1.h>
#include <cstdio>
#include <node/units.hpp>
#include <node/time.h>
#include <motor/motor.hpp>
#include "node/state.hpp"
#include "node/commands/commands.hpp"
#include "board/board.hpp"
#include <node/stop_gap.hpp>

UAVCAN_L6_NUNAVUT_C_SERVICE(uavcan_node_ExecuteCommand,
                            1, 1);

bool
uavcan_node_ExecuteCommand_Request_1_1_handler(node::state::State &state, const CanardTransfer *const transfer)
{
    (void) state;
    printf("Handling execute command\n");
    auto request = uavcan_l6::DSDL<uavcan_node_ExecuteCommand_Request_1_1>::deserialize(transfer->payload_size,
                                                                                        static_cast<const uint8_t *>(transfer->payload));
    if (request.has_value())
    {
        uavcan_node_ExecuteCommand_Response_1_1 response{};
        switch (request.value().command)
        {
            case uavcan_node_ExecuteCommand_Request_1_1_COMMAND_RESTART:
                state.is_restart_required = true;
                response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_SUCCESS;
                break;
            case uavcan_node_ExecuteCommand_Request_1_1_COMMAND_STORE_PERSISTENT_STATES:
                if (motor_is_idle())
                {
                    state.is_save_requested = true;
                    response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_SUCCESS;
                } else
                {
                    response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_BAD_STATE;
                }
                break;
            default:
                response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_BAD_COMMAND;
        }
        uavcan_l6::DSDL<uavcan_node_ExecuteCommand_Response_1_1>::Serializer serializer{};
        auto res = serializer.serialize(response);
        assert(res.has_value());
        if (res.has_value())
        {
            const CanardTransfer response_transfer = {
                .timestamp_usec = get_monotonic_microseconds() +
                                  ONE_SECOND_DEADLINE_usec, // transmission deadline 1 second, optimal for heartbeat
                .priority       = CanardPriorityNominal,
                .transfer_kind  = CanardTransferKindResponse,
                .port_id        = uavcan_node_ExecuteCommand_1_1_FIXED_PORT_ID_,
                .remote_node_id = transfer->remote_node_id,
                .transfer_id    = transfer->transfer_id,
                .payload_size   = res.value(),
                .payload        = serializer.getBuffer(),
            };
            int32_t number_of_frames_enqueued = canardTxPush(&state.canard, &response_transfer);
            (void) number_of_frames_enqueued;
            assert(number_of_frames_enqueued > 0);
        }
        return true;
    }
    return false;
}