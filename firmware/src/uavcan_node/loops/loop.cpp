#include "loop.hpp"

#include <utility>

bool Loop::shouldExecute(CanardMicrosecond current_time)
{
    return current_time >= next_execution_at;
}

void Loop::incrementNextExecution()
{
    next_execution_at += next_loop_delay;
}

Loop::Loop(std::function<void(node::state::State &state)> fun, CanardMicrosecond _next_loop_delay) :
        execution_function(std::move(fun)),
        next_loop_delay(_next_loop_delay)
{
}