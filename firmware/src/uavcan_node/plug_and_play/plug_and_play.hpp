#ifndef FIRMWARE_PLUG_AND_PLAY_HPP
#define FIRMWARE_PLUG_AND_PLAY_HPP

#include "uavcan_node/state.hpp"

using namespace node::state;
namespace node::config
{
bool SendPlugAndPlayRequest(State &state);

bool receivePlugAndPlayResponse(State &state);

bool subscribeToPlugAndPlayResponse(State &state);

bool saveNodeID(State &state);
}
#endif //FIRMWARE_PLUG_AND_PLAY_HPP
