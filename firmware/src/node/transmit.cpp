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
inline void remove_frame(State &state, CanardTxQueue *queue, const CanardTxQueueItem *txf)
{
    // Remove the frame from the queue after it's transmitted.
    canardTxPop(queue, txf);
    // Deallocate the dynamic memory afterwards.
    state.canard.memory_free(&state.canard, (void *) txf);
}

/// Uses bxCAN to send all frames that have been queued in canard, returns the amount of frames that were sent
int transmit(State &state)
{
    palWritePad(GPIOB, 15, 0);
    int count_sent_frames = 0;
    for (int i = 0; i < AMOUNT_OF_QUEUES; ++i)
    {
        for (const CanardTxQueueItem *txf = NULL;
             (txf = canardTxPeek(&state.queues[i])) != nullptr;)  // Look at the top of the TX queue.
        {
            bool is_driver_busy = !bxCANPush(0, get_monotonic_microseconds(), (*txf).tx_deadline_usec,
                                             (*txf).frame.extended_can_id, (*txf).frame.payload_size,
                                             (*txf).frame.payload);
            if (!is_driver_busy)
            {
                // txf was first used by canardTxPeek, then by bxCanPush
                // Now, txf is a pointer that needs to be deallocated in this scope.
                assert(txf != nullptr);
                count_sent_frames++;
                remove_frame(state, &state.queues[i], txf);
            } else
            { break; }
        }
    }

    palWritePad(GPIOB, 15, 1);
    return count_sent_frames;
}
