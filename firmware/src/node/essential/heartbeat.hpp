/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include <uavcan/node/Heartbeat_1_0.h>
#include "node/state.hpp"

void publish_heartbeat(CanardInstance &canard, node::state::State &state);