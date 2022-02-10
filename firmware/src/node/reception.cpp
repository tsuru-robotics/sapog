/*
 * Copyright (c) 2022 Zubax, zubax.com
 * Distributed under the MIT License, available in the file LICENSE.
 * Author: Silver Valdvee <silver.valdvee@zubax.com>
 */
#include <sys/unistd.h>
#include "node/reception.hpp"
#include "uavcan/_register/Name_1_0.h"
#include "transmit.hpp"
#include "src/node/can_interrupt/extern_queue.hpp"
#include "node/interfaces/IHandler.hpp"
#include "board/board.hpp"

void receive_and_queue_for_processing(const uint8_t interface_index)
{
    if (board::get_max_can_interface_index() >= interface_index)
    {
        can_interrupt::frame frame{};
        bool bxCanQueueHadSomething = bxCANPop(interface_index,
                                               &frame.frame.extended_can_id,
                                               &frame.frame.payload_size, frame.payload.data());
        frame.frame.payload = frame.payload.data();
        if (bxCanQueueHadSomething)
        {
            can_interrupt::fifo_queues[interface_index].push(frame);
        }
    }
}

void accept_transfers(State &state)
{
    for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
    {
        while (true)
        {
            auto fifo_queue_item = can_interrupt::fifo_queues[i].pop();
            if (!fifo_queue_item.has_value())
            {
                can_interrupt::fifo_queues[i].reset();
                break;
            }
            CanardRxTransfer transfer{};
            CanardRxSubscription *this_subscription;
            volatile const int8_t canard_result = canardRxAccept(&state.canard, get_monotonic_microseconds(),
                                                                 &fifo_queue_item.value().frame,
                                                                 i,
                                                                 &transfer, &this_subscription);

            if (canard_result == 1)
            {
                if (this_subscription->user_reference != nullptr)
                {
                    IHandler *handler = static_cast<IHandler *>(this_subscription->user_reference);
                    handler->operator()(state, &transfer);
                    board::deallocate(static_cast<const uint8_t *>(transfer.payload));
                }
            }
        }
    }
}


std::pair<std::optional<CanardRxTransfer>, void *> receive_transfer(State &state)
{
    CanardFrame frame{};

    std::array<std::uint8_t, 8> payload_array{};
    frame.payload = &payload_array;

    for (uint16_t j = 0;
         j < (max_frames_to_process_per_iteration * (board::get_max_can_interface_index() + 1)); j += (
        board::get_max_can_interface_index() +
        1))
    {
        bool a_queue_had_something = false;

        for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
        {

            bool bxCanQueueHadSomething = bxCANPop(i,
                                                   &frame.extended_can_id,
                                                   &frame.payload_size, payload_array.data());
            a_queue_had_something = bxCanQueueHadSomething;
            // The transfer payload is actually not stored here in this narrow scoped variable
            CanardRxTransfer transfer{};
            CanardRxSubscription *this_subscription;

            const int8_t canard_result = canardRxAccept(&state.canard, get_monotonic_microseconds(), &frame, i,
                                                        &transfer, &this_subscription);
            if (canard_result > 0)
            {
                return {transfer, this_subscription->user_reference};
            }
        }
        bool canSleep = true;
        for (int i = 0; i <= board::get_max_can_interface_index(); ++i)
        {
            if (a_queue_had_something == true || canardTxPeek(&state.queues[i]) != nullptr)
            {
                canSleep = false;
            }
        }

        if (canSleep)
        {
            chThdSleepMicroseconds(10);
            return {};
        }
    }
    return {};
}

bool not_implemented_handler(const State &state, const CanardRxTransfer *const transfer)
{
    (void) transfer;
    (void) state;
    return true;
}

