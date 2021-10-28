#pragma once

#include <uavcan/pnp/NodeIDAllocationData_2_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include "node/pnp.hpp"
#include "node/time.h"
#include "state.hpp"
#include "publishers.hpp"
#include "reception.hpp"
#include "node/essential/heartbeat.hpp"


namespace node::loops
{
void handle_1hz_loop(node::state::State &state)
{
    node::essential::publish_heartbeat(state.canard, state);
    transmit(state);
    printf("Heartbeat.\n");
    // Before code below is uncommented, make sure that the node has an id.
    // communications::publish_port_list(state.canard, state);
}

inline void handle_fast_loop(node::state::State &state)
{
    auto transfer = receive_transfer(state, 0);
    if (transfer.first.has_value())
    {
        transfer.second->handler(state, &transfer.first.value());
        //process_received_transfer(state, &transfer.value());
    }
    transmit(state);
}
}