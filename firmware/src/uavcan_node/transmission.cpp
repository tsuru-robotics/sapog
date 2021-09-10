#include <bxcan.h>
#include "transmission.h"
#include "node_state.h"
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
    int array_size = sizeof(state.reduntant_interfaces) / sizeof(state.reduntant_interfaces[0]);
    for (int if_index = 0; if_index < array_size; ++if_index)
    {
        for (const CanardFrame *txf = NULL;
             (txf = canardTxPeek(&state.canard, if_index)) != NULL;)  // Look at the top of the TX queue.
        {
            bool isTimelyTransmission = (0U == txf->timestamp_usec) ||
                                        (txf->timestamp_usec > state.timing.current_time);
            if (!isTimelyTransmission)
            {
                remove_frame(state, if_index, txf);
                continue;
            }
            bool isDriverBusy = !please_transmit(*txf, state.timing.current_time, if_index);
            if (!isDriverBusy)
            {
                // txf was first used by canardTxPeek,
                // then by please_transmit, which is bxCanPush.
                // Now, txf is a pointer that needs to be deallocated in this scope.
                remove_frame(state, if_index, txf);
            } else
            { goto out_of_loop; }
        }
    }
    out_of_loop:;
}
