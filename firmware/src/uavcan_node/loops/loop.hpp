#ifndef FIRMWARE_LOOP_HPP
#define FIRMWARE_LOOP_HPP

#include <libcanard/canard.h>
#include <functional>
#include "uavcan_node/state.hpp"

class Loop
{
public:
    Loop(std::function<void(node::state::State &state)>, CanardMicrosecond next_loop_delay);

    CanardMicrosecond next_execution_at;

    bool do_execute(CanardMicrosecond current_time);

    void increment_next_execution();

    std::function<void(node::state::State &state)> execution_function;
    CanardMicrosecond next_loop_delay;
};


#endif //FIRMWARE_LOOP_HPP
