/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include "node/state.hpp"

namespace node::essential
{
bool uavcan_register_Access_1_0_handler(const node::state::State &state, const CanardTransfer *const transfer);
}

