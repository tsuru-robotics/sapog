#ifndef FIRMWARE_TRANSMISSION_H
#define FIRMWARE_TRANSMISSION_H
#include <libcanard/canard.h>
#include "node_state.h"
using namespace node::state;
bool please_transmit(CanardFrame txf, CanardMicrosecond monotonic_micro_seconds, int index);
void transmit(State &state);
#endif //FIRMWARE_TRANSMISSION_H
