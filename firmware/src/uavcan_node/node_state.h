#ifndef FIRMWARE_NODE_STATE_H
#define FIRMWARE_NODE_STATE_H

#include <zubax_chibios/config/config.hpp>

namespace node { namespace state {
        struct Timing {
            CanardMicrosecond fast_loop_period;
            CanardMicrosecond next_fast_iter_at;
            CanardMicrosecond next_1_hz_iter_at;
            CanardMicrosecond next_01_hz_iter_at;
            CanardMicrosecond started_at;
            CanardMicrosecond current_time;
        };
        struct TransferIds {
            uint64_t uavcan_node_heartbeat;
            uint64_t uavcan_node_port_list;
            uint64_t uavcan_pnp_allocation;
        };
        struct Flags {

        };
        struct State {
            Timing timing;
            TransferIds transfer_ids;
            os::config::Param<unsigned> param_node_id{"uavcan.node.id", 0, 0, 128};
            CanardInstance canard;
            int reduntant_interfaces[2] = {0,1};
        };
} }
#endif //FIRMWARE_NODE_STATE_H
