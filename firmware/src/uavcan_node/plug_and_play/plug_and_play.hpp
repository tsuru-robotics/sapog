#ifndef FIRMWARE_PLUG_AND_PLAY_HPP
#define FIRMWARE_PLUG_AND_PLAY_HPP

#include "uavcan_node/state.hpp"

using namespace node::state;
namespace node::config
{
bool send_plug_and_play_request(State &state);

bool receive_plug_and_play_response(State &state);

bool subscribe_to_plug_and_play_response(State &state);

bool save_node_id(State &state);

void plug_and_play_loop(State &state);
}
#endif //FIRMWARE_PLUG_AND_PLAY_HPP
