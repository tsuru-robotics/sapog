#ifndef FIRMWARE_LOOPS_H
#define FIRMWARE_LOOPS_H

#include "node_state.h"
#include "publishes.hpp"
#include "reception.h"

using namespace node::state;
namespace node
{
    namespace loops
    {
        void handle1HzLoop(__attribute__((unused)) State& state)
        {

        }
        void handle01HzLoop(__attribute__((unused)) State& state)
        {
        }
        void handleFastLoop(__attribute__((unused)) State& state)
        {
            //node::communications::publish_heartbeat(state.canard, state);
            receiveTransfer(state, 0);
            //receiveTransfer(state, 1);
            transmit(state);
        }
    }
}


#endif //FIRMWARE_LOOPS_H
