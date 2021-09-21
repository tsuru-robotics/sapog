#include "loop.hpp"

bool Loop::shouldExecute(CanardMicrosecond current_time)
{
    return current_time >= next_execution_at;
}

void Loop::incrementNextExecution()
{
    next_execution_at += next_loop_delay;
}

Loop::Loop(std::function<void(node::state::State &state)> fun, CanardMicrosecond next_loop_delay) : execution_function(
        fun), next_loop_delay(next_loop_delay)
{
}