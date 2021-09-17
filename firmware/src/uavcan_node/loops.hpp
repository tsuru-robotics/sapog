#ifndef FIRMWARE_LOOPS_HPP
#define FIRMWARE_LOOPS_HPP

#include <uavcan/pnp/NodeIDAllocationData_2_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include "src/uavcan_node/plug_and_play/plug_and_play.hpp"
#include "state.hpp"
#include "publishes.hpp"
#include "reception.hpp"

using namespace node::state;
namespace node::loops
{
void handle1HzLoop(__attribute__((unused)) State &state)
{
    const bool anonymous = state.canard.node_id > CANARD_NODE_ID_MAX;
    if (!anonymous)
    {
        node::communications::publish_heartbeat(state.canard, state);
    } else
    {
        node::config::plug_and_play(state);
    }
}

void handle01HzLoop(__attribute__((unused)) State &state)
{
}

void handleFastLoop(__attribute__((unused)) State &state)
{
    receiveTransfer(state, 0);
    //receiveTransfer(state, 1);
    transmit(state);
}
}


#endif //FIRMWARE_LOOPS_HPP
