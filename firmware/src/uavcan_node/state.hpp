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
    uint8_t node_id;
    PNPStatus status = PNPStatus::Subscribing;
    bool anonymous = true;
};
struct State
{
    Timing timing;
    TransferIds transfer_ids;
    PlugAndPlay plug_and_play;
    os::config::Param<unsigned> param_node_id{"uavcan.node.id", 0, 0, 128};
    CanardInstance canard;
    int reduntant_interfaces[2] = {0, 1};
};
}
