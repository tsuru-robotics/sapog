/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include "loop.hpp"
#include <utility>

bool Loop::do_execute(CanardMicrosecond current_time) const
{
    return current_time >= (this->next_execution_at);
}

void Loop::increment_next_execution()
{
    this->next_execution_at += this->next_loop_delay;
}

Loop::Loop(std::function<void(node::state::State &state)> fun, CanardMicrosecond _next_loop_delay, CanardMicrosecond current_time) :
        next_loop_delay(_next_loop_delay),
        next_execution_at(current_time-1),
        execution_function(std::move(fun))
{
}