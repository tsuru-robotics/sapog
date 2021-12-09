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
#include "can_interrupt.hpp"

std::pair<std::optional<CanardRxTransfer>, void *> receive_transfer(State &state)
{
  CanardFrame frame{};

  std::array<std::uint8_t, 8> payload_array{};
  frame.payload = &payload_array;

  palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));
  for (uint16_t j = 0;
       j < (max_frames_to_process_per_iteration * BXCAN_MAX_IFACE_INDEX); j += (BXCAN_MAX_IFACE_INDEX + 1))
  {
    bool a_queue_had_something = false;

    for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
    {

      bool bxCanQueueHadSomething = bxCANPop(i,
                                             &frame.extended_can_id,
                                             &frame.payload_size, payload_array.data());
      a_queue_had_something = bxCanQueueHadSomething;
      // The transfer is actually not stored here in this narrow scoped variable
      // Canard has an internal storage to make sure that it can receive frames in any order and assemble them into
      // transfers. If I now take a frame from bxCANPop and libcanard finds that it completes a transfer, it will
      // assign the transfer to the given CanardTransfer object. Not a bug!
      CanardRxTransfer transfer{};
      CanardRxSubscription *this_subscription;

      const int8_t canard_result = canardRxAccept(&state.canard, get_monotonic_microseconds(), &frame, i,
                                                  &transfer, &this_subscription);
      //this_subscription->
      if (canard_result > 0)
      {
//                printf("Got full transfer: %d\n", transfer.metadata.port_id);
        return {transfer, this_subscription->user_reference};
        //state.canard.memory_free(&state.canard, (void *) transfer.payload);
      } else
      {
        if (transfer.metadata.port_id != 0)
        {
//                    printf("Got one frame of: %d\n", transfer.metadata.port_id);
        }
      }
    }
    bool canSleep = true;
    for (int i = 0; i <= BXCAN_MAX_IFACE_INDEX; ++i)
    {
      if (a_queue_had_something == true || canardTxPeek(&state.queues[i]) != nullptr)
      {
        canSleep = false;
      }
    }

    if (canSleep)
    {
      //palWritePad(GPIOC, 14, ~palReadPad(GPIOC, 14));
      //palWritePad(GPIOC, 14, 1);
      chThdSleepMicroseconds(10);
      //palWritePad(GPIOC, 14, 0);
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

void receive_and_queue_for_processing(const uint8_t interface_index)
{
  can_interrupt::frame frame{};
  bool bxCanQueueHadSomething = bxCANPop(interface_index,
                                         &frame.extended_can_id,
                                         &frame.payload_size, frame.payload.data());
  if (!bxCanQueueHadSomething)
  {
    assert(false);
  }
  can_interrupt::fifo_queue.push(frame);
}

