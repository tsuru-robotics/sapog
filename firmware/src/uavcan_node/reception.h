#ifndef FIRMWARE_RECEPTION_H
#define FIRMWARE_RECEPTION_H

#include <libcanard/canard.h>
#include "node_state.h"
using namespace node::state;
void receiveTransfer(State& state){
    CanardTransfer transfer      = {0};
    const int8_t   canard_result = canardRxAccept(&state.canard, &frame, 0, &transfer);
    if (canard_result > 0)
    {
        processReceivedTransfer(&state, &transfer);
        state.canard.memory_free(&state.canard, (void*) transfer.payload);
    }
    else if ((canard_result == 0) || (canard_result == -CANARD_ERROR_OUT_OF_MEMORY))
    {
        ;  // Zero means that the frame did not complete a transfer so there is nothing to do.
        // OOM should never occur if the heap is sized correctly. We track OOM errors via heap API.
    }
    else
    {
        assert(false);  // No other error can possibly occur at runtime.
    }
}
__attribute__((unused)) void processReceivedTransfer(const State &state, const CanardTransfer *const transfer)
{

    if (transfer->transfer_kind != CanardTransferKindMessage) { return; }

}
#endif //FIRMWARE_RECEPTION_H
