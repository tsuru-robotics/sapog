/*
 * Copyright (c) 2021 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <sys/unistd.h>
#include "node/reception.hpp"
#include "uavcan/_register/Name_1_0.h"
#include "zubax_chibios/zubax_chibios/config/config.h"
#include "transmit.hpp"
#include "node.hpp"

std::pair<std::optional<CanardTransfer>, SubscriptionData *> receive_transfer(State &state, int if_index)
{
    CanardFrame frame{};
    frame.timestamp_usec = get_monotonic_microseconds();
    std::array<std::uint8_t, 8> payload_array{};
    frame.payload = &payload_array;
    for (uint16_t i = 0; i < max_frames_to_process_per_iteration; ++i)
    {
        bool bxCanQueueHadSomething = bxCANPop(if_index,
                                               &frame.extended_can_id,
                                               &frame.payload_size, payload_array.data());
        if (!bxCanQueueHadSomething)
        {
            //palWritePad(GPIOC, 14, ~palReadPad(GPIOC, 14));
            palWritePad(GPIOC, 14, 1);
            chThdSleepMicroseconds(400); // 0.4 ms
            palWritePad(GPIOC, 14, 0);
            return {};
        }
        // The transfer is actually not stored here in this narrow scoped variable
        // Canard has an internal storage to make sure that it can receive frames in any order and assemble them into
        // transfers. If I now take a frame from bxCANPop and libcanard finds that it completes a transfer, it will
        // assign the transfer to the given CanardTransfer object. Not a bug!
        CanardTransfer transfer{};
        CanardRxSubscription *this_subscription;

        const int8_t canard_result = canardRxAcceptEx(&state.canard, &frame, if_index, &transfer, &this_subscription);
        //this_subscription->
        if (canard_result > 0)
        {
            return {transfer, static_cast<SubscriptionData *>(this_subscription->user_reference)};
            //state.canard.memory_free(&state.canard, (void *) transfer.payload);
        } else if ((canard_result == 0) || (canard_result == -CANARD_ERROR_OUT_OF_MEMORY))
        { ;  // Zero means that the frame did not complete a transfer so there is nothing to do.
            // OOM should never occur if the heap is sized correctly. We track OOM errors via heap API.
        } else
        {
            assert(false);  // No other error can possibly occur at runtime.
        }
    }
    return {};
}

bool not_implemented_handler(const State &state, const CanardTransfer *const transfer)
{
    (void) transfer;
    (void) state;
    return true;
}

