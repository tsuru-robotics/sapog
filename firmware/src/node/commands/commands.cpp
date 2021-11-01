/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#include <uavcan/node/ExecuteCommand_1_1.h>
#include <cstdio>
#include "node/state.hpp"
#include "node/commands/commands.hpp"
#include "board/board.hpp"

bool
uavcan_node_ExecuteCommand_Request_1_1_handler(node::state::State &state, const CanardTransfer *const transfer)
{
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
            default:
                response.status = uavcan_node_ExecuteCommand_Response_1_1_STATUS_BAD_COMMAND;
        }
        (void) response;
        return true;
    }
    return false;
}