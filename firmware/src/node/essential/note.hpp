/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "src/node/state/state.hpp"
#include <libcanard/canard.h>
#include "src/node/state/state.hpp"
#include <motor/motor.hpp>
#include "note.hpp"
#include "reg/udral/physics/acoustics/Note_0_1.h"
#include <node/interfaces/IHandler.hpp>

struct : IHandler
{
  void operator()(node::state::State &state, CanardRxTransfer *transfer)
  {
    (void) state;
    printf("Received note\n");
    reg_udral_physics_acoustics_Note_0_1 message{};
    size_t size = transfer->payload_size;
    if (reg_udral_physics_acoustics_Note_0_1_deserialize_(&message, (const uint8_t *) transfer->payload, &size) >=
        0)
    {
      motor_beep(message.frequency.hertz, message.duration.second * 1000);
    }
    return;
  }

} reg_udral_physics_acoustics_Note_0_1_handler;

