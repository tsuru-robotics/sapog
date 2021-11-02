/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include <node/state.hpp>

using namespace node::state;

bool sub_esc_rpm_handler(const node::state::State &state, const CanardTransfer *const transfer);

bool sub_esc_duty_cycle_handler(const node::state::State &state, const CanardTransfer *const transfer);

bool reg_udral_physics_electricity_PowerTs_0_1_handler(const State &state, const CanardTransfer *const transfer);