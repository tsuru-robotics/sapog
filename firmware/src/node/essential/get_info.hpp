/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <libcanard/canard.h>
#include "src/node/state/state.hpp"
#include <node/stop_gap.hpp>
#include <cstdio>
#include <uavcan/node/GetInfo_1_0.h>
#include <board/unique_id.h>
#include <node/units.hpp>
#include <node/interfaces/IHandler.hpp>
#include "board/board.hpp"
#include "get_info.hpp"

uavcan_node_GetInfo_Response_1_0 process_request_node_get_info();

UAVCAN_L6_NUNAVUT_C_SERVICE(uavcan_node_GetInfo,
                            1, 0);
namespace node::essential
{
struct : IHandler
{
  void operator()(node::state::State &state, CanardRxTransfer *transfer)
  {
    uavcan_l6::DSDL<uavcan_node_GetInfo_Response_1_0>::Serializer serializer{};
    auto res = serializer.serialize(process_request_node_get_info());
    if (res.has_value())
    {
      CanardTransferMetadata rtm = transfer->metadata;  // Response transfers are similar to their requests.
      rtm.transfer_kind = CanardTransferKindResponse;
      for (int i = 0; i <= board::detect_hardware_version().minor; ++i)
      {
        (void) canardTxPush(&state.queues[i], const_cast<CanardInstance *>(&state.canard),
                            transfer->timestamp_usec + ONE_SECOND_DEADLINE_usec,
                            &rtm,
                            res.value(),
                            serializer.getBuffer());
      }
    } else
    {
      assert(false);
    }
    return;
  }
} uavcan_node_GetInfo_1_0_handler;
}

