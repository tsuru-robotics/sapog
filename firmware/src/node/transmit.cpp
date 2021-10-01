#include <bxcan/bxcan.h>
#include "transmit.hpp"
#include "state.hpp"
#include "libcanard/canard.h"

// This project differs from ds015_demo
// Here we use bxCan and not SocketCan
bool please_transmit(const CanardFrame txf, CanardMicrosecond monotonic_micro_seconds, int index)
{
    return bxCANPush(index, monotonic_micro_seconds, txf.timestamp_usec, txf.extended_can_id, txf.payload_size,
                     txf.payload);
}

using namespace node::state;

// Removes the frame from the queue and deallocates the dynamic memory of it
void remove_frame(State &state, int if_index, const CanardFrame *txf)
{
    // Remove the frame from the queue after it's transmitted.
    canardTxPop(&state.canard, if_index);
    // Deallocate the dynamic memory afterwards.
    state.canard.memory_free(&state.canard, (CanardFrame *) txf);
}

void transmit(State &state)
{
    for (const CanardFrame *txf = NULL;
         (txf = canardTxPeek(&state.canard, 0)) != NULL;)  // Look at the top of the TX queue.
    {
        bool isDriverBusy = !bxCANPush(0, state.timing.current_time, (*txf).timestamp_usec,
                                       (*txf).extended_can_id, (*txf).payload_size,
                                       (*txf).payload);
        if (!isDriverBusy)
        {
            // txf was first used by canardTxPeek,
            // then by please_transmit, which is bxCanPush.
            // Now, txf is a pointer that needs to be deallocated in this scope.
            remove_frame(state, 0, txf);
        } else
        { break; }
    }
}
