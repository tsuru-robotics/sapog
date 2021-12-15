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
#include "src/node/state/state.hpp"
#include "units.hpp"
#include <cstddef>
#include <cstdio>
#include "time.h"
#include "uavcan_thread.hpp"
#include <board/unique_id.h>
#include <bxcan/bxcan.h>

using namespace node::state;

void accept_transfers(State &state);

// This function adds the received  transfer to a list in state that contains pairs of transfers and their handlers.
void receive_and_queue_for_processing(const uint8_t interface_index);

std::pair<std::optional<CanardRxTransfer>, void *> receive_transfer(State &state);

bool not_implemented_handler(const State &state, const CanardRxTransfer *const transfer);