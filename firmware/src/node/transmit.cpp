/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <bxcan/bxcan.h>
#include <assert.h>
#include <cstdio>
#include <stm32f105xc.h>
#include <hal.h>
#include "transmit.hpp"
#include "state.hpp"
#include "libcanard/canard.h"
#include "time.h"

using namespace node::state;

// Removes the frame from the queue and deallocates the dynamic memory of it
void remove_frame(State &state, int if_index, const CanardFrame *txf)
{
    // Remove the frame from the queue after it's transmitted.
    canardTxPop(&state.canard, if_index);
    // Deallocate the dynamic memory afterwards.
    state.canard.memory_free(&state.canard, (CanardFrame *) txf);
}

/// Uses bxCAN to send all frames that have been queued in canard, returns the amount of frames that were sent
int transmit(State &state)
{
    palWritePad(GPIOB, 15, 0);
    int count_sent_frames = 0;
    for (const CanardFrame *txf = NULL;
         (txf = canardTxPeek(&state.canard, 0)) != nullptr;)  // Look at the top of the TX queue.
    {
        bool is_driver_busy = !bxCANPush(0, get_monotonic_microseconds(), (*txf).timestamp_usec,
                                         (*txf).extended_can_id, (*txf).payload_size,
                                         (*txf).payload);
        if (!is_driver_busy)
        {
            // txf was first used by canardTxPeek, then by bxCanPush
            // Now, txf is a pointer that needs to be deallocated in this scope.
            assert(txf != nullptr);
            count_sent_frames++;
            remove_frame(state, 0, txf);
        } else
        { break; }
    }
    palWritePad(GPIOB, 15, 1);
    return count_sent_frames;
}
