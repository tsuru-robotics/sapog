/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include "state.hpp"

using namespace node::state;

bool please_transmit(CanardFrame txf, CanardMicrosecond monotonic_micro_seconds, int index);

int transmit(State &state);
