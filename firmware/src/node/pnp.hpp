/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#pragma once

#include "node/state.hpp"

using namespace node::state;
namespace node::config
{
bool send_plug_and_play_request(State &state);

bool receive_plug_and_play_response(State &state);

bool subscribe_to_plug_and_play_response(State &state);

bool save_node_id(State &state);

void plug_and_play_loop(State &state);

void save_crc(State &state);
}
