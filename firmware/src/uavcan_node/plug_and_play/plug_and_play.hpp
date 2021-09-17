#ifndef FIRMWARE_PLUG_AND_PLAY_HPP
#define FIRMWARE_PLUG_AND_PLAY_HPP
#include "uavcan_node/state.hpp"
using namespace node::state;
namespace node::config {
    bool plug_and_play(State& state);
}
#endif //FIRMWARE_PLUG_AND_PLAY_HPP
