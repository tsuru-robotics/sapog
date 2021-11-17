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

bool
uavcan_node_ExecuteCommand_Request_1_1_handler(node::state::State &state, const CanardTransfer *const transfer)
{
    (void) state;
    printf("Handling execute command\n");
    uavcan_node_ExecuteCommand_Request_1_1 request{};
    size_t size = transfer->payload_size;

    if (uavcan_node_ExecuteCommand_Request_1_1_deserialize_(&request,
                                                            (const uint8_t *) transfer->payload, &size) >= 0)
    {
        uavcan_node_ExecuteCommand_Response_1_1 response{};
        switch (request.command)
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
        uint8_t serialized[uavcan_node_ExecuteCommand_Response_1_1_EXTENT_BYTES_];
        size_t serialized_size = sizeof(serialized);
        const int8_t error = uavcan_node_ExecuteCommand_Response_1_1_serialize_(&response, &serialized[0],
                                                                                &serialized_size);
        assert(error >= 0);
        if (error >= 0)
        {
            const CanardTransfer response_transfer = {
                .timestamp_usec = get_monotonic_microseconds() +
                                  ONE_SECOND_DEADLINE_usec, // transmission deadline 1 second, optimal for heartbeat
                .priority       = CanardPriorityNominal,
                .transfer_kind  = CanardTransferKindResponse,
                .port_id        = uavcan_node_ExecuteCommand_1_1_FIXED_PORT_ID_,
                .remote_node_id = transfer->remote_node_id,
                .transfer_id    = transfer->transfer_id,
                .payload_size   = serialized_size,
                .payload        = &serialized[0],
            };
            int32_t number_of_frames_enqueued = canardTxPush(&state.canard, &response_transfer);
            (void) number_of_frames_enqueued;
            assert(number_of_frames_enqueued > 0);
        }
        return true;
    }
    return false;
}