/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */

#pragma once

#include <uavcan/pnp/NodeIDAllocationData_2_0.h>
#include <uavcan/pnp/NodeIDAllocationData_1_0.h>
#include <node/interfaces/IHandler.hpp>
#include <node/esc/esc_publishers.hpp>
#include "node/pnp.hpp"
#include "node/time.h"
#include "state.hpp"
#include "publishers.hpp"
#include "reception.hpp"
#include "node/essential/heartbeat.hpp"
#include "node/essential/port_list.hpp"
#include "node/esc/esc_publishers.hpp"
#include "node/esc/esc_publishers.hpp"


namespace node::loops
{
struct : ILoopMethod
{
  void operator()(node::state::State &state)
  {
    node::essential::publish_heartbeat(state.canard, state);
    publish_esc_heartbeat(state);
    publish_esc_feedback(state);
    transmit(state);
    // Before code below is uncommented, make sure that the node has an id.
    // communications::publish_port_list(state.canard, state);
  }
} handle_1hz_loop;

struct : ILoopMethod
{
  void operator()(node::state::State &state)
  {
    publish_port_list(state.canard, state);
    transmit(state);
  }
} handle_5_second_loop;

struct : ILoopMethod
{
  void operator()(node::state::State &state)
  {
    publish_esc_status(state);
    transmit(state);
  }
} handle_esc_status_loop;

struct : ILoopMethod
{
  void operator()(node::state::State &state)
  {
    std::pair<std::optional<CanardRxTransfer>, void *> transfer = receive_transfer(state);
    if (transfer.first.has_value())
    {
      CanardRxTransfer *canard_transfer = &transfer.first.value();
      if (transfer.second != nullptr)
      {
        //palWritePad(GPIOC, 11, 0);
        printf("handler for: %d\n", transfer.first.value().metadata.port_id);
        IHandler *handler = static_cast<IHandler *>(transfer.second);
        handler->operator()(state, canard_transfer);
        //palWritePad(GPIOC, 11, 1);
      } else
      {
        printf("Handler is a null pointer\n");
      }
      board::deallocate(static_cast<const uint8_t *>(transfer.first.value().payload));
    } else
    {
    }
    transmit(state);
  }
} handle_fast_loop;

}