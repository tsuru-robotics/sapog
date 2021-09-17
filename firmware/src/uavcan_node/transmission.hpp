#ifndef FIRMWARE_TRANSMISSION_HPP
#define FIRMWARE_TRANSMISSION_HPP
#include <libcanard/canard.h>
#include "state.hpp"
using namespace node::state;
bool please_transmit(CanardFrame txf, CanardMicrosecond monotonic_micro_seconds, int index);
void transmit(State &state);
#endif //FIRMWARE_TRANSMISSION_HPP
