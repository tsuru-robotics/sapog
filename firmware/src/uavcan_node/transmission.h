#ifndef FIRMWARE_TRANSMISSION_H
#define FIRMWARE_TRANSMISSION_H
#include <libcanard/canard.h>
static bool please_transmit(CanardFrame txf, CanardMicrosecond monotonic_micro_seconds, int index);
static __attribute__((unused)) void make_available_transmissions(State &state);
#endif //FIRMWARE_TRANSMISSION_H
