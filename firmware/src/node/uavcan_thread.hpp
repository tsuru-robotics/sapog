/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <utility>
#include <uavcan/node/GetInfo_1_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include <uavcan/_register/Access_1_0.h>
#include <reg/udral/physics/acoustics/Note_0_1.h>
#include "libcanard/canard.h"
#include <deque>
#include <array>
#include "src/node/state/state.hpp"
#include "node/register_values/subscriptions.hpp"

#pragma once
namespace uavcan_node_1_0
{
int init();
}