/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "node/state.hpp"
#include <libcanard/canard.h>
#include "node/state.hpp"

bool uavcan_node_GetInfo_1_0_handler(const node::state::State &state, const CanardTransfer *const transfer);