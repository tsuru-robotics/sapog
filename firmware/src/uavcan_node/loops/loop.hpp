#ifndef FIRMWARE_LOOP_HPP
#define FIRMWARE_LOOP_HPP

#include <libcanard/canard.h>
#include <functional>
#include "uavcan_node/state.hpp"
#include <etl/delegate.h>
class Loop
{
public:
    Loop(etl::delegate<void(node::state::State &state)>, CanardMicrosecond next_loop_delay);
    int ID;
    CanardMicrosecond next_execution_at;

    bool shouldExecute(CanardMicrosecond current_time);

    void incrementNextExecution();

    std::function<void(node::state::State &state)> execution_function;
    CanardMicrosecond next_loop_delay;
};


#endif //FIRMWARE_LOOP_HPP
