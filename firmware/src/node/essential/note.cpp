/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <libcanard/canard.h>
#include <node/state.hpp>
#include <motor/motor.hpp>
#include "note.hpp"
#include "reg/udral/physics/acoustics/Note_0_1.h"

bool reg_udral_physics_acoustics_Note_0_1_handler(const node::state::State &state, const CanardTransfer *const transfer)
{
    (void) state;
    reg_udral_physics_acoustics_Note_0_1 message{};
    size_t size = transfer->payload_size;
    if (reg_udral_physics_acoustics_Note_0_1_deserialize_(&message, (const uint8_t *) transfer->payload, &size) >= 0)
    {
        motor_beep(message.frequency.hertz, message.duration.second * 1000);
    }
    return true;
}
