#pragma once

#include <uavcan/pnp/NodeIDAllocationData_2_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include "uavcan_node/plug_and_play/plug_and_play.hpp"
#include "uavcan_node/time.h"
#include "state.hpp"
#include "publishes.hpp"
#include "reception.hpp"

using namespace node::state;
namespace node::loops
{
void handle_1hz_loop(__attribute__((unused)) State &state)
{
    node::communications::publish_heartbeat(state.canard, state);
    communications::publish_port_list(state.canard, state);
}

inline void handle_fast_loop(__attribute__((unused)) State &state)
{
    receive_transfer(state, 0);
    std::optional<CanardTransfer> transfer = receive_transfer(state, 0);
    if (transfer.has_value())
    {
        process_received_transfer(state, &transfer.value());
    }
    transmit(state);
}
}