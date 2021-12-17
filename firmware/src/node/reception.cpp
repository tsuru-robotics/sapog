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
#include "src/node/can_interrupt/extern_queue.hpp"
#include "node/interfaces/IHandler.hpp"
#include "board/board.hpp"

void receive_and_queue_for_processing(const uint8_t interface_index)
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

void accept_transfers(State &state)
{
  for (int i = 0; i <= board::detect_hardware_version().minor; ++i)
  {
    while (true)
    {
      auto fifo_queue_item = can_interrupt::fifo_queues[i].pop();
      if (!fifo_queue_item.has_value())
      {
        can_interrupt::fifo_queues[i].reset();
        break;
      }
//      printf("queues: %08x\n", reinterpret_cast<int>(&can_interrupt::fifo_queues));
      CanardRxTransfer transfer{};
      CanardRxSubscription *this_subscription;
      volatile const int8_t canard_result = canardRxAccept(&state.canard, get_monotonic_microseconds(),
                                                           &fifo_queue_item.value().frame,
                                                           i,
                                                           &transfer, &this_subscription);

      if (canard_result == 1)
      {
//        printf("Transfer\n");
        if (this_subscription->user_reference != nullptr)
        {
//          printf("subscription\n");
          IHandler *handler = static_cast<IHandler *>(this_subscription->user_reference);
          handler->operator()(state, &transfer);
          board::deallocate(static_cast<const uint8_t *>(transfer.payload));
        }
      } else if (canard_result == 0)
      {
//        printf("Queue %08x      ", static_cast<unsigned>(fifo_queue_item.value().frame.extended_can_id));
//        for (std::size_t x = 0; x < fifo_queue_item.value().frame.payload_size; x++)
//        {
//          printf("%02x ", fifo_queue_item.value().payload[x]);
//        }
//        printf("\n");
      }
    }
  }
}


std::pair<std::optional<CanardRxTransfer>, void *> receive_transfer(State &state)
{
  CanardFrame frame{};

  std::array<std::uint8_t, 8> payload_array{};
  frame.payload = &payload_array;

  //palWritePad(GPIOC, 12, ~palReadPad(GPIOC, 12));
  for (uint16_t j = 0;
       j < (max_frames_to_process_per_iteration * board::detect_hardware_version().minor); j += (
    board::detect_hardware_version().minor +
    1))
  {
    bool a_queue_had_something = false;

    for (int i = 0; i <= board::detect_hardware_version().minor; ++i)
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
    for (int i = 0; i <= board::detect_hardware_version().minor; ++i)
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

