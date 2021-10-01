#ifndef FIRMWARE_RECEPTION_HPP
#define FIRMWARE_RECEPTION_HPP

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
#include <board/unique_id.h>
#include <bxcan/bxcan.h>

using namespace node::state;

void processReceivedMessage(const State &state, const CanardTransfer *const transfer);

uavcan_node_GetInfo_Response_1_0 processRequestNodeGetInfo();

void processReceivedRequest(const State &state, const CanardTransfer *const transfer);

void processReceivedTransfer(const State &state, const CanardTransfer *const transfer);

std::optional<CanardTransfer> receiveTransfer(State &state, int if_index);

#endif //FIRMWARE_RECEPTION_HPP
