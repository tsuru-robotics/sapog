/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include <functional>
#include "node/state.hpp"

class Loop
{
public:
    Loop(std::function<void(node::state::State &state)>, CanardMicrosecond next_loop_delay,
         CanardMicrosecond current_time);

    CanardMicrosecond next_loop_delay;

    CanardMicrosecond next_execution_at;

    bool do_execute(CanardMicrosecond current_time) const;

    void increment_next_execution();

    std::function<void(node::state::State &state)> execution_function;

    Loop &operator=(const Loop &other) = delete;
};