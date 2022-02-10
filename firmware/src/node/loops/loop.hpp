/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include <functional>
#include "src/node/state/state.hpp"
#include <node/interfaces/IHandler.hpp>

class Loop
{
public:
    Loop(ILoopMethod &_handler, CanardMicrosecond _next_loop_delay);

    CanardMicrosecond next_loop_delay;

    CanardMicrosecond next_execution_at;

    bool is_time_to_execute(CanardMicrosecond current_time) const;

    void increment_next_execution();

    ILoopMethod &handler;

    Loop &operator=(const Loop &other) = delete;
};