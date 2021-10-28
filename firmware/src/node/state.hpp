/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <zubax_chibios/config/config.hpp>
#include <libcanard/canard.h>

namespace node::state
{
struct Timing
{
    CanardMicrosecond next_pnp_request;
    CanardMicrosecond started_at;
    CanardMicrosecond current_time;
};
struct TransferIds
{
    uint64_t uavcan_node_heartbeat;
    uint64_t uavcan_node_port_list;
    uint64_t uavcan_pnp_allocation;
};
enum class PNPStatus
{
    Subscribing,
    TryingToSend,
    SentRequest,
    ReceivedResponse,
    Done
};
struct PlugAndPlay
{
    int request_count = 0;
    uint64_t unique_id_hash;
    PNPStatus status = PNPStatus::Subscribing;
    bool anonymous = true;
};
struct State
{
    bool is_restart_required = false;
    Timing timing;
    TransferIds transfer_ids;
    PlugAndPlay plug_and_play;
    CanardInstance canard;
    int reduntant_interfaces[2] = {0, 1};
};
}
