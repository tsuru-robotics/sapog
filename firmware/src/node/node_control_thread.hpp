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

#ifndef SAPOG_UAVCAN_NODE_1_0_HPP
#define SAPOG_UAVCAN_NODE_1_0_HPP
namespace uavcan_node_1_0
{
class UAVCANNode
{
public:
  static int init();
};
}


// This pair stores two pointers to iterators (an iterator is a pointer in implementation details), for start and end of
// the subscriptions array
std::pair<RegisteredPort *, RegisteredPort *>
get_ports_info_iterators();

#endif //SAPOG_UAVCAN_NODE_1_0_HPP
