#ifndef FIRMWARE_STATE_HPP
#define FIRMWARE_STATE_HPP

#include <zubax_chibios/config/config.hpp>

namespace node::state
{
struct Timing
{
    CanardMicrosecond fast_loop_period;
    CanardMicrosecond next_fast_iter_at;
    CanardMicrosecond next_1_hz_iter_at;
    CanardMicrosecond next_01_hz_iter_at;
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
enum PNPStatus {
    Subscribing,
    TryingToSend,
    SentRequest,
    ReceivedResponse,
    Done
};
struct PlugAndPlay {
    int request_count = 0;
    PNPStatus status = Subscribing;
    bool anonymous = true;
    bool waitingForReply = false;
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
#endif //FIRMWARE_STATE_HPP
