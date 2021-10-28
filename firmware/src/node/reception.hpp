/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

static const int max_frames_to_process_per_iteration = 1000;
#define NUNAVUT_ASSERT assert

#include <libcanard/canard.h>
#include <uavcan/node/GetInfo_1_0.h>
#include <board/board.hpp>
#include "state.hpp"
#include "units.hpp"
#include <cstddef>
#include <cstdio>
#include "time.h"
#include "node.hpp"
#include <board/unique_id.h>
#include <bxcan/bxcan.h>

using namespace node::state;

uavcan_node_GetInfo_Response_1_0 process_request_node_get_info();

void process_received_transfer(const State &state, const CanardTransfer *const transfer);

std::pair<std::optional<CanardTransfer>, SubscriptionData*> receive_transfer(State &state, int if_index);
bool uavcan_node_GetInfo_1_0_handler(const State &state, const CanardTransfer *const transfer);
bool uavcan_pnp_NodeIDAllocationData_1_0_handler(const State &state, const CanardTransfer *const transfer);
bool reg_udral_physics_acoustics_Note_0_1_handler(const State &state, const CanardTransfer *const transfer);
bool uavcan_register_Access_1_0_handler(const State &state, const CanardTransfer *const transfer);
bool not_implemented_handler(const State &state, const CanardTransfer *const transfer);